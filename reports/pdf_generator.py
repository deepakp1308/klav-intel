"""KLAV-INTEL v2.0 — PDF report generator: HTML → PDF via Playwright."""

from __future__ import annotations

import logging
import os
import tempfile

from playwright.sync_api import sync_playwright

logger = logging.getLogger("klav-intel.pdf")


def generate_pdf(html_content: str, output_path: str) -> str:
    """Convert HTML string to PDF using Playwright headless Chromium. Returns the output path."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".html", mode="w", delete=False, encoding="utf-8") as f:
        f.write(html_content)
        tmp_html = f.name

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(f"file://{tmp_html}", wait_until="networkidle")
            page.pdf(
                path=output_path,
                format="Letter",
                margin={"top": "0.6in", "bottom": "0.6in", "left": "0.7in", "right": "0.7in"},
                print_background=True,
            )
            browser.close()
    finally:
        os.unlink(tmp_html)

    size_kb = os.path.getsize(output_path) / 1024
    logger.info(f"PDF saved: {output_path} ({size_kb:.0f} KB)")
    return output_path
