"""HTML fetching and factual metric extraction only."""

from __future__ import annotations

from typing import TypedDict


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
    raise NotImplementedError


def _fetch(url: str) -> str:
    """Fetch static HTML using the requests-first path."""
    raise NotImplementedError


def _fetch_playwright(url: str) -> str:
    """Fetch rendered HTML using the Playwright fallback path."""
    raise NotImplementedError


def _extract(html: str, base_url: str) -> MetricsDict:
    """Extract factual metrics from HTML only."""
    raise NotImplementedError


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
