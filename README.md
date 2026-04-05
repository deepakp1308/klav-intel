# KLAV-INTEL v2.0

Klaviyo Competitive Intelligence Agent — weekly CEO-ready briefs for Mailchimp R&A leadership.

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Run full pipeline
python main.py --run

# Generate from existing markdown
python main.py --from-markdown reports/output/2026-04-04/KLAV-INTEL_2026-04-04.md

# Research only (no synthesis/delivery)
python main.py --run --dry-run

# Skip deployment/notification
python main.py --run --no-deploy --no-slack
```

## Architecture

| Module | Purpose |
|--------|---------|
| `agents/researcher.py` | 10 research tracks via Tavily API |
| `agents/synthesizer.py` | Claude API → McKinsey Markdown brief |
| `reports/html_generator.py` | Markdown → branded HTML |
| `reports/pdf_generator.py` | HTML → PDF via Playwright |
| `delivery/slack_notify.py` | Slack DM with top signals |
| `delivery/github_pages.py` | Deploy to GitHub Pages |

## Environment Variables

```
ANTHROPIC_API_KEY=sk-ant-...
TAVILY_API_KEY=tvly-...
SLACK_BOT_TOKEN=xoxb-...
SLACK_USER_ID=W8FL6URHQ
```

## Tests

```bash
pytest -v
```

## Weekly Automation

GitHub Actions cron runs every Monday at midnight ET (5:00 AM UTC). Auto-disables after 4 runs.
