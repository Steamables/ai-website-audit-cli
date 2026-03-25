# AI-Powered Website Audit Tool

A CLI-based, AI-native website audit tool for single-page analysis. The system first extracts factual website metrics, then passes those grounded metrics into an AI layer that produces structured insights and prioritized recommendations. The scraper, AI layer, orchestration, and CLI rendering are kept deliberately separate because that separation is part of the core system design.

This project was built to satisfy the assignment requirements for a grounded, CLI-based AI website audit tool, especially the emphasis on:

- clean separation between scraping and AI analysis
- structured, predictable outputs
- grounded AI reasoning tied to extracted metrics
- prompt logging / reasoning trace visibility
- practical trade-offs for modern JS-heavy websites

## Start Here

If you are trying to set up the environment and run the tool, go directly to:

`docs/Setup_Guide.md`

That guide contains the exact install commands, `.env` setup, Playwright browser install step, run commands, output-file locations, and common troubleshooting notes.

## What the Tool Does

Given a single URL, the tool:

1. validates the URL in `app.py`
2. fetches the page with `requests`
3. falls back to Playwright when static HTML is too thin
4. extracts factual metrics in `scraper.py`
5. builds grounded prompts in `ai.py`
6. requests structured JSON insights from Gemini
7. validates the AI response and retries once if the output is too generic or not grounded
8. renders factual metrics separately from AI insights in the CLI
9. writes machine-readable and human-readable outputs to `output/`
10. appends a full reasoning trace to `prompt_logs/run.md`

## Core Metrics Collected

The scraper extracts factual metrics only:

- total word count
- H1, H2, H3 counts
- H1 text values
- CTA count and CTA texts
- internal and external link counts
- image count
- percentage of images missing alt text
- meta title and meta description, plus lengths
- page text snippet for AI grounding
- fetch method (`requests` or `playwright`)

These metrics are displayed separately from AI-generated insights, as required by the assignment.

## Architecture Overview

Data flow:

`URL -> app.py -> scraper.py -> MetricsDict -> ai.py -> InsightsDict -> display.py -> CLI/output files`

Module responsibilities:

| File | Responsibility | Must Not Do |
| --- | --- | --- |
| `scraper.py` | Fetch HTML, fallback fetch, parse HTML, extract factual metrics | Call AI or build prompts |
| `ai.py` | Build prompts, call Gemini, parse JSON, validate grounded output, write prompt logs | Fetch pages or parse HTML |
| `app.py` | Validate input, orchestrate the flow, write outputs | Contain heavy business logic |
| `display.py` | Render CLI output with metrics and AI insights clearly separated | Fetch data or call AI |
| `config.py` | Store constants only | Hold orchestration logic |

This structure follows the assignment requirements directly. The goal is not to create a large framework, but a disciplined, testable AI system with clear boundaries.

## Why This Is AI-Native Instead of "Scrape Then Summarize"

The AI layer is constrained by structured inputs rather than loose page dumps:

- factual metrics are extracted first
- metric names and values are injected explicitly into the user prompt
- the system prompt instructs the model to reference specific metrics
- the AI response must match a strict `InsightsDict` contract
- invalid or generic AI output is rejected and retried once with stricter instructions
- prompt logs capture prompts, raw model output, parsed output, and retry behavior

This matters because the assignment is primarily evaluating AI-system design, not scraping difficulty alone.

## AI Design Decisions

### 1. Metrics Before Prose

The prompt is built from extracted metrics first and a page text snippet second. This anchors the model in actual facts like `word_count`, `cta_count`, `missing_alt_pct`, and heading counts before it reads free-form content.

### 2. Structured Output Contract

The AI layer returns a strict `InsightsDict` shape:

- `seo_analysis`
- `messaging_clarity`
- `cta_usage`
- `content_depth`
- `ux_concerns`
- `recommendations`
- `error`

This makes the AI response easier to validate, log, render, and export.

### 3. Lightweight Validation Loop

The model output is not trusted blindly. The AI layer:

- strips JSON fences if needed
- validates required keys and recommendation structure
- rejects shallow or generic output
- retries once with stricter instructions when the first answer is low quality

This came directly from the improvement guidance and is one of the strongest differentiators of the system.

### 4. Snippet Instead of Raw HTML

The AI receives a cleaned page text snippet rather than raw HTML. This reduces prompt noise and token usage while still giving the model enough page context to reason about messaging and content quality.

## Reliability and Failure Handling

The tool is designed to fail predictably rather than crash:

- invalid URL -> early exit from `app.py`
- request timeout / connection error -> structured scraper error
- non-200 response -> structured scraper error
- empty HTML -> structured scraper error
- thin static HTML -> Playwright fallback
- Playwright unavailable -> structured scraper error with install guidance
- missing API key -> explicit AI error at call time
- Gemini API failure / timeout / rate limit -> structured AI error
- invalid AI JSON -> structured AI error
- missing required AI fields -> structured AI error

