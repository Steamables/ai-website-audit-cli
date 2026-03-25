"""CLI entrypoint and top-level orchestration only."""

from __future__ import annotations

import sys
from urllib.parse import urlparse

from config import VALID_URL_SCHEMES


def _is_valid_url(url: str) -> bool:
    """Validate that the input is an HTTP or HTTPS URL."""
    parsed = urlparse(url)
    return parsed.scheme in VALID_URL_SCHEMES and bool(parsed.netloc)


def main(url: str) -> None:
    """Run the website audit flow."""
    raise NotImplementedError


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python app.py https://example.com")
        sys.exit(1)

    candidate_url = sys.argv[1].strip()
    if not _is_valid_url(candidate_url):
        print("Error: please provide a valid http/https URL.")
        sys.exit(1)

    main(candidate_url)
