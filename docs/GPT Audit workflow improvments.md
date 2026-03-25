

 AI-Native System Enhancements &
## Engineering Considerations
## 1. Introduction
This document outlines additional engineering considerations and enhancements beyond the
core architecture. While the primary system satisfies all assignment requirements, the following
improvements demonstrate deeper AI-native system design thinking, focusing on robustness,
extensibility, and intelligent AI usage.

- AI Output Validation & Feedback Loop
## 2.1 Problem
The current system uses a single-pass AI inference:
metrics → prompt → AI → output

This approach assumes the model always produces high-quality, grounded output, which may
not hold in edge cases.

## 2.2 Enhancement: Validation Layer
A lightweight validation layer is introduced after AI response parsing.
## Validation Checks:
● Ensure all required fields are present
● Verify each insight references at least one metric
● Check minimum length/quality of responses
● Ensure recommendations are actionable (not generic)

## 2.3 Retry Strategy

If validation fails:
IF response_invalid:
modify prompt (add stricter instruction)
retry once
## ELSE:
accept response


## 2.4 Benefit
● Reduces hallucinated or generic insights
● Demonstrates AI orchestration, not just usage
● Improves reliability without overcomplicating system

- Derived Feature Layer (Feature Engineering for AI)
## 3.1 Problem
Currently, raw metrics are passed directly to the AI:
MetricsDict → Prompt

This limits higher-level reasoning.

## 3.2 Enhancement: Feature Preparation Layer
Introduce a preprocessing step:
MetricsDict → DerivedFeatures → Prompt


## 3.3 Example Derived Features
## Feature Logic Purpose
is_thin_content

word_count < 300 Helps AI prioritise content issues

cta_density

cta_count / word_count Evaluates conversion
effectiveness
seo_risk_flag

meta_desc_len < 120 Highlights SEO weaknesses
heading_structure_
score

based on H1/H2
hierarchy
Detects structure issues

## 3.4 Benefit
● Improves AI reasoning quality
● Reduces reliance on model inference
● Demonstrates feature engineering thinking

- Structured Output Export (Machine + Human Readable)
## 4.1 Problem
Current output is CLI-only, optimized for human readability.

## 4.2 Enhancement: Dual Output System
Add structured output export:
output/
latest.json   ← machine-readable
latest.txt    ← CLI snapshot


4.3 JSON Structure
## {
## "metrics": { ... },
## "insights": { ... },
## "timestamp": "...",
## "url": "..."
## }



## 4.4 Benefit
● Enables integration with other systems
● Supports future dashboards or APIs
● Shows production-ready thinking

## 5. Observability & Execution Logging
## 5.1 Problem
Current logging focuses on prompts and responses only.

## 5.2 Enhancement: Operational Metrics
Extend logging to include:
## Metric Purpose
execution_time performance tracking
fetch_method requests vs playwright
usage
retry_count AI reliability tracking
error_type debugging and analysis

## 5.3 Example Log Addition
## Execution Time: 2.14s
Fetch Method: playwright
AI Retry Count: 1
Status: success


## 5.4 Benefit

● Enables system debugging
● Shows awareness of production concerns
● Demonstrates engineering maturity

## 6. Extensibility Considerations
## 6.1 Problem
The current system is designed for single-URL analysis.

## 6.2 Potential Extensions
## 1. Batch Processing
input: list[URL]
output: aggregated reports

- Multi-Page Crawling
● Homepage + internal pages
● Deeper SEO insights
## 3. Model Abstraction
● Swap Gemini ↔ OpenAI
● Plug-and-play AI backend
- Plugin-Based Metrics
● Add new metrics without modifying core logic

## 6.3 Benefit
● Demonstrates forward-thinking design
● Shows scalability awareness
● Signals production mindset


## 7. Trade-offs & Design Decisions
## 7.1 Static + Playwright Hybrid
## Decision Reason
## Use
requests
first
Faster, lightweight
Fallback to Playwright Handles JS-heavy
pages
## Trade-off:
● Slight complexity increase vs significantly improved coverage

7.2 Snippet-Based Content
## Decision Reason
Use text snippet instead of full HTML Reduces token
usage
## Trade-off:
● May miss deeper context in long pages

## 7.3 Single Retry Strategy
## Decision Reason
Retry AI call once only Prevents excessive API
usage
## Trade-off:
● May not fully recover from repeated failures

7.4 CLI-Based Output

## Decision Reason
CLI instead of web UI Simpler, faster to implement
## Trade-off:
● Less user-friendly but sufficient for assignment scope

## 8. Conclusion
These enhancements elevate the system from a functional assignment solution to a more
AI-native, production-aware architecture.
Key improvements include:
● AI validation and retry mechanisms
● Feature engineering for better reasoning
● Structured outputs for extensibility
● Observability for debugging and monitoring
Together, these demonstrate a deeper understanding of:
● AI system design
● reliability engineering
● and scalable architecture

