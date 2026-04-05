"""Shared fixtures for KLAV-INTEL tests."""

import pytest


SAMPLE_TAVILY_RESPONSE = {
    "answer": "Klaviyo launched Composer, an AI campaign generation tool.",
    "results": [
        {
            "title": "Klaviyo Launches Composer for AI Campaign Creation",
            "url": "https://www.klaviyo.com/blog/composer-launch",
            "content": "Klaviyo announced Composer, which generates launch-ready campaigns from a single prompt, trained on 14 years of data across 193,000 brands.",
        },
        {
            "title": "Klaviyo Q1 2026 Product Updates",
            "url": "https://www.klaviyo.com/whats-new/q1-2026",
            "content": "RCS messaging is now GA. Personalized Send Time optimizes delivery per-subscriber. Customer Hub supports WooCommerce.",
        },
    ],
}


SAMPLE_BRIEF_MARKDOWN = """# KLAV-INTEL | Week of April 4, 2026
**Klaviyo Competitive Intelligence | Mailchimp R&A | Confidential**

---

## EXECUTIVE SNAPSHOT

| Signal | Insight | Mailchimp R&A Implication |
|--------|---------|--------------------------|
| 🔴 Composer redefines campaign creation | AI generates launch-ready campaigns from single prompt — 193K brand dataset | Accelerate Mailchimp AI campaign builder; brief product team by Apr 11 |
| 🔴 "Autonomous B2C CRM" positioning | Klaviyo frames itself as category-creator; claims 50K brands switched | Commission positioning study; update battlecards by Apr 18 |
| 🟡 Analytics custom reporting in beta | Addresses most-cited G2 weakness; adds funnel-to-segment activation | Evaluate R&A feature parity gaps; prioritize Q3 roadmap items |
| 🟢 Pricing backlash intensifies | Active-profile billing driving 1-star reviews; Klaviyo One adds 20% surcharge | Arm sales with TCO comparison; target churning Klaviyo accounts |

---

## I. PRODUCT & AI VELOCITY

Klaviyo shipped 75+ features in Q1 2026. The headline is Composer — an agentic AI that builds complete campaigns from natural-language prompts, trained on 14 years of performance data across 193,000 brands. Channel expansion continued: RCS messaging is now GA via Google partnership, Personalized Send Time optimizes delivery per-subscriber, and Customer Hub broke out of Shopify-only to support WooCommerce.

**R&A implication:** Composer's AI-optimized targeting will change attribution patterns. R&A must model impact on competitive narrative.

## II. ANALYTICS & REPORTING POSITIONING

Klaviyo positions K:Analytics as "the customer analytics platform to unify your reporting." Key proof points: "48x ROI after consolidation", "flows generate 41% of email revenue from 5.3% of sends." Custom reporting entered public beta. Segments from Funnels links analytics directly to activation. Attribution remains cooperative last-touch for owned channels — multiple analyses note it overstates Klaviyo's contribution.

**R&A implication:** Klaviyo is closing its reporting flexibility gap. Their attribution overstatement is an exploitable weakness. Recommend: publish attribution methodology comparison, fast-track custom reporting features.

## III. GO-TO-MARKET & DIGITAL PRESENCE

**Messaging:** Shifted from "email marketing platform" to "Autonomous B2C CRM." Claims "50,000+ brands switched from Mailchimp or Salesforce."
**SEO/SEM:** Targets "best marketing automation platform", "ecommerce email analytics", "marketing attribution ecommerce."
**Video & Social:** YouTube features Composer walkthroughs. Jamie Domenici actively publishing AI thought leadership on LinkedIn.
**Case Studies:** 323% conversion improvement via segmentation, 18x revenue-per-recipient in flows vs campaigns.

## IV. MARKET SIGNALS

FY2025 revenue hit $1.2B (+32% YoY); FY2026 outlook raised to ~$1.5B. Google strategic partnership for RCS. Glassdoor at 3.3/5. Klaviyo One adds 20% surcharge for >$10K/mo accounts.

## V. VOICE OF MARKET

| Source | Positive | Negative | Analytics-Specific |
|--------|----------|----------|--------------------|
| Reddit | Best Shopify integration | Cost scaling concerns | Limited custom reporting |
| G2/Capterra | Segmentation depth | Pricing escalation | More flexible reporting requested |
| Trustpilot | Agent praise | Support, billing jumps | Attribution overstatement noted |

---

## STRATEGIC IMPLICATIONS MATRIX

| Priority | Klaviyo Move | Impact to Mailchimp R&A | Recommended Action | Owner |
|----------|-------------|------------------------|-------------------|-------|
| 🔴 | Composer AI campaign gen | Redefines AI marketing baseline | Brief product team by Apr 11 | Product / R&A |
| 🔴 | Custom reporting beta | Closes their #1 weakness | Fast-track custom reporting | R&A |
| 🟡 | Claude/ChatGPT integrations | Conversational analytics moat | Assess MCP strategy by Apr 25 | R&A / Platform |
| 🟢 | Pricing backlash | Mid-market churn opportunity | Launch win-back campaign | Sales / Growth |

---

*KLAV-INTEL v2.0 | April 4, 2026 | Sources: 28 | Next brief: April 11, 2026*"""


@pytest.fixture
def sample_tavily_response():
    return SAMPLE_TAVILY_RESPONSE


@pytest.fixture
def sample_brief_markdown():
    return SAMPLE_BRIEF_MARKDOWN


@pytest.fixture
def sample_research_text():
    return """### Product & Platform

**[1] Klaviyo Launches Composer** (https://www.klaviyo.com/blog/composer-launch)
Klaviyo announced Composer, which generates launch-ready campaigns from a single prompt.

**[2] Klaviyo Q1 2026 Updates** (https://www.klaviyo.com/whats-new/q1-2026)
RCS messaging is now GA. Personalized Send Time optimizes delivery per-subscriber.

### Analytics, Reporting & Attribution

**[1] K:Analytics Custom Reporting Beta** (https://www.klaviyo.com/features/reporting)
Custom reporting entered public beta for Marketing Analytics customers.

**[2] Attribution Model Update**
Klaviyo's attribution remains cooperative last-touch. Configurable windows now in-dashboard."""