When scraping fails, the CLI still renders the factual section and shows that AI analysis was skipped or unavailable.

## Hybrid Fetching Strategy

The scraper uses a requests-first strategy with a Playwright fallback:

- `requests` is faster and simpler for static pages
- when extracted text is below the configured threshold, the tool assumes the page may be JS-rendered
- Playwright then renders the page and extraction runs again on the rendered HTML

This is a practical compromise for modern marketing websites and was explicitly recommended in the assignment guidance.

## Output Files

Every successful or partially successful run produces artifacts under the repo root:

- `output/latest.json`
  machine-readable payload with `timestamp`, `url`, `metrics`, and `insights`
- `output/latest.txt`
  human-readable snapshot of the CLI output
- `prompt_logs/run.md`
  append-only reasoning trace with prompts, attempts, raw model output, and parsed status
- `prompt_logs/example_run.md`
  committed sample prompt log deliverable

## Prompt Logging

Prompt logging is treated as a first-class deliverable, not an afterthought. Each run writes:

- URL
- fetch method
- parsed status
- system prompt
- each user prompt attempt
- each raw model response
- final parsed output

This makes the AI layer inspectable and easier to debug or review.

## Project Structure

```text
AI-powered Website Audit Tool/
|-- app.py
|-- scraper.py
|-- ai.py
|-- display.py
|-- config.py
|-- requirements.txt
|-- .env.example
|-- README.md
|-- docs/
|   `-- Setup_Guide.md
|-- output/
|   `-- latest.json / latest.txt
`-- prompt_logs/
    |-- example_run.md
    `-- run.md
```

## Dependencies

Installed through `requirements.txt`:

- `requests`
- `beautifulsoup4`
- `playwright`
- `python-dotenv`
- `google-generativeai`

Playwright also requires:

```powershell
.\.venv\Scripts\python.exe -m playwright install chromium
```

## Quick Start

### 1. Create a virtual environment

```powershell
py -m venv .venv
```

### 2. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

### 3. Configure environment variables

```powershell
Copy-Item .env.example .env
```

Set a real Gemini API key in `.env`:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
```

### 4. Run the tool

```powershell
.\.venv\Scripts\python.exe app.py https://example.com
```

For more detailed setup and operational guidance, see `docs/Setup_Guide.md`.

## Example Run Targets

The tool was exercised against sample pages from `https://www.scrapethissite.com/pages/`, including:

- `/pages/simple/`
- `/pages/forms/`
- `/pages/ajax-javascript/`
- `/pages/frames/`

These pages are useful because they mix static content, structured data, and light dynamic behavior.

## Trade-Offs

### 1. Requests + Playwright Hybrid

This improves coverage for JS-heavy pages but adds browser-install complexity and a heavier local setup than a pure `requests` solution.

### 2. Single-Page Scope

The tool intentionally analyzes one page only. That keeps the assignment focused and architecture simple, but it means the output is not a site-wide SEO audit.

### 3. Snippet-Based AI Context

Passing a snippet instead of the full page reduces token cost and noise, but deeper context from very long pages may be missed.

### 4. Single Retry on AI Quality

Retrying once helps reject generic AI output without overcomplicating the system. It also avoids runaway API usage, but repeated failures may still result in a structured AI error.

### 5. Gemini Rate Limits

The current implementation uses Gemini through `google-generativeai`, which is simple for this assignment but can hit rate limits when many runs are made in a short period.

## What Would You Improve With More Time

- deploy the tool so it can be used without local setup
- add a simple user interface where someone can paste in a URL instead of using only the CLI
- let users audit a few important pages in one run instead of one page at a time
- keep a history of past audits so teams can compare results over time
- make the final report easier to share with cleaner export options for internal teams or clients
- improve the presentation of results with clearer summaries and easier-to-scan output

## Submission Notes

This project intentionally prioritizes clarity, grounded AI behavior, and predictable outputs over extra features. The assignment itself frames the problem as an AI-system-design task, so the design choices here favor:

- strict module boundaries
- explicit data contracts
- inspectable prompt construction
- graceful failure behavior
- useful agency-relevant output

## Additional Documentation

- `docs/Setup_Guide.md` for detailed environment setup and usage
- `prompt_logs/example_run.md` for the committed prompt-log deliverable

## AI Reference Links

This project was implemented as an AI-native assignment with support from external AI planning and workflow references. These links are included as supporting context only:

- Claude AI user manual and workflow architecture:
  https://claude.ai/share/800c9cba-35b7-42bf-9221-c0377a01dc39
- ChatGPT AI-native thoughts and strategies:
  https://chatgpt.com/share/69c39495-e2a8-83a6-8c10-c87ac4863b1e
- ChatGPT AI tool assignment strategy:
  https://chatgpt.com/share/69c39613-972c-83a7-ac9e-db795e31c6ca
