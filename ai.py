"""Prompt construction, model invocation, parsing, and logging only."""

from __future__ import annotations

from typing import TypedDict

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


def analyse(metrics: MetricsDict) -> InsightsDict:
    """Generate grounded insights from extracted metrics."""
    raise NotImplementedError


def _build_system_prompt() -> str:
    """Return the static system prompt."""
    raise NotImplementedError


def _build_user_prompt(metrics: MetricsDict) -> str:
    """Return the per-run user prompt with injected metrics."""
    raise NotImplementedError


def _call_api(system_prompt: str, user_prompt: str) -> str:
    """Call the configured model and return the raw response text."""
    raise NotImplementedError


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
