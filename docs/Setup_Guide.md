# Setup Guide

This document is the operational companion to the main `README.md`. The README explains the product and architecture; this guide focuses on getting the project running, understanding the output artifacts, and avoiding common evaluator friction.

## Prerequisites

Required:

- Python 3.11+ with `py` available on Windows
- internet access for package installation
- a valid Gemini API key

Recommended:

- PowerShell
- a fresh virtual environment inside the repo at `.venv`

## Fresh Setup From Scratch

Run these commands from the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
Copy-Item .env.example .env
```

Then open `.env` and set a real API key:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
```

## If `.venv` Already Exists

If the local virtual environment is already present, only run:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

You do not need to recreate the environment unless it is broken or uses the wrong Python version.

## Installed Dependencies

The repo currently depends on:

- `requests`
- `beautifulsoup4`
- `playwright`
- `python-dotenv`
- `google-generativeai`

Important: `playwright` requires a separate browser install step. `pip install playwright` alone is not enough.

## Environment Files

### `.venv/`

- local Python environment
- not committed
- should stay repo-local for repeatable runs

### `.env`

- local runtime config only
- not committed
- must contain the real `GEMINI_API_KEY`

### `.env.example`

- committed template
- documents the required environment variables
- safe to share

## Running the Tool

Run a single-page audit:

```powershell
.\.venv\Scripts\python.exe app.py https://example.com
```

Examples:

```powershell
.\.venv\Scripts\python.exe app.py https://www.scrapethissite.com/pages/forms/
.\.venv\Scripts\python.exe app.py https://www.scrapethissite.com/pages/ajax-javascript/
```

## What Happens During a Run

1. `app.py` validates the URL.
2. `scraper.py` tries `requests` first.
3. If the page content is too thin, `scraper.py` uses Playwright fallback.
4. `scraper.py` returns a full `MetricsDict`.
5. `ai.py` builds grounded prompts from metrics plus the text snippet.
6. `ai.py` requests a structured response from Gemini.
7. `ai.py` validates the response and retries once if needed.
8. `display.py` prints factual metrics separately from AI insights.
9. `app.py` writes output files.

## Output Files

### `output/latest.json`

Machine-readable export for downstream use. The shape is:

```json
{
  "timestamp": "...",
  "url": "...",
  "metrics": { "...": "..." },
  "insights": { "...": "..." }
}
```

Use this when you want the audit result as structured data instead of terminal output.

### `output/latest.txt`

Human-readable snapshot of the latest CLI report. This mirrors what the terminal printed for the most recent run.

### `prompt_logs/run.md`

Append-only log of AI execution details:

- URL
- fetch method
- parsed status
- system prompt
- each user prompt attempt
- raw API responses
- parsed output

This is the main debugging and review artifact for the AI layer.

### `prompt_logs/example_run.md`

Committed sample deliverable showing a real prompt-log entry from a successful run.

## Expected CLI Output Shape

The terminal output is intentionally split into sections:

1. factual metrics
2. AI insights
3. prioritized recommendations

This separation is required by the assignment and preserved in `display.py`.

## Common Issues and Fixes

### Missing API Key

Symptom:

- AI section returns an explicit config error

Fix:

- add `GEMINI_API_KEY` to `.env`

### Playwright Not Installed

Symptom:

- JS-heavy pages return a scraper error mentioning Playwright availability

Fix:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
```

### Rate Limited by Gemini

Symptom:

- AI section returns `Rate limited`

Fix:

- wait briefly and rerun
- avoid firing many audits in parallel
- run one page at a time during evaluation

### Invalid URL

Symptom:

- app exits before scraping

Fix:

- ensure the input starts with `http://` or `https://`

### Thin or Empty Content

Symptom:

- scraper falls back to Playwright or returns a meaningful-content error

Fix:

- confirm the page is publicly reachable
- confirm the page is not blocking automated traffic

## Suggested Evaluator-Friendly Flow

If you want the smoothest possible review experience:

1. create `.venv`
2. install dependencies
3. install Playwright Chromium
4. copy `.env.example` to `.env`
5. add the Gemini key
6. run one sample URL
7. inspect `output/latest.json`, `output/latest.txt`, and `prompt_logs/run.md`

## Notes on the Current AI Model Setting

The committed `.env.example` and `config.py` default to:

```env
GEMINI_MODEL=gemini-2.5-flash-lite
```

This matches the current local implementation and working setup for this repo.

## Reference Docs

If you want to trace the project back to the assignment intent, use these in order:

1. `docs/AI-Native Software Engineer`
2. `docs/Assignment Manual.md`
3. `docs/Architecture_Workflow_v2.md`
4. `docs/GPT Audit workflow improvments.md`
5. `docs/AI Tool Assignment Strategy.md`
