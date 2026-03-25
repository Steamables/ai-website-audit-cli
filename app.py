"""CLI entrypoint and top-level orchestration only."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse

from ai import InsightsDict, analyse
from config import LATEST_JSON_PATH, LATEST_TEXT_PATH, OUTPUT_DIR, VALID_URL_SCHEMES
from display import render
from scraper import MetricsDict, scrape


def _is_valid_url(url: str) -> bool:
    """Validate that the input is an HTTP or HTTPS URL."""
    parsed = urlparse(url)
    return parsed.scheme in VALID_URL_SCHEMES and bool(parsed.netloc)


def main(url: str) -> None:
    """Run the website audit flow."""
    metrics = scrape(url)
    insights = analyse(metrics) if metrics["error"] is None else _skipped_insights()
    report = render(metrics, insights)

    _display(report)
    _write_outputs(url, metrics, insights, report)


def _display(report: str) -> None:
    """Render and print the final report."""
    print(report)


def _write_outputs(url: str, metrics: MetricsDict, insights: InsightsDict, report: str) -> None:
    """Write the latest machine-readable and text outputs."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "url": url,
        "metrics": metrics,
        "insights": insights,
    }

    LATEST_JSON_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    LATEST_TEXT_PATH.write_text(report, encoding="utf-8")


def _skipped_insights() -> InsightsDict:
    """Return a safe AI placeholder when scraping fails."""
    return {
        "seo_analysis": "",
        "messaging_clarity": "",
        "cta_usage": "",
        "content_depth": "",
        "ux_concerns": "",
        "recommendations": [],
        "error": "AI analysis skipped because scraping failed.",
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py https://example.com")
        sys.exit(1)

    candidate_url = sys.argv[1].strip()
    if not _is_valid_url(candidate_url):
        print("Error: please provide a valid http/https URL.")
        sys.exit(1)

    main(candidate_url)
