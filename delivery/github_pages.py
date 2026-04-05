"""KLAV-INTEL v2.0 — GitHub Pages deployment."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
from datetime import datetime
from typing import Optional

from config import BASE_DIR, DOCS_DIR

logger = logging.getLogger("klav-intel.deploy")


def _run_git(args: list, cwd: Optional[str] = None) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd or BASE_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.error(f"git {' '.join(args)} failed: {result.stderr}")
        raise RuntimeError(f"git error: {result.stderr}")
    return result.stdout.strip()


def deploy_to_pages(html_content: str, report_date: str) -> str:
    """Deploy HTML to docs/ for GitHub Pages. Returns the report URL path."""
    os.makedirs(DOCS_DIR, exist_ok=True)

    date_slug = datetime.now().strftime("%Y-%m-%d")
    archive_filename = f"KLAV-INTEL_{date_slug}.html"

    # Save as latest (index.html)
    index_path = os.path.join(DOCS_DIR, "index.html")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    logger.info(f"Updated docs/index.html")

    # Save archive copy
    archive_path = os.path.join(DOCS_DIR, archive_filename)
    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    logger.info(f"Saved docs/{archive_filename}")

    # Update archive.html
    _update_archive_index(report_date, archive_filename)

    return archive_filename


def _update_archive_index(report_date: str, new_filename: str) -> None:
    """Update the archive.html page with the new report link."""
    archive_path = os.path.join(DOCS_DIR, "archive.html")

    # Build new entry
    new_entry = f'    <li><a href="{new_filename}">{report_date}</a></li>\n'

    if os.path.exists(archive_path):
        with open(archive_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Insert new entry after <ul>
        content = content.replace("<ul>\n", f"<ul>\n{new_entry}", 1)
    else:
        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>KLAV-INTEL Archive</title>
<style>
  body {{ font-family: Helvetica, Arial, sans-serif; max-width: 600px; margin: 40px auto; color: #1a1f36; }}
  h1 {{ color: #162251; border-bottom: 2px solid #00b9a9; padding-bottom: 8px; }}
  a {{ color: #0070d2; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  li {{ margin: 8px 0; }}
</style>
</head>
<body>
<h1>KLAV-INTEL Archive</h1>
<p>Weekly Klaviyo Competitive Intelligence Briefs</p>
<ul>
{new_entry}</ul>
<p><a href="index.html">&larr; Latest Brief</a></p>
</body>
</html>"""

    with open(archive_path, "w", encoding="utf-8") as f:
        f.write(content)
    logger.info("Updated docs/archive.html")


def git_commit_and_push(report_date: str) -> bool:
    """Stage docs/, commit, and push to origin."""
    try:
        _run_git(["add", "docs/"])
        _run_git(["commit", "-m", f"KLAV-INTEL: Week of {report_date}"])
        _run_git(["push", "origin", "main"])
        logger.info("Pushed to GitHub")
        return True
    except RuntimeError as e:
        logger.error(f"Git push failed: {e}")
        return False
