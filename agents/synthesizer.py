"""KLAV-INTEL v2.0 — Synthesis agent: Claude API → McKinsey Markdown brief."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Optional

import anthropic

from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, CLAUDE_MAX_TOKENS, CLAUDE_TEMPERATURE

logger = logging.getLogger("klav-intel.synthesizer")

SYSTEM_PROMPT = """You are KLAV-INTEL, an elite competitive intelligence analyst producing CEO-ready briefs for Mailchimp's R&A leadership. Your output standard is McKinsey/BCG — every sentence must earn its place on the page.

WRITING RULES (Non-Negotiable):
1. Pyramid Principle: State the conclusion, then the evidence. Never bury the lead.
2. No filler phrases: Delete "continues to", "it is worth noting", "interestingly", "as mentioned".
3. Quantify everything: Use numbers, percentages, dollar figures wherever available.
4. Attribution density: "Klaviyo claims 48x ROI" not "they report good results".
5. Competitive framing: Every finding should implicitly or explicitly reference Mailchimp position.
6. 2-page ceiling: Ruthlessly edit for density. If it doesn't fit, cut the lowest-priority item.
7. Action verbs in recommendations: "Brief product team by Apr 11" not "Consider reviewing".
8. Every section ends with bold **R&A implication:** stating what this means for Mailchimp."""

BRIEF_TEMPLATE = """Produce the executive brief in EXACTLY this Markdown format. Fill every section with real intelligence from the research data. Use the exact heading structure below.

# KLAV-INTEL | Week of {report_date}
**Klaviyo Competitive Intelligence | Mailchimp R&A | Confidential**

---

## EXECUTIVE SNAPSHOT

| Signal | Insight | Mailchimp R&A Implication |
|--------|---------|--------------------------|
| [emoji] [1-line signal] | [1-line evidence with number] | [1-line action with deadline] |

(Include exactly 4 rows: 2x 🔴, 1x 🟡, 1x 🟢)

---

## I. PRODUCT & AI VELOCITY

[2-3 tight paragraphs. Tag ICP: 🛒 E-Commerce, 💼 Professional Services, 🏢 Enterprise. End with bold **R&A implication:**]

## II. ANALYTICS & REPORTING POSITIONING

[Most important section. 2 paragraphs covering: analytics value proposition, K:Analytics features, attribution models, custom reporting, case studies/benchmarks, user review weaknesses. End with bold **R&A implication:**]

## III. GO-TO-MARKET & DIGITAL PRESENCE

[1-2 paragraphs in exhibit-style density with bold subsections:]
**Messaging:** [positioning, competitive claims]
**SEO/SEM:** [search terms, content strategy]
**Video & Social:** [YouTube | TikTok/IG | LinkedIn exec presence]
**Case Studies:** [verticals, metrics highlighted]

## IV. MARKET SIGNALS

[1 tight paragraph: press, partnerships, org changes, pricing, earnings, reviews. Only material items.]

## V. VOICE OF MARKET

| Source | Positive | Negative | Analytics-Specific |
|--------|----------|----------|--------------------|
| Reddit | [2-3 words] | [2-3 words] | [2-3 words] |
| G2/Capterra | [2-3 words] | [2-3 words] | [2-3 words] |
| Trustpilot | [2-3 words] | [2-3 words] | [2-3 words] |

---

## STRATEGIC IMPLICATIONS MATRIX

| Priority | Klaviyo Move | Impact to Mailchimp R&A | Recommended Action | Owner |
|----------|-------------|------------------------|-------------------|-------|
| 🔴 | [move] | [impact] | [action + deadline] | [team] |
| 🔴 | [move] | [impact] | [action + deadline] | [team] |
| 🟡 | [move] | [impact] | [action + deadline] | [team] |
| 🟢 | [move] | [impact] | [action + deadline] | [team] |

---

*KLAV-INTEL v2.0 | {report_date} | Sources: [count] | Next: {next_date}*"""


def synthesize_brief(research_text: str, report_date: Optional[str] = None) -> str:
    """Synthesize research into a McKinsey-grade Markdown executive brief."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not set. Add it to .env")

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    if not report_date:
        report_date = datetime.now().strftime("%B %d, %Y")

    next_monday = datetime.now() + timedelta(days=(7 - datetime.now().weekday()) % 7 or 7)
    next_date = next_monday.strftime("%B %d, %Y")

    user_prompt = f"""Here is the research intelligence gathered this week across 10 tracks:

{research_text}

---

Now produce the executive brief for the week of {report_date}.
Next brief date: {next_date}.

{BRIEF_TEMPLATE.format(report_date=report_date, next_date=next_date)}"""

    logger.info(f"Synthesizing brief ({len(research_text):,} chars of research) via {CLAUDE_MODEL}")

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        temperature=CLAUDE_TEMPERATURE,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    brief = message.content[0].text
    logger.info(f"Brief generated: {len(brief):,} chars, {message.usage.input_tokens} in / {message.usage.output_tokens} out tokens")
    return brief
