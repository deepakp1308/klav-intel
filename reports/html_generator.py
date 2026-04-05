"""KLAV-INTEL v2.0 — HTML report generator: Markdown → styled HTML."""

from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional

import markdown
from jinja2 import Environment, FileSystemLoader

from config import BASE_DIR

logger = logging.getLogger("klav-intel.html")

TEMPLATE_DIR = os.path.join(BASE_DIR, "reports", "templates")


def _classify_tables(html: str) -> str:
    """Add CSS classes to tables based on their position/content."""
    count = 0
    classified = []
    for line in html.split("\n"):
        if "<table>" in line:
            count += 1
            if count == 1:
                line = line.replace("<table>", '<table class="snapshot-table">')
            elif "Positive" in html[html.find("<table>"):html.find("</table>", html.find("<table>"))]:
                line = line.replace("<table>", '<table class="vom-table">')
            elif count >= 3:
                line = line.replace("<table>", '<table class="matrix-table">')
        classified.append(line)
    return "\n".join(classified)


def generate_html(markdown_text: str, report_date: Optional[str] = None) -> str:
    """Convert Markdown brief to styled HTML using Jinja2 template."""
    if not report_date:
        report_date = datetime.now().strftime("%B %d, %Y")

    md = markdown.Markdown(extensions=["tables", "fenced_code"])
    html_content = md.convert(markdown_text)
    html_content = _classify_tables(html_content)

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("executive_brief.html")

    full_html = template.render(
        content=html_content,
        report_date=report_date,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M UTC"),
    )

    logger.info(f"HTML generated: {len(full_html):,} chars")
    return full_html


def save_html(html: str, output_path: str) -> str:
    """Save HTML to file. Returns the path."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    logger.info(f"HTML saved: {output_path}")
    return output_path
