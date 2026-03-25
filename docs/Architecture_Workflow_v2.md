**Architecture & Workflow**

**Specification**

AI-Native Website Audit Tool

_Implementation-ready. Built for a developer to code directly from this document._

# **1\. System Flow - Full Execution Pipeline**

Complete step-by-step execution from URL input to final output. Every step includes what each module receives, what it returns, and the data format at that stage.

| **\[1\] URL Input & Validation**<br><br>app.py receives URL string from CLI argument (sys.argv\[1\]) or interactive prompt.<br><br>_IN: raw string \| ACTION: validate format with urllib.parse \| OUT: validated URL string or exit(1)_        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **▼**                                                                                                                                                                                                                                           |
| **◆ DECISION Is the URL a valid http/https URL with a reachable host?**<br><br>YES → proceed → call scraper.scrape(url)<br><br>NO → print error message → exit(1) - do not proceed                                                              |
| **▼**                                                                                                                                                                                                                                           |
| **\[2\] scraper.scrape(url) called**<br><br>app.py hands off URL to scraper module. scraper takes full control until it returns.<br><br>_IN: url: str \| OUT: MetricsDict (see Section 2)_                                                      |
| **▼**                                                                                                                                                                                                                                           |
| **\[3\] HTTP Fetch - requests.get()**<br><br>scraper.\_fetch(url): GET with realistic User-Agent header. Timeout: 15s.<br><br>_IN: url: str \| OUT: raw HTML string or raises FetchError_                                                       |
| **▼**                                                                                                                                                                                                                                           |
| **◆ DECISION Did fetch succeed AND does parsed body contain > 100 words?**<br><br>YES → proceed with BeautifulSoup parsing on raw HTML<br><br>NO → trigger scraper.\_fetch_playwright(url) - JS fallback                                        |
| **▼**                                                                                                                                                                                                                                           |
| **\[4\] HTML Parsing & Metric Extraction**<br><br>scraper.\_extract(html, base*url): BeautifulSoup parses HTML. All 14 metric fields populated.<br><br>\_IN: html: str, base_url: str \| OUT: MetricsDict with fetch_method field set*          |
| **▼**                                                                                                                                                                                                                                           |
| **\[5\] MetricsDict returned to app.py**<br><br>scraper.scrape() returns clean dict. No HTML. No raw content except page*text_snippet.<br><br>\_IN: - \| OUT: MetricsDict (typed dict, all keys always present)*                                |
| **▼**                                                                                                                                                                                                                                           |
| **\[6\] ai.analyse(metrics) called**<br><br>app.py passes MetricsDict to AI module. AI module takes full control until it returns.<br><br>_IN: metrics: MetricsDict \| OUT: InsightsDict (see Section 2)_                                       |
| **▼**                                                                                                                                                                                                                                           |
| **\[7\] Prompt Construction**<br><br>ai.\_build*system_prompt() + ai.\_build_user_prompt(metrics): inject all metric values into template.<br><br>\_IN: metrics: MetricsDict \| OUT: system_prompt: str, user_prompt: str*                      |
| **▼**                                                                                                                                                                                                                                           |
| **\[8\] Gemini API Call**<br><br>ai.\_call*api(system, user): POST to Gemini. model=gemini-1.5-flash. max_tokens=1500. timeout=30s.<br><br>\_IN: system: str, user: str \| OUT: raw_response: str (JSON string)*                                |
| **▼**                                                                                                                                                                                                                                           |
| **◆ DECISION Is raw_response valid JSON with all required InsightsDict keys?**<br><br>YES → parse → return InsightsDict to app.py<br><br>NO → strip \`\`\`json fences → retry parse → if still invalid, return ErrorInsightsDict                |
| **▼**                                                                                                                                                                                                                                           |
| **\[9\] Prompt Log Written**<br><br>ai.\_write*log(): appends timestamped run to prompt_logs/run.md. Always runs - even on API error.<br><br>\_Writes: url, timestamp, system_prompt, user_prompt, raw_response, parsed_status*                 |
| **▼**                                                                                                                                                                                                                                           |
| **\[10\] Output Rendered**<br><br>app.py calls display.render(metrics, insights): prints FACTUAL METRICS section, then AI INSIGHTS section, then RECOMMENDATIONS.<br><br>_IN: metrics + insights \| OUT: structured CLI output (see Section 6)_ |

# **2\. Module Interfaces - Strict Contracts**

Every function signature and data shape is defined here. Treat these as immutable contracts between modules.

## **2.1 MetricsDict - scraper.py output contract**

\# scraper.py → app.py → ai.py

\# All keys ALWAYS present. Missing data uses defaults, not None.

MetricsDict = {

'url': str, # the input URL

'fetch_method': str, # 'requests' | 'playwright'

'word_count': int, # body text word count

'h1_count': int,

'h2_count': int,

'h3_count': int,

'h1_texts': list\[str\], # actual heading text - used in AI prompt

'cta_count': int,

'cta_texts': list\[str\], # button/link text - used in AI prompt

'internal_links': int,

'external_links': int,

'image_count': int,

'missing_alt_pct': float, # 0.0-100.0. 0.0 if image_count == 0

'meta_title': str, # '' if not found

'meta_title_len': int, # 0 if not found

'meta_description': str, # '' if not found

'meta_desc_len': int, # 0 if not found

'page_text_snippet': str, # first 1200 chars of visible body text

'error': str | None, # None on success, message string on failure

}

## **2.2 InsightsDict - ai.py output contract**

\# ai.py → app.py

\# Returned on success OR error. app.py always receives a valid dict.

InsightsDict = {

'seo_analysis': str, # must reference h1_count, meta lengths

'messaging_clarity': str, # must reference h1_texts, word_count

'cta_usage': str, # must reference cta_count, cta_texts

'content_depth': str, # must reference word_count, h2_count

'ux_concerns': str, # must reference image/alt data, link counts

'recommendations': \[

{

'priority': int, # 1 = highest

'action': str, # specific, actionable

'reasoning': str, # references metric values explicitly

},

\# 3-5 items

\],

'error': str | None, # None on success, error message on failure

}

## **2.3 Public Function Signatures**

\# scraper.py

def scrape(url: str) -> MetricsDict: ...

def \_fetch(url: str) -> str: ... # raises FetchError on failure

def \_fetch_playwright(url: str) -> str: ... # raises FetchError on failure

def \_extract(html: str, base_url: str) -> MetricsDict: ...

\# ai.py

def analyse(metrics: MetricsDict) -> InsightsDict: ...

def \_build_system_prompt() -> str: ...

def \_build_user_prompt(metrics: MetricsDict) -> str: ...

def \_call_api(system: str, user: str) -> str: ...

def \_parse_response(raw: str) -> InsightsDict: ...

def \_write_log(system: str, user: str, raw: str, metrics: MetricsDict) -> None: ...

\# app.py

def main(url: str) -> None: ...

def \_display(metrics: MetricsDict, insights: InsightsDict) -> None: ...

# **3\. Metrics → Prompt Pipeline**

Exactly how the MetricsDict is transformed into the two prompts. This is the most critical section - it determines whether AI output is grounded or generic.

## **3.1 System Prompt - Static**

Does not change between runs. Defines role, grounding rule, and output format constraint.

SYSTEM_PROMPT = """

You are a senior web marketing analyst specialising in SEO, conversion rate

optimisation, and content clarity for B2B marketing websites.

You will receive:

1\. Structured factual metrics extracted from a webpage.

2\. A snippet of visible page text.

RULES - you must follow all of these:

\- Every insight MUST cite a specific metric value by name and number.

\- Do NOT make observations that are not supported by the provided data.

\- Do NOT give generic advice (e.g. 'improve your meta description').

Instead: 'Your meta description is 12 chars - well below the 150 minimum.'

\- Output ONLY valid JSON. No markdown. No explanation. No preamble.

\- Follow the exact JSON schema provided.

"""

## **3.2 User Prompt - Dynamic (metrics injected)**

The MetricsDict is serialised field-by-field into a readable template. Not dumped as raw JSON - formatted for readability so the model can reason clearly.

def \_build_user_prompt(metrics: MetricsDict) -> str:

cta_list = ', '.join(metrics\['cta_texts'\]\[:5\]) or 'none detected'

h1_list = ', '.join(metrics\['h1_texts'\]\[:3\]) or 'none detected'

return f'''

FACTUAL METRICS - cite these by name in every insight:

word_count: {metrics\['word_count'\]}

h1_count: {metrics\['h1_count'\]} (text: {h1_list})

h2_count: {metrics\['h2_count'\]}

h3_count: {metrics\['h3_count'\]}

cta_count: {metrics\['cta_count'\]} (text: {cta_list})

internal_links: {metrics\['internal_links'\]}

external_links: {metrics\['external_links'\]}

image_count: {metrics\['image_count'\]}

missing_alt_pct: {metrics\['missing_alt_pct'\]:.1f}%

meta_title: '{metrics\['meta_title'\]}' ({metrics\['meta_title_len'\]} chars)

meta_description: '{metrics\['meta_description'\]}' ({metrics\['meta_desc_len'\]} chars)

PAGE TEXT SNIPPET:

{metrics\['page_text_snippet'\]}

Return ONLY this JSON structure, no other text:

{{

"seo_analysis": "...",

"messaging_clarity": "...",

"cta_usage": "...",

"content_depth": "...",

"ux_concerns": "...",

"recommendations": \[

{{"priority": 1, "action": "...", "reasoning": "..."}},

{{"priority": 2, "action": "...", "reasoning": "..."}},

{{"priority": 3, "action": "...", "reasoning": "..."}}

\]

}}

'''

## **3.3 Grounding Enforcement**

Three mechanisms work together to prevent the AI from generating generic or hallucinated output:

| **Mechanism**                 | **What it does**                                                  | **Why it matters**                                                                          |
| ----------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| System prompt rule            | Instructs model to cite metric names and values in every sentence | Model cannot write 'consider improving your CTAs' - must say 'with only 2 CTAs detected...' |
| Metrics passed by name        | Each metric is labelled in the prompt (not buried in JSON blob)   | Model reasons field-by-field, not from raw data dump                                        |
| h1_texts + cta_texts included | Actual heading and CTA copy passed as strings                     | Enables insights like 'Your H1 reads X - does not communicate value proposition'            |

# **4\. Playwright Fallback Logic - Decision Tree**

| **START \_fetch(url) called**<br><br>requests.get(url, headers={'User-Agent': CHROME_UA}, timeout=15)                                                                                                                                                  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **▼**                                                                                                                                                                                                                                                  |
| **◆ DECISION Did requests.get() raise an exception? (Timeout, ConnectionError, etc.)**<br><br>YES → do NOT fall back to Playwright - it won't help with network errors → raise FetchError<br><br>NO → HTTP response received - check status code       |
| **▼**                                                                                                                                                                                                                                                  |
| **◆ DECISION Is HTTP status code 200?**<br><br>YES → parse HTML with BeautifulSoup → count words in soup.get_text()<br><br>NO → status 4xx/5xx → raise FetchError('HTTP {status_code}') - do not fall back                                             |
| **▼**                                                                                                                                                                                                                                                  |
| **◆ DECISION Is word count from parsed HTML > 100?**<br><br>YES → page has real content → proceed with \_extract(html, base_url)<br><br>NO → < 100 words - page is likely JS-rendered → trigger Playwright fallback                                    |
| **▼**                                                                                                                                                                                                                                                  |
| **FALLBACK \_fetch_playwright(url) called**<br><br>Launches headless Chromium. Navigates to URL. Waits for networkidle (max 15s). Returns page.content().<br><br>_Sets metrics\['fetch_method'\] = 'playwright' so evaluator can see it was triggered_ |
| **▼**                                                                                                                                                                                                                                                  |
| **◆ DECISION Did Playwright return HTML with > 100 words?**<br><br>YES → proceed with \_extract(html, base_url) - same function as static path<br><br>NO → return MetricsDict with error='Could not extract meaningful content' and all counts = 0     |

**Playwright not installed:**

Playwright is imported inside \_fetch_playwright() with a try/except ImportError.

If Playwright is not installed, the system catches the error and returns MetricsDict

with fetch_method='requests' and error='Playwright not available - install with: playwright install chromium'.

This prevents a hard crash and surfaces a clear message.

## **4.1 CHROME_UA Header**

Many sites block Python's default User-Agent. Always set this:

CHROME_UA = (

'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '

'AppleWebKit/537.36 (KHTML, like Gecko) '

'Chrome/120.0.0.0 Safari/537.36'

)

response = requests.get(url, headers={'User-Agent': CHROME_UA}, timeout=15)

# **5\. Error Handling Flow**

Every failure mode, what the system returns, and whether it retries. The tool never crashes - it always returns a structured response.

## **5.1 Scraping Layer Errors**

| **Error**                     | **System action**                                               | **Returns**                                      |
| ----------------------------- | --------------------------------------------------------------- | ------------------------------------------------ |
| Invalid URL format            | Validate in app.py before calling scraper. print() + exit(1)    | Exit - no dict returned                          |
| requests timeout (>15s)       | Catch requests.Timeout. No retry. Raise FetchError.             | MetricsDict with error='Fetch timeout after 15s' |
| Connection refused / DNS fail | Catch requests.ConnectionError. No retry.                       | MetricsDict with error='Could not reach URL'     |
| HTTP 4xx / 5xx                | Catch non-200 status. No Playwright fallback for server errors. | MetricsDict with error='HTTP {code}'             |
| < 100 words (JS page)         | Auto-trigger Playwright. No user notification.                  | MetricsDict with fetch_method='playwright'       |
| Playwright import fails       | Catch ImportError inside \_fetch_playwright()                   | MetricsDict with error note, counts = 0          |
| BeautifulSoup parse error     | Catch Exception in \_extract(). Return safe defaults.           | MetricsDict with all counts = 0, error set       |
| Missing meta tags             | Default to '' and 0. Not an error - expected.                   | Normal MetricsDict, metric = '' or 0             |
| Zero images (div by zero)     | Guard: missing_alt_pct = 0.0 if image_count == 0                | Normal MetricsDict                               |

## **5.2 AI Layer Errors**

| **Error**                  | **System action**                                                   | **Returns**                                       |
| -------------------------- | ------------------------------------------------------------------- | ------------------------------------------------- |
| API key not set            | Raise ValueError at module load time with clear message             | Exit before any scraping runs                     |
| API timeout (>30s)         | Catch requests.Timeout / httpx.TimeoutException. No retry.          | InsightsDict with error='API timeout'             |
| HTTP 429 rate limit        | Wait 5s. Retry once. If still 429, return error dict.               | InsightsDict with error='Rate limited'            |
| Response not valid JSON    | Strip \`\`\`json fences. Try json.loads(). On failure → error dict. | InsightsDict with error='Invalid JSON response'   |
| JSON missing required keys | Check all 6 required keys. If any missing → error dict.             | InsightsDict with error='Incomplete AI response'  |
| API 500 server error       | No retry. Return error dict.                                        | InsightsDict with error='Gemini API error {code}' |

**Error display rule:**

app.py checks insights\['error'\] before rendering.

If error is not None: print the factual metrics (always available), then print

the error message in place of AI insights. Never skip rendering metrics - they

are always available regardless of AI failure.

# **6\. Output Layer Design - CLI**

Exact format for the CLI output. Metrics and AI insights are visually separated with clear headers. Never mixed.

## **6.1 CLI Output Structure**

╔══════════════════════════════════════════════════════════════╗

║ WEBSITE AUDIT - FACTUAL METRICS ║

╚══════════════════════════════════════════════════════════════╝

URL: <https://example.com/services>

Fetch method: requests (static HTML)

Content

Word count 1,243

H1 / H2 / H3 1 / 4 / 6

H1 text 'What We Do'

Conversion

CTAs 2 ('Get Started', 'Contact Us')

Internal links 14

External links 3

SEO

Meta title 'Example Page Title' (28 chars) \[optimal: 50-60\]

Meta description 'Short desc.' (12 chars) \[⚠ too short: min 150\]

Media

Images 8 | Missing alt text: 37.5% (3 of 8) \[⚠\]

══════════════════════════════════════════════════════════════

AI INSIGHTS

══════════════════════════════════════════════════════════════

SEO Structure

With 1 H1 ('What We Do') and a meta description of 12 chars -

far below the 150-char minimum - search engines have minimal

snippet content to display. The meta title at 28 chars is also

under the 50-char optimal range.

Messaging Clarity

The sole H1 ('What We Do') does not communicate a value

proposition. Combined with 1,243 words and 4 H2s, the content

has depth but lacks a clear entry-point headline.

\[... other insight sections ...\]

══════════════════════════════════════════════════════════════

RECOMMENDATIONS (PRIORITISED)

══════════════════════════════════════════════════════════════

\[1\] Expand meta description to 150-160 chars

Reason: Currently 12 chars - provides no search snippet value.

\[2\] Add alt text to 3 images (37.5% missing)

Reason: Accessibility and image SEO impact.

\[3\] Rewrite H1 to communicate value proposition

Reason: 'What We Do' does not differentiate or convert.

## **6.2 Warning Thresholds (built into display layer)**

| **Metric**      | **Warning condition**                                           |
| --------------- | --------------------------------------------------------------- |
| meta_title_len  | &lt; 30 or &gt; 65 → show \[⚠ too short\] or \[⚠ too long\]     |
| meta_desc_len   | &lt; 120 or &gt; 165 → show \[⚠\] with note                     |
| missing_alt_pct | \> 0% → show \[⚠\]                                              |
| cta_count       | \== 0 → show \[⚠ no CTAs detected\]                             |
| h1_count        | \== 0 → show \[⚠ no H1 found\] \| > 1 → show \[⚠ multiple H1s\] |
| word_count      | < 300 → show \[⚠ thin content\]                                 |

# **7\. Prompt Logging Design**

## **7.1 When logs are written**

**Timing rule:**

Logging happens inside ai.\_write_log() - called at the END of ai.analyse(),

after the API call completes (success or failure). It is ALWAYS called.

A failed API call still gets logged - the raw_response field will contain

the error or empty string, and parsed_status will be 'error'.

## **7.2 Log file location and naming**

\# File: prompt_logs/run.md

\# Mode: append - multiple runs accumulate in the same file

\# Created automatically if not exists

os.makedirs('prompt_logs', exist_ok=True)

with open('prompt_logs/run.md', 'a', encoding='utf-8') as f:

f.write(log_entry)

## **7.3 Log entry format**

\---

\## Run - 2026-03-25 14:32:01 UTC

\*\*URL:\*\* <https://example.com/services>

\*\*Fetch method:\*\* requests

\*\*Parsed status:\*\* success # or: error - Invalid JSON response

\### Design Decisions

\- Metrics are passed field-by-field (not raw JSON dump) so the model

reasons from labelled values, reducing hallucination risk.

\- System prompt explicitly requires metric citation in every insight.

\- Output constrained to JSON schema - no prose allowed.

\### System Prompt

\[full system prompt text here\]

\### User Prompt (values injected)

\[full user prompt with actual metric values filled in\]

\### Raw API Response

\[raw string returned by Gemini, before any processing\]

\### Parsed Output

\[final InsightsDict as pretty-printed JSON, or error message\]

\---

# **8\. Complete Flow Diagram**

Full system including all decision branches and error paths. Read top to bottom.

INPUT

URL (string)

│

▼

app.py - validate URL

│

├── INVALID ──────────────────────────────► print error + exit(1)

│

▼

scraper.scrape(url)

│

▼

\_fetch(url) \[requests + CHROME_UA, timeout=15s\]

│

├── ConnectionError / Timeout ────────────► MetricsDict(error='...')

├── HTTP 4xx / 5xx ──────────────────────► MetricsDict(error='HTTP {code}')

│

▼

word_count > 100?

│

├── NO ──► \_fetch_playwright(url)

│ │

│ ├── ImportError ──────────► MetricsDict(error='Playwright not installed')

│ ├── Still < 100 words ────► MetricsDict(error='Could not extract content')

│ └── OK ──────────────────► HTML (fetch_method='playwright')

│

▼ (YES or Playwright OK)

\_extract(html, base_url)

│

├── Parse error ──────────────────────────► MetricsDict(all counts=0, error='...')

│

▼

MetricsDict (all 14 fields populated)

│

▼

app.py → ai.analyse(metrics)

│

▼

\_build_system_prompt() \[static\]

\_build_user_prompt(metrics) \[metrics injected field-by-field\]

│

▼

\_call_api(system, user) \[Gemini, timeout=30s\]

│

├── Timeout ────────────────────────────► InsightsDict(error='API timeout')

├── HTTP 429 ── wait 5s ── retry once

│ └── Still 429 ──────────────────► InsightsDict(error='Rate limited')

├── HTTP 5xx ───────────────────────────► InsightsDict(error='Gemini API error')

│

▼

\_parse_response(raw)

│

├── Not JSON ── strip fences ── retry

│ └── Still invalid ──────────────► InsightsDict(error='Invalid JSON')

├── Missing keys ───────────────────────► InsightsDict(error='Incomplete response')

│

▼

InsightsDict (all 6 fields populated)

│

▼

\_write_log() \[ALWAYS runs - success or error\]

│ Appends to prompt_logs/run.md

│

▼

app.py → \_display(metrics, insights)

│

├── metrics\['error'\] → print metrics only + error message

├── insights\['error'\] → print full metrics + error in AI section

└── No errors → print full output (metrics + insights + recommendations)

│

▼

DONE

# **9\. Quick Reference Card**

**CONTRACTS**

scraper.scrape(url: str) → MetricsDict # 14 fields, always complete

ai.analyse(metrics: MetricsDict) → InsightsDict # 6 fields + error key

**PLAYWRIGHT TRIGGER**

requests succeeds + word_count < 100 → fallback (not on network errors)

**PROMPT GROUNDING**

Metrics injected field-by-field with labels (not raw JSON dump)

System prompt explicitly requires metric citation in every insight sentence

**ERROR RULE**

Never crash. Every error path returns a typed dict with error key set.

Metrics are always rendered - even when AI layer fails.

**LOGGING RULE**

\_write_log() called at end of ai.analyse() - always, success or error.

Appends to prompt_logs/run.md. Includes: url, timestamp, both prompts, raw response, parse status.