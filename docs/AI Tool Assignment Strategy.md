# AI Tool Assignment Strategy

#### AI-Native Software Engineer v2.pdf

#### PDF

#### Assignment_Manual.docx

#### Document

#### Architecture_Workflow_v2.docx

#### Document

#### GPT Audit workflow improvments.pdf

#### PDF

#### hi i have been given an assignemt from a comapny its to make an Ai tool... i want this chat to be

#### used professionaly in a way to help me not only propely submit this assigment. but also mak esure

#### i get selected form the 100s of people whome were given the same assement.

#### what makes my submison diff from them..

#### The resources given to you are the:

#### Actualy assesment pdf with the task

#### an assement manual from cluad used as a refercne guide

#### the Proper Workflow architercture from claud.

#### and an enhancemnt docuemnt to addon to the workflow architecture to improve resutls.

#### below is ur context prompt

#### You are a senior Python engineer helping me set up a clean, production-quality workspace for an

#### AI-native CLI tool.

#### I already have:

#### * A full architecture spec (scraper / ai / app separation)

#### * Defined data contracts (MetricsDict, InsightsDict)

#### * Prompt logging system

#### * Playwright fallback

#### * CLI output layer

#### Your job is to generate a **clean, ready-to-code project setup** that strictly follows this

#### architecture.

#### ---

#### ## REQUIREMENTS

#### ### 1. PROJECT STRUCTURE

#### Create a professional folder structure:

#### * modular (scraper, ai, app clearly separated)


#### * includes logs, output, config

#### * ready for scaling

#### ---

#### ### 2. FILE STRUCTURE (VERY IMPORTANT)

#### List ALL files with purpose:

#### * scraper.py

#### * ai.py

#### * app.py

#### * display.py (if needed)

#### * utils.py (optional)

#### * config.py (for constants like UA, thresholds)

#### Also include:

#### * prompt_logs/

#### * output/

#### * .env

#### * .env.example

#### * requirements.txt

#### * README.md

#### ---

#### ### 3. ENVIRONMENT SETUP

#### Provide exact steps:

#### * venv creation

#### * dependency installation

#### * Playwright install

#### * .env usage

#### * API key setup

#### Make it copy-paste friendly.

#### ---

#### ### 4. REQUIREMENTS.TXT

#### List all dependencies cleanly:

#### * requests

#### * beautifulsoup

#### * playwright

#### * python-dotenv

#### * google-generativeai (or equivalent)


#### ---

#### ### 5. BASE CODE SCAFFOLDING

#### Generate minimal starter code for:

#### * scraper.py (function signatures only)

#### * ai.py (prompt + API structure)

#### * app.py (main flow)

#### * logging setup

#### NO full implementation — just clean structure and function skeletons.

#### ---

#### ### 6. CONFIG DESIGN

#### Define:

#### * constants (timeouts, thresholds)

#### * user-agent string

#### * retry limits

#### ---

#### ### 7. RUN INSTRUCTIONS

#### Show exactly how to run:

#### python app.py https://example.com

#### ---

#### ## IMPORTANT

#### * Follow the architecture strictly (no mixing scraper + AI)

#### * Keep everything clean and modular

#### * No overengineering

#### * No unnecessary frameworks

#### * Think like a real backend engineer, not a tutorial

#### This setup will be used directly in an assignment submission.

#### Understood. I’ll treat this as a serious submission strategy chat from here onward.

#### You are not trying to merely “finish the assignment.” You are trying to make your submission look like it

#### was built by someone who already thinks like an engineer they would trust on a real internal AI tool.


#### Based on the actual assignment, the evaluators are not mainly testing scraping difficulty. They are

#### testing whether you can build a small AI system with clean separation, grounded reasoning, structured

#### outputs, and practical trade-off awareness. The assignment explicitly emphasizes clean separation

#### between scraping and AI analysis, structured outputs, prompt design quality, and practical usefulness to

#### a web agency.

```
AI-Native Software Engineer v
```
#### What will make your submission different from the other 100 candidates is not “more features.” It is this:

#### Most candidates will build a scraper with an API call.

#### You need to build a small, disciplined AI system.

