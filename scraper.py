"""HTML fetching and factual metric extraction only."""

from __future__ import annotations

import re
from typing import TypedDict
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag

from config import (
    CHROME_UA,
    PAGE_TEXT_SNIPPET_CHARS,
    PLAYWRIGHT_TIMEOUT_MS,
    PLAYWRIGHT_TRIGGER_WORD_COUNT,
    REQUEST_TIMEOUT_SECONDS,
)

_CTA_KEYWORDS = (
    "book",
    "buy",
    "call",
    "contact",
    "demo",
    "download",
    "get started",
    "join",
    "learn more",
    "order",
    "pricing",
    "quote",
    "request",
    "schedule",
    "shop",
    "sign up",
    "start",
    "subscribe",
    "talk to sales",
    "try",
)
_CTA_BLOCKLIST = {
    "back",
    "close",
    "menu",
    "next",
    "open menu",
    "previous",
    "prev",
}
_CTA_MAX_WORDS = 6


class MetricsDict(TypedDict):
    url: str
    fetch_method: str
    word_count: int
    h1_count: int
    h2_count: int
    h3_count: int
    h1_texts: list[str]
    cta_count: int
    cta_texts: list[str]
    internal_links: int
    external_links: int
    image_count: int
    missing_alt_pct: float
    meta_title: str
    meta_title_len: int
    meta_description: str
    meta_desc_len: int
    page_text_snippet: str
    error: str | None


class FetchError(Exception):
    """Raised when a page cannot be fetched or parsed meaningfully."""


def scrape(url: str) -> MetricsDict:
    """Fetch a URL and return the structured metrics contract."""
    try:
        static_html = _fetch(url)
    except FetchError as exc:
        return _empty_metrics(url, str(exc))

    metrics = _extract(static_html, url)
    if metrics["error"] is not None:
        return metrics

    if metrics["word_count"] >= PLAYWRIGHT_TRIGGER_WORD_COUNT:
        return metrics

    try:
        rendered_html = _fetch_playwright(url)
    except FetchError as exc:
        error = str(exc)
        fetch_method = "requests" if error.startswith("Playwright not available") else "playwright"
        return _empty_metrics(url, error, fetch_method=fetch_method)

    rendered_metrics = _extract(rendered_html, url)
    if rendered_metrics["error"] is not None:
        return _empty_metrics(url, rendered_metrics["error"], fetch_method="playwright")

    if rendered_metrics["word_count"] < PLAYWRIGHT_TRIGGER_WORD_COUNT:
        return _empty_metrics(
            url,
            "Could not extract meaningful content",
            fetch_method="playwright",
        )

    rendered_metrics["fetch_method"] = "playwright"
    return rendered_metrics



def _fetch(url: str) -> str:
    """Fetch static HTML using the requests-first path."""
    headers = {"User-Agent": CHROME_UA}

    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    except requests.Timeout as exc:
        raise FetchError(f"Fetch timeout after {REQUEST_TIMEOUT_SECONDS}s") from exc
    except requests.ConnectionError as exc:
        raise FetchError("Could not reach URL") from exc
    except requests.RequestException as exc:
        raise FetchError(f"Request failed: {exc}") from exc

    if response.status_code != requests.codes.ok:
        raise FetchError(f"HTTP {response.status_code}")

    html = response.text.strip()
    if not html:
        raise FetchError("Empty HTML response")

    return html


def _fetch_playwright(url: str) -> str:
    """Fetch rendered HTML using the Playwright fallback path."""
    try:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise FetchError(
            "Playwright not available - install with: playwright install chromium"
        ) from exc

    browser = None
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page(user_agent=CHROME_UA)
            page.goto(url, wait_until="networkidle", timeout=PLAYWRIGHT_TIMEOUT_MS)
            html = page.content().strip()
    except PlaywrightError as exc:
        raise FetchError(f"Playwright fetch failed: {exc}") from exc
    except Exception as exc:
        raise FetchError(f"Playwright fetch failed: {exc}") from exc
    finally:
        if browser is not None:
            browser.close()

    if not html:
        raise FetchError("Could not extract meaningful content")

    return html


def _extract(html: str, base_url: str) -> MetricsDict:
    """Extract factual metrics from HTML only."""
    try:
        soup = BeautifulSoup(html, "html.parser")
        body = soup.body or soup

        visible_text = _extract_visible_text(body)
        h1_texts = _extract_tag_texts(soup.find_all("h1"))
        cta_texts = _extract_cta_texts(soup)
        internal_links, external_links = _classify_links(soup, base_url)

        images = soup.find_all("img")
        image_count = len(images)
        missing_alt_count = sum(1 for image in images if not (image.get("alt") or "").strip())
        missing_alt_pct = (
            round((missing_alt_count / image_count) * 100, 1) if image_count else 0.0
        )

        meta_title = _clean_text(soup.title.get_text(" ", strip=True) if soup.title else "")
        meta_description = _extract_meta_description(soup)

        return {
            "url": base_url,
            "fetch_method": "requests",
            "word_count": _count_words(visible_text),
            "h1_count": len(h1_texts),
            "h2_count": len(soup.find_all("h2")),
            "h3_count": len(soup.find_all("h3")),
            "h1_texts": h1_texts,
            "cta_count": len(cta_texts),
            "cta_texts": cta_texts,
            "internal_links": internal_links,
            "external_links": external_links,
            "image_count": image_count,
            "missing_alt_pct": missing_alt_pct,
            "meta_title": meta_title,
            "meta_title_len": len(meta_title),
            "meta_description": meta_description,
            "meta_desc_len": len(meta_description),
            "page_text_snippet": visible_text[:PAGE_TEXT_SNIPPET_CHARS],
            "error": None,
        }
    except Exception as exc:
        return _empty_metrics(base_url, f"Failed to parse HTML: {exc}")


