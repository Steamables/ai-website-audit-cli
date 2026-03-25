**AI-Native Website Audit Tool**

Assignment Manual - How to Build, What They Want to See

# **1\. What This Assignment Is Really Testing**

The company sends this to everyone they interview. The scraping part is normal - every candidate will do that. What separates you is how you think about the AI layer.

| **What they say they want**              | **What they actually mean**                                            |
| ---------------------------------------- | ---------------------------------------------------------------------- |
| Clean separation between scraping and AI | Two different modules/files - scraper never calls AI, AI never scrapes |
| Structured outputs                       | AI returns JSON, not a paragraph of prose                              |
| Prompt design quality                    | Your prompts are grounded in real metrics, not just 'analyze this'     |
| AI-native thinking                       | You treat AI as a system component, not a magic box                    |
| Practical relevance to a web agency      | Insights actually sound useful to an SEO/CRO team                      |

**Key Insight:** The single biggest differentiator: a candidate who passes structured metrics into the AI and constrains its output beats one who dumps raw HTML and hopes for the best.

# **2\. Architecture Overview**

Three clean modules. Keep them separate - this separation is explicitly evaluated.

| **Module / File** | **Responsibility**                                                  | **What it must NOT do**         |
| ----------------- | ------------------------------------------------------------------- | ------------------------------- |
| scraper.py        | Fetch HTML, extract all factual metrics, return a clean dict/object | Call any AI API                 |
| ai.py             | Build prompts, call the AI API, return structured JSON insights     | Do any scraping or HTML parsing |
| app.py            | Accept URL input, call scraper, pass result to AI, display output   | Contain business logic          |

## **Data Flow**

URL input → scraper.py (metrics dict) → ai.py (structured insights JSON) → app.py (display)

# **3\. What the Scraper Must Extract**

These are required. Display them separately from AI output - the assignment explicitly says this.

| **Metric**                  | **How to extract (BeautifulSoup)**                         |
| --------------------------- | ---------------------------------------------------------- |
| Total word count            | soup.get_text() → split → len()                            |
| H1, H2, H3 counts           | len(soup.find_all('h1')), h2, h3                           |
| Number of CTAs              | find_all('button') + &lt;a&gt; tags with CTA-like text     |
| Internal vs external links  | Check href - same domain = internal, else external         |
| Image count + % missing alt | find_all('img') → check alt attr → calculate %             |
| Meta title & description    | find('title') + find('meta', attrs={'name':'description'}) |

## **Handling JS-Rendered Pages (Important Tradeoff)**

Most modern marketing websites are React/Vue. Plain requests + BeautifulSoup will return empty HTML on these.

**Recommended Approach:** Strategy: Try requests first. If word count < 100, fall back to Playwright to render the JS. Mention this in your README - it shows awareness.

Files you'll need for scraping:

- requests - HTTP fetching
- beautifulsoup4 - HTML parsing
- playwright - JS rendering fallback (install with: playwright install chromium)
- urllib.parse - for internal vs external link detection

# **4\. The AI Layer - The Most Important Part**

## **Which API to Use**

Use Google Gemini (gemini-1.5-flash). It's free, no credit card required, and generous enough for this project. The evaluators will run your repo - a paid key creates friction.

**Note:** Which API you pick does NOT matter. How you call it does. A well-structured Gemini call beats a sloppy GPT-4 call every time for this assignment.

## **How to Structure the AI Call - BAD vs GOOD**

| **BAD - what most candidates will do**                                                                                        | **GOOD - what will impress them**                                                                                                                                                   |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| prompt = f"Here is the HTML: {raw_html}. Analyze it."<br><br>AI hallucinates, outputs ungrounded prose, not tied to real data | Pass metrics dict + page text separately. Tell the AI to reference specific numbers in every insight.<br><br>AI output says 'with 0 CTAs found...' - grounded, specific, impressive |

## **System Prompt Structure**

This is the most important thing to get right. Here is a template:

You are a senior web marketing analyst specialising in SEO, conversion rate optimisation, and content strategy for B2B marketing websites. You will be given: 1. Factual metrics extracted from a webpage 2. A summary of the page content Your job is to produce a structured analysis grounded strictly in the metrics provided. Every insight MUST reference specific numbers from the metrics. Do not make generic recommendations. Return your response as valid JSON only, with this exact structure: { "seo_analysis": "...", "messaging_clarity": "...", "cta_usage": "...", "content_depth": "...", "ux_concerns": "...", "recommendations": \[ {"priority": 1, "action": "...", "reasoning": "..."}, ... \] }

## **User Prompt Structure**

Pass the metrics as structured data, not as prose:

