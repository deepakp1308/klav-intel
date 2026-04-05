"""KLAV-INTEL v2.0 — Configuration and research track definitions."""

import os
from dotenv import load_dotenv

load_dotenv()

# ── API Keys ──────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN", "")
SLACK_USER_ID = os.getenv("SLACK_USER_ID", "W8FL6URHQ")
GITHUB_PAGES_URL = os.getenv("GITHUB_PAGES_URL", "https://deepakp1308.github.io/klav-intel/")

# ── LLM Settings ──────────────────────────────────────────────────────────
CLAUDE_MODEL = "claude-sonnet-4-6-20250514"
CLAUDE_MAX_TOKENS = 8192
CLAUDE_TEMPERATURE = 0.3

# ── Rate Limiting ─────────────────────────────────────────────────────────
TAVILY_DELAY_MS = 500
TAVILY_MAX_RETRIES = 3
TAVILY_RESULTS_PER_QUERY = 5

# ── Output Paths ──────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_OUTPUT_DIR = os.path.join(BASE_DIR, "reports", "output")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# ── Canonical Sources ─────────────────────────────────────────────────────
CANONICAL_URLS = {
    "whats_new": "https://www.klaviyo.com/whats-new/all",
    "blog": "https://www.klaviyo.com/blog/category/klaviyo-news",
    "community": "https://community.klaviyo.com/product-updates-announcements-51",
    "analytics": "https://www.klaviyo.com/solutions/analytics",
    "reporting": "https://www.klaviyo.com/features/reporting",
    "marketing_analytics": "https://www.klaviyo.com/products/marketing-analytics/strategy",
    "newsroom": "https://www.klaviyo.com/newsroom",
    "investors": "https://investors.klaviyo.com/news",
    "pricing": "https://www.klaviyo.com/pricing",
    "youtube": "https://www.youtube.com/@klaviyo",
    "tiktok": "https://www.tiktok.com/@klaviyo",
    "instagram": "https://www.instagram.com/klaviyo/",
    "linkedin": "https://www.linkedin.com/company/klaviyo/",
}

# ── Key Personnel ─────────────────────────────────────────────────────────
KEY_PERSONNEL = {
    "Andrew Bialecki": "CEO & Co-founder",
    "Amanda Whalen": "CFO",
    "Ed Hallen": "Co-founder & CPO",
    "Jamie Domenici": "CMO",
    "Steve Rowland": "President",
}

# ── 10 Research Tracks ────────────────────────────────────────────────────
RESEARCH_TRACKS = {
    "product_platform": {
        "name": "Product & Platform",
        "queries": [
            "Klaviyo new feature announcement product update 2026",
            "Klaviyo Customer Hub Helpdesk Composer update",
            "Klaviyo RCS WhatsApp SMS channel expansion 2026",
            "Klaviyo ecommerce integration Shopify WooCommerce update",
            "Klaviyo product changelog release notes April 2026",
        ],
    },
    "ai_intelligence": {
        "name": "AI Product Intelligence",
        "queries": [
            "Klaviyo Composer AI campaign generation capabilities 2026",
            "Klaviyo Customer Agent Marketing Agent autonomous AI",
            "Klaviyo AI model integration Claude ChatGPT Gemini MCP",
            "Klaviyo predictive analytics AI segmentation send time optimization",
            "Klaviyo AI features vs Mailchimp AI comparison 2026",
        ],
    },
    "analytics_reporting": {
        "name": "Analytics, Reporting & Attribution",
        "queries": [
            "Klaviyo analytics custom reporting dashboard features 2026",
            "Klaviyo attribution model multi-touch configurable windows",
            "Klaviyo funnel analysis cohort analysis segments from funnels",
            "Klaviyo RFM analysis predictive CLV churn scoring",
            "Klaviyo data warehouse connector reverse ETL CDP capabilities",
            "Klaviyo analytics ROI benchmark case study ecommerce",
        ],
    },
    "gtm_messaging": {
        "name": "Go-to-Market Messaging & Value Proposition",
        "queries": [
            "Klaviyo B2C CRM autonomous positioning 2026",
            "Klaviyo vs Mailchimp comparison switched brands",
            "Klaviyo target audience DTC mid-market enterprise positioning",
            "Klaviyo Forrester Gartner G2 analyst recognition 2026",
            "Klaviyo homepage value proposition messaging 2026",
        ],
    },
    "seo_paid": {
        "name": "SEO & Paid Search Strategy",
        "queries": [
            "Klaviyo blog content marketing strategy topics 2026",
            "Klaviyo vs Mailchimp comparison landing page",
            "best marketing automation platform ecommerce email analytics",
            "Klaviyo case study benchmark report 2026",
            "Klaviyo SEO content strategy email marketing analytics",
        ],
    },
    "video_social": {
        "name": "Digital Video & Social Content Strategy",
        "queries": [
            "Klaviyo YouTube channel recent videos topics 2026",
            "Klaviyo TikTok Instagram social media content strategy",
            "Klaviyo LinkedIn executive thought leadership Andrew Bialecki",
            "Klaviyo Jamie Domenici CMO marketing AI thought leadership",
            "Klaviyo video content analytics reporting data marketing",
        ],
    },
    "press_partnerships": {
        "name": "Press, Partnerships & Org Signals",
        "queries": [
            "Klaviyo press release partnership announcement 2026",
            "Klaviyo Shopify Google Meta TikTok partnership",
            "Klaviyo earnings revenue growth Q1 2026 financial results",
            "Klaviyo C-suite hire departure organizational change 2026",
            "Klaviyo Glassdoor employee sentiment review 2026",
        ],
    },
    "pricing": {
        "name": "Pricing & Competitive Position",
        "queries": [
            "Klaviyo pricing change 2026 active profile billing",
            "Klaviyo One surcharge pricing complaints",
            "Klaviyo vs Mailchimp pricing comparison contacts tiers 2026",
            "Klaviyo pricing customer complaints expensive cost",
        ],
    },
    "voice_of_market": {
        "name": "Voice of Market (Social & Reviews)",
        "queries": [
            "Klaviyo review Reddit ecommerce shopify emailmarketing 2026",
            "Klaviyo G2 review rating recent 2026",
            "Klaviyo Trustpilot review complaint 2026",
            "Klaviyo migration from Mailchimp switch experience review",
            "Klaviyo analytics reporting user feedback complaint 2026",
        ],
    },
    "crm_lead_to_cash": {
        "name": "CRM & Lead-to-Cash",
        "queries": [
            "Klaviyo B2C CRM positioning evolution customer hub 2026",
            "Klaviyo Helpdesk CSAT support revenue attribution",
            "Klaviyo lead scoring pipeline B2B features",
            "Klaviyo customer data platform CDP capabilities 2026",
        ],
    },
}
