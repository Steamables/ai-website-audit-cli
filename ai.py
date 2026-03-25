"""Prompt construction, model invocation, parsing, and logging only."""

from __future__ import annotations

import json
import time
import warnings
from datetime import datetime, timezone
from pathlib import Path
from typing import TypedDict

from google.api_core import exceptions as google_exceptions

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    import google.generativeai as genai

from google.generativeai import types as genai_types

from config import (
    AI_MAX_OUTPUT_TOKENS,
    AI_RECOMMENDATION_MAX_COUNT,
    AI_RECOMMENDATION_MIN_COUNT,
    AI_RATE_LIMIT_RETRY_DELAY_SECONDS,
    AI_RETRY_LIMIT,
    AI_TIMEOUT_SECONDS,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    PROMPT_LOG_DIR,
    PROMPT_LOG_FILE,
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

_REQUIRED_INSIGHT_KEYS = {
    "seo_analysis",
    "messaging_clarity",
    "cta_usage",
    "content_depth",
    "ux_concerns",
    "recommendations",
}
_REQUIRED_RECOMMENDATION_KEYS = {"priority", "action", "reasoning"}
_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "seo_analysis": {"type": "string"},
        "messaging_clarity": {"type": "string"},
        "cta_usage": {"type": "string"},
        "content_depth": {"type": "string"},
        "ux_concerns": {"type": "string"},
        "recommendations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "priority": {"type": "integer"},
                    "action": {"type": "string"},
                    "reasoning": {"type": "string"},
                },
                "required": ["priority", "action", "reasoning"],
            },
        },
    },
    "required": [
        "seo_analysis",
        "messaging_clarity",
        "cta_usage",
        "content_depth",
        "ux_concerns",
        "recommendations",
    ],
}
_GENERIC_PHRASES = (
    "improve seo",
    "improve your seo",
    "enhance user experience",
    "improve user experience",
    "improve content",
    "optimize content",
    "optimize seo",
    "strengthen messaging",
    "improve messaging",
    "improve cta usage",
    "consider improving",
)
_LAST_PARSED_STATUS = "not_run"
_LAST_PARSED_OUTPUT = ""


def analyse(metrics: MetricsDict) -> InsightsDict:
    """Generate grounded insights from extracted metrics."""
    global _LAST_PARSED_OUTPUT, _LAST_PARSED_STATUS

    system_prompt = _build_system_prompt()
    user_prompt = _build_user_prompt(metrics)
    attempts_log: list[dict[str, str]] = []
    insights = _empty_insights("AI analysis failed before completion")

    try:
        for attempt in range(AI_RETRY_LIMIT + 1):
            current_user_prompt = (
                user_prompt if attempt == 0 else _build_retry_user_prompt(user_prompt, insights["error"] or "")
            )
            raw_response = ""
            attempt_error = ""

            try:
                raw_response = _call_api(system_prompt, current_user_prompt)
            except (RuntimeError, TimeoutError) as exc:
                attempt_error = str(exc)
                insights = _empty_insights(attempt_error)
                attempts_log.append(
                    {
                        "attempt": str(attempt + 1),
                        "user_prompt": current_user_prompt,
                        "raw_response": raw_response or "(empty response)",
                        "result": attempt_error,
                    }
                )
                break

            insights = _parse_response(raw_response)
            quality_error = None if insights["error"] else _quality_error(insights, metrics)
            attempt_result = insights["error"] or quality_error or "accepted"
            attempts_log.append(
                {
                    "attempt": str(attempt + 1),
                    "user_prompt": current_user_prompt,
                    "raw_response": raw_response or "(empty response)",
                    "result": attempt_result,
                }
            )
            if quality_error is None:
                break

            insights = _empty_insights(quality_error)
            if attempt >= AI_RETRY_LIMIT:
                break

        _LAST_PARSED_STATUS = "success" if insights["error"] is None else f"error - {insights['error']}"
        _LAST_PARSED_OUTPUT = json.dumps(insights, indent=2)
        return insights
    finally:
        _write_log(system_prompt, attempts_log, metrics)


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
        "- Use the literal metric labels from the prompt, such as word_count, h1_count, "
        "h2_count, h3_count, cta_count, internal_links, external_links, image_count, "
        "missing_alt_pct, meta_title_len, and meta_desc_len.\n"
        "- Do not make observations that are not supported by the provided data.\n"
        "- Do not give generic advice.\n"
        "- Keep each analysis field to 1-2 concise sentences.\n"
        "- Keep each recommendation reasoning to 1 concise sentence.\n"
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
meta_title: "{metrics["meta_title"]}"
meta_title_len: {metrics["meta_title_len"]}
meta_description: "{metrics["meta_description"]}"
meta_desc_len: {metrics["meta_desc_len"]}
fetch_method: {metrics["fetch_method"]}