def _extract_visible_text(root: Tag | BeautifulSoup) -> str:
    """Return visible page text with obvious non-content tags removed."""
    working_root = BeautifulSoup(str(root), "html.parser")
    for element in working_root(["script", "style", "noscript", "template"]):
        element.decompose()

    return _clean_text(working_root.get_text(" ", strip=True))


def _extract_tag_texts(tags: list[Tag]) -> list[str]:
    """Return cleaned non-empty text from a set of tags."""
    texts: list[str] = []
    for tag in tags:
        text = _clean_text(tag.get_text(" ", strip=True))
        if text:
            texts.append(text)

    return texts


def _extract_cta_texts(soup: BeautifulSoup) -> list[str]:
    """Return CTA-like text from buttons and action-oriented links."""
    cta_texts: list[str] = []

    for button in soup.find_all("button"):
        text = _cta_candidate_text(button)
        button_type = _clean_text((button.get("type") or "")).casefold()
        if text and (_is_cta_text(text) or button_type == "submit"):
            cta_texts.append(text)

    for anchor in soup.find_all("a", href=True):
        text = _cta_candidate_text(anchor)
        if text and _is_cta_text(text):
            cta_texts.append(text)

    return list(dict.fromkeys(cta_texts))


def _element_label(tag: Tag) -> str:
    """Extract the best available user-facing label for an element."""
    for candidate in (tag.get_text(" ", strip=True), tag.get("aria-label"), tag.get("title")):
        cleaned = _clean_text(candidate or "")
        if cleaned:
            return cleaned

    return ""


def _cta_candidate_text(tag: Tag) -> str:
    """Return a cleaned CTA candidate only if it passes basic quality filters."""
    text = _element_label(tag)
    if not text:
        return ""

    normalized = text.casefold()
    if normalized in _CTA_BLOCKLIST:
        return ""

    if len(text.split()) > _CTA_MAX_WORDS:
        return ""

    return text


def _is_cta_text(text: str) -> bool:
    """Apply a simple action-oriented heuristic to anchor text."""
    if not text:
        return False

    normalized = text.casefold()
    return any(keyword in normalized for keyword in _CTA_KEYWORDS)


def _classify_links(soup: BeautifulSoup, base_url: str) -> tuple[int, int]:
    """Classify links as internal or external relative to the input URL."""
    internal_links = 0
    external_links = 0
    base_host = _normalized_host(urlparse(base_url).netloc)

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()
        if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
            continue

        resolved = urljoin(base_url, href)
        parsed = urlparse(resolved)
        if parsed.scheme not in {"http", "https"}:
            continue

        link_host = _normalized_host(parsed.netloc)
        if _is_internal_host(base_host, link_host):
            internal_links += 1
        else:
            external_links += 1

    return internal_links, external_links


def _normalized_host(host: str) -> str:
    """Normalize a host for loose same-site comparison."""
    normalized = host.casefold().strip()
    return normalized[4:] if normalized.startswith("www.") else normalized


def _is_internal_host(base_host: str, link_host: str) -> bool:
    """Treat exact hosts and subdomains as internal."""
    if not base_host or not link_host:
        return False

    return (
        link_host == base_host
        or link_host.endswith(f".{base_host}")
        or base_host.endswith(f".{link_host}")
    )


def _extract_meta_description(soup: BeautifulSoup) -> str:
    """Extract a cleaned meta description string."""
    meta_tag = soup.find(
        "meta",
        attrs={"name": lambda value: isinstance(value, str) and value.casefold() == "description"},
    )
    if meta_tag is None:
        return ""

    return _clean_text(meta_tag.get("content", ""))


def _count_words(text: str) -> int:
    """Count word-like tokens in visible text."""
    return len(re.findall(r"\b\w+\b", text))


def _clean_text(value: str) -> str:
    """Collapse repeated whitespace into a single space."""
    return re.sub(r"\s+", " ", value).strip()


def _empty_metrics(url: str, error: str, fetch_method: str = "requests") -> MetricsDict:
    """Return a safe metrics object that satisfies the contract."""
    return {
        "url": url,
        "fetch_method": fetch_method,
        "word_count": 0,
        "h1_count": 0,
        "h2_count": 0,
        "h3_count": 0,
        "h1_texts": [],
        "cta_count": 0,
        "cta_texts": [],
        "internal_links": 0,
        "external_links": 0,
        "image_count": 0,
        "missing_alt_pct": 0.0,
        "meta_title": "",
        "meta_title_len": 0,
        "meta_description": "",
        "meta_desc_len": 0,
        "page_text_snippet": "",
        "error": error,
    }
