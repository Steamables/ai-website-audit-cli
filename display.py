"""CLI rendering only."""

from __future__ import annotations

from textwrap import fill
from typing import TYPE_CHECKING

from config import (
    META_DESCRIPTION_TARGET_MAX,
    META_DESCRIPTION_TARGET_MIN,
    META_DESCRIPTION_WARNING_MAX,
    META_DESCRIPTION_WARNING_MIN,
    META_TITLE_TARGET_MAX,
    META_TITLE_TARGET_MIN,
    META_TITLE_WARNING_MAX,
    META_TITLE_WARNING_MIN,
    THIN_CONTENT_WORD_COUNT,
)
from scraper import MetricsDict

if TYPE_CHECKING:
    from ai import InsightsDict

_SECTION_RULE = "=" * 62
_TEXT_WIDTH = 78


def render(metrics: MetricsDict, insights: InsightsDict) -> str:
    """Render the full CLI output."""
    sections = [render_metrics(metrics), render_insights(insights)]

    if not insights["error"]:
        recommendations = _render_recommendations(insights["recommendations"])
        if recommendations:
            sections.append(recommendations)

    return "\n\n".join(section for section in sections if section)


def render_metrics(metrics: MetricsDict) -> str:
    """Render the factual metrics section."""
    h1_text = ", ".join(f"'{text}'" for text in metrics["h1_texts"][:3]) or "none detected"
    cta_text = ", ".join(f"'{text}'" for text in metrics["cta_texts"][:5]) or "none detected"
    missing_alt_count = round(metrics["image_count"] * metrics["missing_alt_pct"] / 100)

    lines = [
        "WEBSITE AUDIT - FACTUAL METRICS",
        _SECTION_RULE,
        f"URL: {metrics['url']}",
        f"Fetch method: {metrics['fetch_method']}",
    ]

    if metrics["error"]:
        lines.append(f"Scraper status: {metrics['error']}")

    lines.extend(
        [
            "",
            "Content",
            f"Word count: {_format_number(metrics['word_count'])}{_word_count_warning(metrics['word_count'])}",
            (
                f"H1 / H2 / H3: {metrics['h1_count']} / {metrics['h2_count']} / {metrics['h3_count']}"
                f"{_h1_warning(metrics['h1_count'])}"
            ),
            f"H1 text: {h1_text}",
            "",
            "Conversion",
            f"CTAs: {metrics['cta_count']} ({cta_text}){_cta_warning(metrics['cta_count'])}",
            f"Internal links: {_format_number(metrics['internal_links'])}",
            f"External links: {_format_number(metrics['external_links'])}",
            "",
            "SEO",
            (
                f"Meta title: '{metrics['meta_title']}' ({metrics['meta_title_len']} chars)"
                f"{_meta_title_note(metrics['meta_title_len'])}"
            ),
            (
                f"Meta description: '{metrics['meta_description']}' ({metrics['meta_desc_len']} chars)"
                f"{_meta_description_note(metrics['meta_desc_len'])}"
            ),
            "",
            "Media",
            (
                f"Images: {_format_number(metrics['image_count'])} | "
                f"Missing alt text: {metrics['missing_alt_pct']:.1f}% ({missing_alt_count} of {metrics['image_count']})"
                f"{_alt_warning(metrics['missing_alt_pct'])}"
            ),
        ]
    )

    return "\n".join(lines)


def render_insights(insights: InsightsDict) -> str:
    """Render the AI insights section."""
    lines = ["AI INSIGHTS", _SECTION_RULE]

    if insights["error"]:
        lines.append(_wrap_text(f"AI analysis unavailable: {insights['error']}"))
        return "\n".join(lines)

    sections = (
        ("SEO Structure", insights["seo_analysis"]),
        ("Messaging Clarity", insights["messaging_clarity"]),
        ("CTA Usage", insights["cta_usage"]),
        ("Content Depth", insights["content_depth"]),
        ("UX Concerns", insights["ux_concerns"]),
    )

    for heading, content in sections:
        lines.extend(["", heading, _wrap_text(content or "No insight returned.")])

    return "\n".join(lines)


def _render_recommendations(recommendations: list[dict[str, object]]) -> str:
    """Render the prioritised recommendations section."""
    if not recommendations:
        return ""

    lines = ["RECOMMENDATIONS (PRIORITISED)", _SECTION_RULE]
    ordered = sorted(recommendations, key=lambda item: int(item.get("priority", 999)))

    for recommendation in ordered:
        priority = recommendation.get("priority", "?")
        action = str(recommendation.get("action", "")).strip() or "No action provided."
        reasoning = str(recommendation.get("reasoning", "")).strip() or "No reasoning provided."
        lines.extend(
            [
                "",
                f"[{priority}] {action}",
                _wrap_text(f"Reason: {reasoning}"),
            ]
        )

    return "\n".join(lines)


def _wrap_text(value: str) -> str:
    """Wrap long lines for terminal readability."""
    return fill(value, width=_TEXT_WIDTH)


def _format_number(value: int) -> str:
    """Format integers with separators."""
    return f"{value:,}"


def _word_count_warning(word_count: int) -> str:
    """Return a warning note for thin content."""
    if word_count < THIN_CONTENT_WORD_COUNT:
        return " [warning: thin content]"
    return ""


def _h1_warning(h1_count: int) -> str:
    """Return a warning note for H1 structure."""
    if h1_count == 0:
        return " [warning: no H1 found]"
    if h1_count > 1:
        return " [warning: multiple H1s]"
    return ""


def _cta_warning(cta_count: int) -> str:
    """Return a warning note when no CTAs are detected."""
    if cta_count == 0:
        return " [warning: no CTAs detected]"
    return ""


def _meta_title_note(length: int) -> str:
    """Return a warning note for meta title length."""
    if length < META_TITLE_WARNING_MIN:
        return f" [warning: too short, target {META_TITLE_TARGET_MIN}-{META_TITLE_TARGET_MAX}]"
    if length > META_TITLE_WARNING_MAX:
        return f" [warning: too long, target {META_TITLE_TARGET_MIN}-{META_TITLE_TARGET_MAX}]"
    return f" [target: {META_TITLE_TARGET_MIN}-{META_TITLE_TARGET_MAX}]"


def _meta_description_note(length: int) -> str:
    """Return a warning note for meta description length."""
    if length < META_DESCRIPTION_WARNING_MIN:
        return (
            f" [warning: too short, target "
            f"{META_DESCRIPTION_TARGET_MIN}-{META_DESCRIPTION_TARGET_MAX}]"
        )
    if length > META_DESCRIPTION_WARNING_MAX:
        return (
            f" [warning: too long, target "
            f"{META_DESCRIPTION_TARGET_MIN}-{META_DESCRIPTION_TARGET_MAX}]"
        )
    return f" [target: {META_DESCRIPTION_TARGET_MIN}-{META_DESCRIPTION_TARGET_MAX}]"


def _alt_warning(missing_alt_pct: float) -> str:
    """Return a warning note when alt text is missing."""
    if missing_alt_pct > 0:
        return " [warning]"
    return ""