PAGE TEXT SNIPPET:
{metrics["page_text_snippet"] or "No visible text extracted."}

Keep the response concise:
- Each analysis field: maximum 2 sentences
- Each recommendation action: short and specific
- Each recommendation reasoning: 1 sentence grounded in metrics
- In every analysis field, include at least one literal metric label and value such as "word_count is 124" or "cta_count is 0"

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
    _configure_client()

    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=system_prompt,
        generation_config=genai_types.GenerationConfig(
            candidate_count=1,
            max_output_tokens=AI_MAX_OUTPUT_TOKENS,
            response_mime_type="application/json",
            response_schema=_RESPONSE_SCHEMA,
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
    try:
        payload = _extract_json_payload(raw_response)
        data = json.loads(payload)
    except json.JSONDecodeError:
        return _empty_insights("Invalid JSON response")

    if not isinstance(data, dict):
        return _empty_insights("Invalid JSON response")

    if set(data.keys()) != _REQUIRED_INSIGHT_KEYS:
        return _empty_insights("Incomplete AI response")

    recommendations = data.get("recommendations")
    if not isinstance(recommendations, list):
        return _empty_insights("Incomplete AI response")

    if not AI_RECOMMENDATION_MIN_COUNT <= len(recommendations) <= AI_RECOMMENDATION_MAX_COUNT:
        return _empty_insights("Incomplete AI response")

    normalized_recommendations: list[RecommendationDict] = []
    for recommendation in recommendations:
        if not isinstance(recommendation, dict):
            return _empty_insights("Incomplete AI response")
        if set(recommendation.keys()) != _REQUIRED_RECOMMENDATION_KEYS:
            return _empty_insights("Incomplete AI response")

        try:
            priority = int(recommendation["priority"])
        except (TypeError, ValueError):
            return _empty_insights("Incomplete AI response")

        action = str(recommendation["action"]).strip()
        reasoning = str(recommendation["reasoning"]).strip()
        if not action or not reasoning:
            return _empty_insights("Incomplete AI response")

        normalized_recommendations.append(
            {
                "priority": priority,
                "action": action,
                "reasoning": reasoning,
            }
        )

    return {
        "seo_analysis": str(data["seo_analysis"]).strip(),
        "messaging_clarity": str(data["messaging_clarity"]).strip(),
        "cta_usage": str(data["cta_usage"]).strip(),
        "content_depth": str(data["content_depth"]).strip(),
        "ux_concerns": str(data["ux_concerns"]).strip(),
        "recommendations": normalized_recommendations,
        "error": None,
    }


def _write_log(system_prompt: str, attempts_log: list[dict[str, str]], metrics: MetricsDict) -> None:
    """Append a prompt log entry for the current run."""
    PROMPT_LOG_DIR.mkdir(parents=True, exist_ok=True)

    attempt_sections: list[str] = []
    if attempts_log:
        for entry in attempts_log:
            attempt_sections.extend(
                [
                    f"### Attempt {entry['attempt']}",
                    f"**Result:** {entry['result']}",
                    "#### User Prompt",
                    "```text",
                    entry["user_prompt"],
                    "```",
                    "#### Raw API Response",
                    "```text",
                    entry["raw_response"],
                    "```",
                ]
            )
    else:
        attempt_sections.extend(
            [
                "### Attempt 1",
                "**Result:** No API attempt recorded",
                "#### User Prompt",
                "```text",
                "(no prompt recorded)",
                "```",
                "#### Raw API Response",
                "```text",
                "(empty response)",
                "```",
            ]
        )

    log_entry = "\n".join(
        [
            "---",
            f"## Run - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}",
            f"**URL:** {metrics['url']}",
            f"**Fetch method:** {metrics['fetch_method']}",
            f"**Parsed status:** {_LAST_PARSED_STATUS}",
            "### Design Decisions",
            "- Metrics are passed field-by-field instead of as a raw JSON blob.",
            "- The prompt requires every insight to reference explicit metric values.",
            "- A stricter retry is used when the output is invalid or too generic.",
            "### System Prompt",
            "```text",
            system_prompt,
            "```",
            *attempt_sections,
            "### Parsed Output",
            "```json",
            _LAST_PARSED_OUTPUT or json.dumps(_empty_insights("No parsed output"), indent=2),
            "```",
            "---",
            "",
        ]
    )

    Path(PROMPT_LOG_FILE).write_text(
        Path(PROMPT_LOG_FILE).read_text(encoding="utf-8") + log_entry
        if Path(PROMPT_LOG_FILE).exists()
        else log_entry,
        encoding="utf-8",
    )


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


def _configure_client() -> None:
    """Configure the Gemini client lazily so non-AI paths can still import this module."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set. Add it to the local .env file before running AI analysis.")

    genai.configure(api_key=GEMINI_API_KEY)


def _response_text(response: object) -> str:
    """Return the raw model text or raise if no text payload is present."""
    text = getattr(response, "text", "")
    if isinstance(text, str) and text.strip():
        return text.strip()

    raise RuntimeError("Gemini API returned an empty response")


def _build_retry_user_prompt(base_prompt: str, reason: str) -> str:
    """Make the retry prompt stricter when the first output is invalid or generic."""
    return (
        f"{base_prompt}\n\n"
        "RETRY INSTRUCTIONS:\n"
        f"- The previous response was rejected: {reason or 'invalid or low quality output'}.\n"
        "- Every section must explicitly reference the provided metric names and values.\n"
        "- Use literal labels like word_count, h1_count, cta_count, missing_alt_pct, meta_title_len, or meta_desc_len.\n"
        "- Recommendations must be specific and actionable, with reasoning tied to metrics.\n"
        "- Keep every field concise so the JSON completes in full.\n"
        "- Do not include generic advice.\n"
        "- Return valid JSON only."
    )


def _extract_json_payload(raw_response: str) -> str:
    """Strip markdown fences and isolate the JSON object payload."""
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines:
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end >= start:
        return cleaned[start : end + 1]

    return cleaned


def _quality_error(insights: InsightsDict, metrics: MetricsDict) -> str | None:
    """Reject structurally valid but shallow or ungrounded AI output."""
    section_rules = (
        ("seo_analysis", _metric_tokens(metrics["h1_count"], metrics["meta_title_len"], metrics["meta_desc_len"])),
        (
            "messaging_clarity",
            _metric_tokens(
                metrics["word_count"],
                metrics["meta_desc_len"],
                *metrics["h1_texts"][:3],
                metrics["meta_description"],
            ),
        ),
        ("cta_usage", _metric_tokens(metrics["cta_count"], *metrics["cta_texts"][:5])),
        ("content_depth", _metric_tokens(metrics["word_count"], metrics["h2_count"], metrics["h3_count"])),
        (
            "ux_concerns",
            _metric_tokens(
                metrics["image_count"],
                metrics["missing_alt_pct"],
                metrics["internal_links"],
                metrics["external_links"],
            ),
        ),
    )

    for field, tokens in section_rules:
        content = insights[field].strip()
        if len(content) < 25:
            return f"{field} is too short to be useful"
        if _looks_generic(content):
            return f"{field} is too generic"
        if not _contains_metric_token(content, tokens):
            return f"{field} is not grounded in the provided metrics"

    for recommendation in insights["recommendations"]:
        action = recommendation["action"].strip()
        reasoning = recommendation["reasoning"].strip()
        if len(action) < 8 or _looks_generic(action):
            return "Recommendation actions are too generic"
        if len(reasoning) < 18 or not _contains_metric_token(
            reasoning,
            _metric_tokens(
                metrics["word_count"],
                metrics["h1_count"],
                metrics["h2_count"],
                metrics["h3_count"],
                metrics["cta_count"],
                metrics["internal_links"],
                metrics["external_links"],
                metrics["image_count"],
                metrics["missing_alt_pct"],
                metrics["meta_title_len"],
                metrics["meta_desc_len"],
                *metrics["h1_texts"][:3],
                *metrics["cta_texts"][:5],
            ),
        ):
            return "Recommendation reasoning is not grounded in the provided metrics"

    return None


def _metric_tokens(*values: object) -> set[str]:
    """Build a set of text tokens that should appear in grounded output."""
    tokens: set[str] = set()
    for value in values:
        if isinstance(value, int):
            tokens.add(str(value))
            tokens.add(f"{value:,}")
        elif isinstance(value, float):
            tokens.add(f"{value:.1f}")
            tokens.add(f"{value:.1f}%")
        elif isinstance(value, str):
            cleaned = value.strip()
            if cleaned:
                tokens.add(cleaned.casefold())

    return tokens


def _contains_metric_token(text: str, tokens: set[str]) -> bool:
    """Check whether the output explicitly includes at least one metric token."""
    normalized_text = text.casefold()
    return any(token and token.casefold() in normalized_text for token in tokens)


def _looks_generic(text: str) -> bool:
    """Reject shallow filler phrases that are not specific enough."""
    normalized = text.casefold()
    return any(phrase in normalized for phrase in _GENERIC_PHRASES)
