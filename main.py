#!/usr/bin/env python3
"""KLAV-INTEL v2.0 — Klaviyo Competitive Intelligence Agent.

Usage:
    python main.py --run                  # Full pipeline
    python main.py --run --no-deploy      # Skip GitHub Pages
    python main.py --run --no-slack       # Skip Slack DM
    python main.py --run --dry-run        # Research only, no synthesis/delivery
    python main.py --from-markdown FILE   # Generate PDF/HTML from existing .md
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import datetime
from typing import Optional

from config import REPORTS_OUTPUT_DIR, LOGS_DIR

# ── Logging ───────────────────────────────────────────────────────────────
os.makedirs(LOGS_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(LOGS_DIR, "klav-intel.log")),
    ],
)
logger = logging.getLogger("klav-intel")


def run_pipeline(
    dry_run: bool = False,
    no_deploy: bool = False,
    no_slack: bool = False,
    from_markdown: Optional[str] = None,
) -> dict:
    """Execute the full KLAV-INTEL pipeline."""
    from agents.researcher import run_research, format_research_for_synthesis
    from agents.synthesizer import synthesize_brief
    from reports.html_generator import generate_html, save_html
    from reports.pdf_generator import generate_pdf
    from delivery.github_pages import deploy_to_pages, git_commit_and_push
    from delivery.slack_notify import send_slack_dm

    report_date = datetime.now().strftime("%B %d, %Y")
    date_slug = datetime.now().strftime("%Y-%m-%d")
    output_dir = os.path.join(REPORTS_OUTPUT_DIR, date_slug)
    os.makedirs(output_dir, exist_ok=True)

    result = {"date": report_date, "date_slug": date_slug}

    # ── Step 1: Research or load markdown ─────────────────────────────
    if from_markdown:
        logger.info(f"Loading markdown from: {from_markdown}")
        with open(from_markdown, "r", encoding="utf-8") as f:
            brief_md = f.read()
    else:
        logger.info("=" * 60)
        logger.info("PHASE 1: INTELLIGENCE COLLECTION")
        logger.info("=" * 60)
        research = run_research()
        research_text = format_research_for_synthesis(research)

        # Save raw research
        research_path = os.path.join(output_dir, f"research_{date_slug}.txt")
        with open(research_path, "w", encoding="utf-8") as f:
            f.write(research_text)
        result["research_path"] = research_path
        logger.info(f"Research saved: {research_path}")

        if dry_run:
            logger.info("DRY RUN — stopping after research")
            result["status"] = "dry_run"
            return result

        # ── Step 2: Synthesis ─────────────────────────────────────────
        logger.info("=" * 60)
        logger.info("PHASE 2: SYNTHESIS")
        logger.info("=" * 60)
        brief_md = synthesize_brief(research_text, report_date)

    # Save markdown
    md_path = os.path.join(output_dir, f"KLAV-INTEL_{date_slug}.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(brief_md)
    result["markdown_path"] = md_path
    logger.info(f"Markdown saved: {md_path}")

    # ── Step 3: Generate HTML ─────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("PHASE 3: REPORT GENERATION")
    logger.info("=" * 60)
    html_content = generate_html(brief_md, report_date)
    html_path = os.path.join(output_dir, f"KLAV-INTEL_{date_slug}.html")
    save_html(html_content, html_path)
    result["html_path"] = html_path

    # ── Step 4: Generate PDF ──────────────────────────────────────────
    pdf_path = os.path.join(output_dir, f"KLAV-INTEL_{date_slug}.pdf")
    generate_pdf(html_content, pdf_path)
    result["pdf_path"] = pdf_path

    # ── Step 5: Deploy to GitHub Pages ────────────────────────────────
    if not no_deploy:
        logger.info("=" * 60)
        logger.info("PHASE 4: GITHUB PAGES DEPLOYMENT")
        logger.info("=" * 60)
        archive_file = deploy_to_pages(html_content, report_date)
        result["archive_file"] = archive_file
        pushed = git_commit_and_push(report_date)
        result["deployed"] = pushed
    else:
        logger.info("Skipping GitHub Pages deployment (--no-deploy)")

    # ── Step 6: Slack DM ──────────────────────────────────────────────
    if not no_slack:
        logger.info("=" * 60)
        logger.info("PHASE 5: SLACK DELIVERY")
        logger.info("=" * 60)
        sent = send_slack_dm(
            markdown_text=brief_md,
            report_date=report_date,
            pdf_path=pdf_path,
        )
        result["slack_sent"] = sent
    else:
        logger.info("Skipping Slack DM (--no-slack)")

    result["status"] = "complete"
    logger.info("=" * 60)
    logger.info("KLAV-INTEL COMPLETE")
    logger.info(f"  Markdown: {result.get('markdown_path')}")
    logger.info(f"  HTML:     {result.get('html_path')}")
    logger.info(f"  PDF:      {result.get('pdf_path')}")
    logger.info("=" * 60)
    return result


def main():
    parser = argparse.ArgumentParser(description="KLAV-INTEL v2.0 — Klaviyo Competitive Intelligence")
    parser.add_argument("--run", action="store_true", help="Run the full pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Research only, no synthesis/delivery")
    parser.add_argument("--no-deploy", action="store_true", help="Skip GitHub Pages deployment")
    parser.add_argument("--no-slack", action="store_true", help="Skip Slack DM")
    parser.add_argument("--from-markdown", type=str, help="Generate PDF/HTML from existing .md file")

    args = parser.parse_args()

    if not args.run and not args.from_markdown:
        parser.print_help()
        sys.exit(1)

    result = run_pipeline(
        dry_run=args.dry_run,
        no_deploy=args.no_deploy,
        no_slack=args.no_slack,
        from_markdown=args.from_markdown,
    )

    if result["status"] == "complete":
        logger.info("Pipeline finished successfully")
    elif result["status"] == "dry_run":
        logger.info("Dry run finished — research saved")


if __name__ == "__main__":
    main()
