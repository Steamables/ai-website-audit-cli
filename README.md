# AI-Powered Website Audit Tool

CLI-based website audit tool with strict separation between scraping, AI analysis,
orchestration, and display.

## Planned Structure

- `scraper.py`: fetch HTML and extract factual metrics only
- `ai.py`: build prompts, call the model, parse structured insights only
- `app.py`: validate input and orchestrate the flow
- `display.py`: render factual metrics separately from AI insights
- `config.py`: shared constants only

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
Copy-Item .env.example .env
```

Set `GEMINI_API_KEY` in `.env` before running the tool.

## Run

```powershell
.\.venv\Scripts\python.exe app.py https://example.com
```