#### That means your submission should visibly show five things.

#### First, strict architecture discipline.

#### Your files must clearly separate responsibilities: scraper extracts facts, ai module builds prompts and

#### returns structured insights, app orchestrates, display renders. No cross-contamination. This is directly

#### aligned with both the manual and the workflow spec.

#### Second, grounded AI instead of fluffy AI.

#### Your AI output must visibly reference real metrics like word count, CTA count, H1 text, meta description

#### length, missing alt percentage. That is the biggest differentiator the manual calls out: candidates who

#### pass structured metrics into AI and force grounded reasoning beat candidates who dump raw HTML and

#### hope for magic.

```
Assignment_Manual
```
#### Third, structured output quality.

#### Do not let the AI return loose prose. It should return a predictable JSON-style insights structure that can

#### be validated, logged, displayed, and exported. The architecture spec is very strong on this.

Architecture_Workflow_v

#### Fourth, engineering maturity around failure cases.

#### Most candidates will ignore JS-rendered pages, invalid JSON responses, missing API keys, and fallback

#### behavior. Your docs already point to a stronger approach: requests first, Playwright fallback when static

#### content is too thin, parse validation, graceful error handling, and prompt logging that always runs.

#### Fifth, clarity of thinking in the README and prompt logs.

#### A strong evaluator will often decide from your README whether you “get it.” The assignment explicitly

#### asks for architecture overview, AI design decisions, trade-offs, and what you would improve with more

#### time. If your README explains why metrics are passed before text, why JSON output is requested, why

#### Playwright is only a fallback, and what limitations remain, you will look much stronger than someone

#### who just says “used BeautifulSoup and Gemini.”

#### So, in practical terms, your submission should feel like this :

#### A reviewer clones it, installs it, runs one command, sees clear factual metrics separated from AI insights,

#### sees recommendations tied to numbers, sees prompt logs, sees that the tool handles modern sites, and

#### sees a README written by someone who understands AI orchestration rather than someone who just

#### called an LLM.

#### That is what makes it different.

#### Here is the standard I recommend for your final submission:

#### Tier 1 — must be excellent

#### Clean modular file structure


#### Clear CLI output

#### Strong prompt design

#### Prompt logs included

#### README written professionally

#### Works reliably on a few real URLs

#### Tier 2 — your differentiators

#### Playwright fallback

#### AI response validation

#### One controlled retry if AI output is weak/invalid

#### Derived features such as thin-content or SEO-risk flags before prompting

#### Export to output/latest.json and output/latest.txt

#### Execution logging like fetch method, retry count, elapsed time

#### Those “enhancement” ideas are exactly the kind of things that elevate the system from assignment-level

#### to production-aware without bloating it.

```
GPT Audit workflow improvments
```
#### My recommendation is that we use this chat in a very deliberate way:

#### 1. We lock the submission strategy first.

#### 2. We generate the exact project workspace and starter scaffold.

#### 3. We design the README so it sounds like a strong engineer wrote it.

#### 4. We design the prompt logs and output examples.

#### 5. We refine the “why this is better than other submissions” narrative for interview/review.

#### The context prompt you gave is good, but I would tighten the goal slightly:

#### You are not just asking for “clean ready-to-code setup.”

#### You are asking for a submission-ready workspace that maximizes evaluator confidence.

#### So from this point, I’ll help you optimize for:

#### correctness,

#### professionalism,

#### evaluator psychology,

#### and differentiation.

#### Your real edge will be this sentence:

#### This submission does not present AI as a magic summarizer. It treats AI as a constrained,

#### observable, grounded system component.

#### That is the hiring signal.

#### Next, I can turn your context prompt into a sharper master prompt that you can feed into GPT to

#### generate the actual workspace and scaffolding with a much better chance of getting high-quality


#### output.

**Sources**

#### This makes sense — I think we’re aligned on the overall approach now.

#### At this point, I want to move from strategy into implementation. The architecture and workflow are

#### already defined, so the next step is to set up a clean, build-ready workspace.

#### Can you now help with a more concrete setup, specifically:

#### * Project folder structure

