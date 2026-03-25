"""Prompt construction, model invocation, parsing, and logging only."""

from __future__ import annotations

import time
import warnings
from typing import TypedDict

from google.api_core import exceptions as google_exceptions

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    import google.generativeai as genai

from google.generativeai import types as genai_types

from config import (
    AI_MAX_OUTPUT_TOKENS,
    AI_RATE_LIMIT_RETRY_DELAY_SECONDS,
    AI_RETRY_LIMIT,
    AI_TIMEOUT_SECONDS,
    GEMINI_API_KEY,
    GEMINI_MODEL,
)
from scraper import MetricsDict


class RecommendationDict(TypedDict):
    priority: int
    action: str
    reasoning: str


class InsightsDict(TypedDict):
    seo_analysis: str
    messaging_clarity: str
    cta_usage: str
    content_depth: str
    ux_concerns: str
    recommendations: list[RecommendationDict]
    error: str | None


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Add it to the local .env file before running AI analysis.")

genai.configure(api_key=GEMINI_API_KEY)


def analyse(metrics: MetricsDict) -> InsightsDict:
    """Generate grounded insights from extracted metrics."""
    raise NotImplementedError


def _build_system_prompt() -> str:
    """Return the static system prompt."""
    return (
        "You are a senior web marketing analyst specialising in SEO, conversion rate "
        "optimisation, and content clarity for B2B marketing websites.\n\n"
        "You will receive:\n"
        "1. Structured factual metrics extracted from a webpage.\n"
        "2. A snippet of visible page text.\n\n"
        "Rules you must follow:\n"
        "- Every insight must cite a specific metric value by name and number.\n"
        "- Do not make observations that are not supported by the provided data.\n"
        "- Do not give generic advice.\n"
        "- Output only valid JSON.\n"
        "- Do not include markdown, code fences, or explanatory text.\n"
        "- Follow the exact JSON schema provided in the user prompt."
    )


def _build_user_prompt(metrics: MetricsDict) -> str:
    """Return the per-run user prompt with injected metrics."""
    h1_list = _preview_texts(metrics["h1_texts"], limit=3)
    cta_list = _preview_texts(metrics["cta_texts"], limit=5)

    return f"""FACTUAL METRICS - cite these by name in every insight:

word_count: {metrics["word_count"]}
h1_count: {metrics["h1_count"]} (text: {h1_list})
h2_count: {metrics["h2_count"]}
h3_count: {metrics["h3_count"]}
cta_count: {metrics["cta_count"]} (text: {cta_list})
internal_links: {metrics["internal_links"]}
external_links: {metrics["external_links"]}
image_count: {metrics["image_count"]}
missing_alt_pct: {metrics["missing_alt_pct"]:.1f}%
meta_title: "{metrics["meta_title"]}" ({metrics["meta_title_len"]} chars)
meta_description: "{metrics["meta_description"]}" ({metrics["meta_desc_len"]} chars)
fetch_method: {metrics["fetch_method"]}

PAGE TEXT SNIPPET:
{metrics["page_text_snippet"] or "No visible text extracted."}

Return ONLY this JSON structure and do not add any extra keys:
{{
  "seo_analysis": "...",
  "messaging_clarity": "...",
  "cta_usage": "...",
  "content_depth": "...",
  "ux_concerns": "...",
  "recommendations": [
    {{"priority": 1, "action": "...", "reasoning": "..."}},
    {{"priority": 2, "action": "...", "reasoning": "..."}},
    {{"priority": 3, "action": "...", "reasoning": "..."}}
  ]
}}"""


def _call_api(system_prompt: str, user_prompt: str) -> str:
    """Call the configured model and return the raw response text."""
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=system_prompt,
        generation_config=genai_types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=AI_MAX_OUTPUT_TOKENS,
            response_mime_type="application/json",
        ),
    )

    for attempt in range(AI_RETRY_LIMIT + 1):
        try:
            response = model.generate_content(
                user_prompt,
                request_options={"timeout": AI_TIMEOUT_SECONDS},
            )
            return _response_text(response)
        except google_exceptions.TooManyRequests as exc:
            if attempt >= AI_RETRY_LIMIT:
                raise RuntimeError("Rate limited") from exc
            time.sleep(AI_RATE_LIMIT_RETRY_DELAY_SECONDS)
        except google_exceptions.DeadlineExceeded as exc:
            raise TimeoutError("API timeout") from exc
        except (
            google_exceptions.InternalServerError,
            google_exceptions.ServiceUnavailable,
        ) as exc:
            status_code = getattr(exc, "code", "unknown")
            raise RuntimeError(f"Gemini API error {status_code}") from exc
        except google_exceptions.GoogleAPIError as exc:
            status_code = getattr(exc, "code", "unknown")
            raise RuntimeError(f"Gemini API error {status_code}") from exc

    raise RuntimeError("Rate limited")


def _parse_response(raw_response: str) -> InsightsDict:
    """Parse and validate the raw model response."""
    raise NotImplementedError


def _write_log(system_prompt: str, user_prompt: str, raw_response: str, metrics: MetricsDict) -> None:
    """Append a prompt log entry for the current run."""
    raise NotImplementedError


def _empty_insights(error: str | None = None) -> InsightsDict:
    """Return a safe insights object that satisfies the contract."""
    return {
        "seo_analysis": "",
        "messaging_clarity": "",
        "cta_usage": "",
        "content_depth": "",
        "ux_concerns": "",
        "recommendations": [],
        "error": error,
    }


def _preview_texts(values: list[str], limit: int) -> str:
    """Format a short readable preview list for prompt injection."""
    preview = ", ".join(values[:limit])
    return preview or "none detected"


def _response_text(response: object) -> str:
    """Return the raw model text or raise if no text payload is present."""
    text = getattr(response, "text", "")
    if isinstance(text, str) and text.strip():
        return text.strip()

    raise RuntimeError("Gemini API returned an empty response")
