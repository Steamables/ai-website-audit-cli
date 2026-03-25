"""Project-wide constants for the website audit tool."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final

from dotenv import load_dotenv

load_dotenv()

BASE_DIR: Final[Path] = Path(__file__).resolve().parent

VALID_URL_SCHEMES: Final[tuple[str, str]] = ("http", "https")

CHROME_UA: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

REQUEST_TIMEOUT_SECONDS: Final[int] = 15
PLAYWRIGHT_TIMEOUT_MS: Final[int] = 15_000
AI_TIMEOUT_SECONDS: Final[int] = 30
AI_RATE_LIMIT_RETRY_DELAY_SECONDS: Final[int] = 5
AI_RETRY_LIMIT: Final[int] = 1
AI_MAX_OUTPUT_TOKENS: Final[int] = 1_500

PLAYWRIGHT_TRIGGER_WORD_COUNT: Final[int] = 100
THIN_CONTENT_WORD_COUNT: Final[int] = 300
PAGE_TEXT_SNIPPET_CHARS: Final[int] = 1_200

META_TITLE_WARNING_MIN: Final[int] = 30
META_TITLE_WARNING_MAX: Final[int] = 65
META_TITLE_TARGET_MIN: Final[int] = 50
META_TITLE_TARGET_MAX: Final[int] = 60

META_DESCRIPTION_WARNING_MIN: Final[int] = 120
META_DESCRIPTION_WARNING_MAX: Final[int] = 165
META_DESCRIPTION_TARGET_MIN: Final[int] = 150
META_DESCRIPTION_TARGET_MAX: Final[int] = 160

AI_RECOMMENDATION_MIN_COUNT: Final[int] = 3
AI_RECOMMENDATION_MAX_COUNT: Final[int] = 5

PROMPT_LOG_DIR: Final[Path] = BASE_DIR / "prompt_logs"
PROMPT_LOG_FILE: Final[Path] = PROMPT_LOG_DIR / "run.md"
OUTPUT_DIR: Final[Path] = BASE_DIR / "output"
LATEST_JSON_PATH: Final[Path] = OUTPUT_DIR / "latest.json"
LATEST_TEXT_PATH: Final[Path] = OUTPUT_DIR / "latest.txt"

GEMINI_MODEL: Final[str] = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
GEMINI_API_KEY: Final[str] = os.getenv("GEMINI_API_KEY", "").strip()