#### * Exact terminal commands for environment setup (venv, installs, Playwright)

#### * requirements.txt

#### * .env.example

#### * Starter file skeletons (scraper.py, ai.py, app.py, etc.)

#### * Run instructions

#### * Any setup notes for Playwright

#### The goal here is to create a minimal but solid scaffold so I can start implementing module by

#### module without ambiguity.

#### From here, I’ll follow this sequence:

#### 1. Docs locked

#### 2. Env/workspace scaffold

#### 3. Minimal starter files

#### 4. Implement module by module

#### 5. README + final polish

#### Let’s focus on making the setup clean, modular, and directly aligned with the architecture.

#### Yes. Here is a clean scaffold that stays aligned with the assignment and your architecture docs: strict

#### scraper.py / ai.py / app.py separation, factual metrics rendered separately from AI insights, prompt

#### logging, Playwright fallback, and a simple CLI entrypoint.

## Recommended project structure


website-audit-tool/
│
├── app.py
├── scraper.py
├── ai.py
├── display.py
├── config.py
├── utils.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── prompt_logs/
│ └── .gitkeep
│
└── output/
└── .gitkeep

### File purpose

#### app.py — CLI entrypoint; validates URL, calls scraper, calls AI, renders output, writes exports.

#### scraper.py — fetches HTML, runs requests-first logic, triggers Playwright fallback when content is

#### too thin, extracts factual metrics only. It must not call AI.

#### ai.py — builds prompts, calls Gemini, parses/validates JSON, writes prompt logs. It must not scrape

#### or parse HTML.

#### display.py — CLI rendering so app.py stays thin.

#### config.py — constants like timeouts, retry count, thresholds, model name, User-Agent.

#### utils.py — optional shared helpers like timestamping, JSON writing, URL normalization.

#### prompt_logs/ — required deliverable area for prompts, raw responses, and reasoning traces.

#### output/ — optional but strong addition for latest.json and latest.txt, which your enhancement

#### doc recommends.

```
GPT Audit workflow improvments
```
## Exact terminal setup

### Windows PowerShell

mkdir **_website-audit-tool_**
cd **_website-audit-tool_**

**_python_** - **_m venv_**. **_venv_**

. **_venv_** \ **_Scripts_** \ **_Activate_**. **_ps_**

**_python_** - **_m pip install_** -- **_upgrade pip
pip install_** - r **_requirements_**. **_txt_**

**_playwright install chromium_**

### macOS / Linux


mkdir website-audit-tool
cd website-audit-tool

python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt

playwright install chromium

### If you are creating the files from zero first

mkdir prompt_logs output
touch app.py scraper.py ai.py display.py config.py utils.py README.md requirements.txt .env.example .g

#### On Windows PowerShell:

mkdir **_prompt_logs_** , **_output_**
ni **_app_**. **_py_** , **_scraper_**. **_py_** , **_ai_**. **_py_** , **_display_**. **_py_** , **_config_**. **_py_** , **_utils_**. **_py_** , **_README_** .md, **_requirements_**. **_txt_** ,. **_env_**. **_examp_**

#### The docs explicitly support requests, beautifulsoup4, playwright, python-dotenv, and google-generativeai,

#### and recommend playwright install chromium for JS-rendered pages.

### requirements.txt

requests
beautifulsoup
playwright
python-dotenv
google-generativeai

#### This matches the dependency list called out in the manual.

```
Assignment_Manual
```
### .env.example

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash

#### The manual specifically recommends Gemini and the workflow uses gemini-1.5-flash in the AI call path.

### .gitignore