FACTUAL METRICS: - Word count: {word_count} - H1 count: {h1}, H2: {h2}, H3: {h3} - CTAs found: {cta_count} - Internal links: {internal_links}, External: {external_links} - Images: {image_count}, Missing alt text: {missing_alt}% - Meta title: "{meta_title}" ({meta_title_length} chars) - Meta description: "{meta_desc}" ({meta_desc_length} chars) PAGE CONTENT SUMMARY: {first_1000_chars_of_body_text} Analyse this page and return the JSON structure specified.

**Why this matters:** Why this works: The AI cannot hallucinate metrics it was explicitly given. It is forced to reason from real data. This is what 'grounded in extracted metrics' means.

# **5\. Prompt Logs - Don't Treat This as an Afterthought**

Prompt logs are a required deliverable. Most candidates will log them as an afterthought. Treat them as part of your submission.

Your prompt log file should include, for each run:

- The system prompt used
- The exact user prompt sent (with real values filled in)
- The raw API response before any formatting
- Any decisions you made about prompt design and why

Save this as a file: prompt_logs/example_run.md or prompt_logs/example_run.json

**Pro tip:** If the evaluator reads your prompt log and can see your reasoning - why you structured the system prompt the way you did, why you pass metrics separately from content - that is rare and impressive.

# **6\. Code Quality Standards**

## **What to Follow**

- PEP 8
- Type hints
- Docstrings
- Error handling
- No hardcoded secrets

## **What NOT to Worry About**

- Fancy UI - a clean terminal output or simple Flask page is fine
- Test coverage - unit tests are a bonus, not required
- Performance optimisation - this is a single-page tool
- Dockerisation - unless you enjoy it

# **7\. Files You'll Need**

| **File**                   | **Purpose**                                                                         |
| -------------------------- | ----------------------------------------------------------------------------------- |
| scraper.py                 | All HTML fetching and metric extraction logic                                       |
| ai.py                      | Prompt building, API call, JSON parsing                                             |
| app.py                     | Entry point - ties everything together, handles UI/output                           |
| .env                       | API key storage (never commit this to GitHub)                                       |
| .env.example               | Template showing what keys are needed - DO commit this                              |
| requirements.txt           | Python dependencies (requests, bs4, playwright, python-dotenv, google-generativeai) |
| README.md                  | Architecture, AI design decisions, tradeoffs, what you'd improve                    |
| prompt_logs/example_run.md | Your required prompt log deliverable                                                |
| .gitignore                 | Must include .env and \_\_pycache\_\_                                               |

# **8\. The README - Don't Underestimate It**

The README is a deliverable with specific sections they want. Treat each one seriously.

### **Architecture Overview**

Describe the three-module structure. One paragraph. Include the data flow arrow diagram.

### **AI Design Decisions**

This is where you explain WHY you structured your prompts the way you did. Examples of things to write:

- "I pass metrics as structured data before page content so the AI is anchored to real numbers before reading prose."
- "I use a system prompt that constrains the AI to reference specific metrics - this prevents generic outputs."
- "I request JSON output directly to make the AI layer composable and testable."

### **Trade-offs**

Write 3-4 honest tradeoffs. Examples:

- "Used Playwright as JS fallback - adds install complexity but handles modern marketing sites correctly."
- "Used Gemini Free tier - limits to 250 req/day but removes the need for a paid key during review."
- "Single-page analysis only - multi-page crawling would require a queue system out of scope here."

### **What I'd Improve With More Time**

- Caching scraped results to avoid re-fetching
- A confidence score on AI insights
- A web UI with side-by-side metrics and insights panels
- Support for authenticated pages

# **9\. Quick Checklist Before Submitting**

| **✓** | scraper.py and ai.py are completely separate - no cross-contamination |
| ----- | --------------------------------------------------------------------- |
| **✓** | Factual metrics display separately from AI insights in the output     |
| **✓** | AI insights reference specific numbers (not generic advice)           |
| **✓** | AI output is structured JSON, not a prose paragraph                   |
| **✓** | Prompt logs saved as a real file in the repo                          |
| **✓** | README covers all 4 required sections                                 |
| **✓** | .env.example committed, .env gitignored                               |
| **✓** | Tool works on at least 3 different URLs (test this yourself)          |
| **✓** | JS-heavy pages handled or acknowledged in README tradeoffs            |
| **✓** | No API keys hardcoded anywhere in the code                            |
| **✓** | requirements.txt is up to date                                        |

**Final reminder:** You don't need to build something fancy. You need to build something that shows you understand AI as a system - structured inputs, grounded outputs, clean separation, and honest reasoning. That's what gets you hired.