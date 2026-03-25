"""CLI rendering only."""

from __future__ import annotations

from ai import InsightsDict
from scraper import MetricsDict


def render(metrics: MetricsDict, insights: InsightsDict) -> str:
    """Render the full CLI output."""
    raise NotImplementedError


def render_metrics(metrics: MetricsDict) -> str:
    """Render the factual metrics section."""
    raise NotImplementedError


def render_insights(insights: InsightsDict) -> str:
    """Render the AI insights section."""
    raise NotImplementedError