.venv/
__pycache__/
*.pyc
.env
prompt_logs/*.md
output/*.json
output/*.txt

#### You should definitely ignore .env, and the manual explicitly says .gitignore must include .env and

#### __pycache__.

```
Assignment_Manual
```
### config.py


"""Central configuration for the website audit tool."""

from **___future___** import **_annotations_**

import **_os_**
from **_dotenv_** import **_load_dotenv_**

**_load_dotenv_** ()

**_CHROME_UA_** = (
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
"AppleWebKit/537.36 (KHTML, like Gecko) "
"Chrome/120.0.0.0 Safari/537.36"
)

**_REQUEST_TIMEOUT_SECONDS_** = 15
**_PLAYWRIGHT_TIMEOUT_MS_** = 15_
**_AI_TIMEOUT_SECONDS_** = 30
**_AI_RETRY_LIMIT_** = 1
**_PLAYWRIGHT_TRIGGER_WORD_COUNT_** = 100
**_PAGE_TEXT_SNIPPET_CHARS_** = 1000

**_GEMINI_MODEL_** = **_os_** .getenv("GEMINI_MODEL", "gemini-1.5-flash")
**_GEMINI_API_KEY_** = **_os_** .getenv("GEMINI_API_KEY", "")

#### These values align with the workflow spec: 15s fetch timeout, 30s AI timeout, one retry on some AI

#### failures, and Playwright fallback when parsed content is under 100 words. The Chrome-style User-Agent

#### is also explicitly recommended.

### utils.py

"""Shared utility helpers."""

from **___future___** import **_annotations_**

import **_json_**
from **_datetime_** import **_datetime_** , **_timezone_**
from **_pathlib_** import **_Path_**
from **_typing_** import **_Any_**

def **_utc_timestamp_** () -> **_str_** :
"""Return an ISO 8601 UTC timestamp."""
return **_datetime_** .now( **_timezone_** .utc).isoformat()

def **_ensure_dir_** ( **_path_** : **_str_** | **_Path_** ) -> **_Path_** :
"""Create a directory if it does not exist."""
**_p_** = **_Path_** ( **_path_** )
**_p_** .mkdir( **_parents_** =True, **_exist_ok_** =True)
return **_p_**

def **_write_json_** ( **_path_** : **_str_** | **_Path_** , **_payload_** : **_dict_** [ **_str_** , **_Any_** ]) -> None:
"""Write a JSON file with stable formatting."""
**_Path_** ( **_path_** ).write_text( **_json_** .dumps( **_payload_** , **_indent_** = 2 , **_ensure_ascii_** =False), **_encoding_** ="utf-8")

def **_write_text_** ( **_path_** : **_str_** | **_Path_** , **_content_** : **_str_** ) -> None:
"""Write plain text content to a file."""
**_Path_** ( **_path_** ).write_text( **_content_** , **_encoding_** ="utf-8")

### scraper.py


"""HTML fetching and factual metric extraction only."""

from **___future___** import **_annotations_**

from **_typing_** import **_TypedDict_**

class MetricsDict( **_TypedDict_** ):
**_url_** : **_str
fetch_method_** : **_str
word_count_** : **_int
h1_count_** : **_int
h2_count_** : **_int
h3_count_** : **_int
h1_texts_** : **_list_** [ **_str_** ]
**_cta_count_** : **_int
cta_texts_** : **_list_** [ **_str_** ]
**_internal_link_count_** : **_int
external_link_count_** : **_int
image_count_** : **_int
missing_alt_pct_** : **_float
meta_title_** : **_str
meta_title_length_** : **_int
meta_description_** : **_str
meta_description_length_** : **_int
page_text_snippet_** : **_str
error_** : **_str_** | None

class FetchError( **_Exception_** ):
"""Raised when a page cannot be fetched meaningfully."""

def **_scrape_** ( **_url_** : **_str_** ) -> **_MetricsDict_** :
"""Fetch a page and return extracted factual metrics."""
raise **_NotImplementedError_**

def **__fetch_** ( **_url_** : **_str_** ) -> **_str_** :
"""Fetch static HTML via requests with configured headers and timeout."""
raise **_NotImplementedError_**

def **__fetch_playwright_** ( **_url_** : **_str_** ) -> **_str_** :
"""Fetch rendered HTML via Playwright as a JS fallback."""
raise **_NotImplementedError_**

def **__extract_** ( **_html_** : **_str_** , **_base_url_** : **_str_** , **_fetch_method_** : **_str_** ) -> **_MetricsDict_** :
"""Parse HTML and extract all required factual metrics."""
raise **_NotImplementedError_**

def **__count_words_** ( **_text_** : **_str_** ) -> **_int_** :
"""Return total word count for page text."""
raise **_NotImplementedError_**

def **__extract_ctas_** () -> **_tuple_** [ **_int_** , **_list_** [ **_str_** ]]:
"""Extract CTA count and visible CTA texts."""
raise **_NotImplementedError_**

def **__classify_links_** ( **_base_url_** : **_str_** ) -> **_tuple_** [ **_int_** , **_int_** ]:
"""Return internal and external link counts."""
raise **_NotImplementedError_**

def **__safe_empty_metrics_** ( **_url_** : **_str_** , **_error_** : **_str_** , **_fetch_method_** : **_str_** = "requests") -> **_MetricsDict_** :
"""Return a fully populated safe MetricsDict on scraper failure."""
raise **_NotImplementedError_**

#### This keeps scraper.py focused on fetching and factual extraction only, exactly as required. It also leaves

#### room for the requests-first / Playwright-fallback decision tree in the workflow spec.


### ai.py


"""Prompt construction, Gemini call, JSON parsing, and prompt logging."""

from **___future___** import **_annotations_**

from **_typing_** import **_TypedDict_** , **_Any_**

from **_scraper_** import **_MetricsDict_**

class Recommendation( **_TypedDict_** ):
**_priority_** : **_int
action_** : **_str
reasoning_** : **_str_**

class InsightsDict( **_TypedDict_** ):
**_seo_analysis_** : **_str
messaging_clarity_** : **_str
cta_usage_** : **_str
content_depth_** : **_str
ux_concerns_** : **_str
recommendations_** : **_list_** [ **_Recommendation_** ]
**_error_** : **_str_** | None

def **_analyse_** ( **_metrics_** : **_MetricsDict_** ) -> **_InsightsDict_** :
"""Generate structured AI insights from extracted metrics."""
raise **_NotImplementedError_**

def **__build_system_prompt_** () -> **_str_** :
"""Return the static system prompt."""
raise **_NotImplementedError_**

def **__build_user_prompt_** ( **_metrics_** : **_MetricsDict_** ) -> **_str_** :
"""Inject metrics field-by-field into the user prompt."""
raise **_NotImplementedError_**

def **__call_api_** ( **_system_prompt_** : **_str_** , **_user_prompt_** : **_str_** ) -> **_str_** :
"""Call Gemini and return the raw text response."""
raise **_NotImplementedError_**

def **__parse_response_** ( **_raw_response_** : **_str_** ) -> **_InsightsDict_** :
"""Parse, validate, and normalize the model JSON output."""
raise **_NotImplementedError_**

def **__validate_response_** ( **_data_** : **_dict_** [ **_str_** , **_Any_** ]) -> **_bool_** :
"""Check required keys and minimum structural quality."""
raise **_NotImplementedError_**

def **__write_log_** (
*,
**_url_** : **_str_** ,
**_system_prompt_** : **_str_** ,
**_user_prompt_** : **_str_** ,
**_raw_response_** : **_str_** ,
**_parsed_status_** : **_str_** ,
) -> None:
"""Append a prompt log entry for every run."""
raise **_NotImplementedError_**

def **__error_insights_** ( **_message_** : **_str_** ) -> **_InsightsDict_** :
"""Return a safe InsightsDict for AI failures."""
return {
"seo_analysis": "",
"messaging_clarity": "",
"cta_usage": "",
"content_depth": "",
"ux_concerns": "",
i


"recommendations": [],
"error": **_message_** ,
}

#### This follows the documented AI flow: build prompts, call Gemini, parse JSON, validate required keys, and

#### always write a prompt log.

### display.py

"""CLI rendering helpers for metrics and AI output."""

from **___future___** import **_annotations_**

from **_scraper_** import **_MetricsDict_**
from **_ai_** import **_InsightsDict_**

def **_render_** ( **_metrics_** : **_MetricsDict_** , **_insights_** : **_InsightsDict_** ) -> **_str_** :
"""Return the full CLI report as a string."""
raise **_NotImplementedError_**

def **_render_metrics_** ( **_metrics_** : **_MetricsDict_** ) -> **_str_** :
"""Return the factual metrics section."""
raise **_NotImplementedError_**

def **_render_insights_** ( **_insights_** : **_InsightsDict_** ) -> **_str_** :
"""Return the AI insights section."""
raise **_NotImplementedError_**

#### The workflow spec explicitly wants metrics and AI insights visually separated in the CLI output.

### app.py


"""CLI entrypoint for the website audit tool."""

from **___future___** import **_annotations_**

import **_sys_**
from **_urllib_**. **_parse_** import **_urlparse_**

from **_ai_** import **_analyse_**
from **_display_** import **_render_**
from **_scraper_** import **_scrape_**
from **_utils_** import **_ensure_dir_** , **_utc_timestamp_** , **_write_json_** , **_write_text_**

def **_is_valid_url_** ( **_url_** : **_str_** ) -> **_bool_** :
"""Basic validation for http/https URLs."""
**_parsed_** = **_urlparse_** ( **_url_** )
return **_parsed_** .scheme in {"http", "https"} and **_bool_** ( **_parsed_** .netloc)

def **_main_** () -> None:
"""Run the end-to-end audit flow."""
if **_len_** ( **_sys_** .argv) < 2 :
**_print_** ("Usage: python app.py https://example.com")
**_sys_** .exit( 1 )

**_url_** = **_sys_** .argv[ 1 ].strip()

if not **_is_valid_url_** ( **_url_** ):
**_print_** ("Error: please provide a valid http/https URL.")
**_sys_** .exit( 1 )

**_ensure_dir_** ("prompt_logs")
**_ensure_dir_** ("output")

**_metrics_** = **_scrape_** ( **_url_** )
**_insights_** = **_analyse_** ( **_metrics_** ) if not **_metrics_** ["error"] else {
"seo_analysis": "",
"messaging_clarity": "",
"cta_usage": "",
"content_depth": "",
"ux_concerns": "",
"recommendations": [],
"error": "AI analysis skipped because scraping failed.",
}

**_report_** = **_render_** ( **_metrics_** , **_insights_** )
**_print_** ( **_report_** )

**_timestamp_** = **_utc_timestamp_** ()
**_write_json_** (
"output/latest.json",
{
"timestamp": **_timestamp_** ,
"url": **_url_** ,
"metrics": **_metrics_** ,
"insights": **_insights_** ,
},
)
**_write_text_** ("output/latest.txt", **_report_** )

if **___name___** == "__main__":
**_main_** ()

#### This matches the orchestrator role described in the manual and workflow: validate URL, call scraper,

#### pass metrics to AI, render output, and keep business logic minimal. Exporting latest.json and

#### latest.txt is also a strong enhancement.

## Run instructions

#### Once the environment is activated and .env is filled:


python app.py https://example.com

#### That exact local CLI pattern is aligned with the assignment’s allowed interface options.

```
AI-Native Software Engineer v
```
## Playwright setup notes

#### Use this logic and mention it in your README:

#### Try requests first.

#### Parse the returned HTML.

#### If parsed body text is under 100 words, treat it as likely JS-rendered and fall back to Playwright.

#### Do not use Playwright for ordinary network failures or HTTP 4xx/5xx.

#### Import Playwright inside the fallback function so the tool can fail gracefully with a clear message if

#### Playwright is missing.

#### Recommended install command:

playwright install chromium

#### Also use a realistic Chrome User-Agent in the requests fetch path because some sites block Python

#### defaults.

## Minimal implementation order

#### Build it in this order so you do not get lost:

#### 1. config.py

#### 2. scraper.py static fetch + extraction only

#### 3. Playwright fallback in scraper.py

#### 4. display.py

#### 5. ai.py prompt builder

#### 6. ai.py raw Gemini call

#### 7. ai.py JSON parsing + prompt log writing

#### 8. app.py orchestration

#### 9. output/latest.json and output/latest.txt

#### 10. README polish

#### That order fits the architecture and keeps each layer independently testable.

#### The next strongest step is to generate the actual first-pass implementation for scraper.py only, with the

#### requests path, Playwright fallback, and metric extraction done properly.

**Sources**


