"""KLAV-INTEL v2.0 — Slack DM delivery."""

from __future__ import annotations

import logging
import re
from typing import Optional

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import SLACK_BOT_TOKEN, SLACK_USER_ID, GITHUB_PAGES_URL

logger = logging.getLogger("klav-intel.slack")


def _extract_top_signals(markdown_text: str) -> list[str]:
    """Extract top 3 signals from the EXECUTIVE SNAPSHOT table."""
    signals = []
    in_snapshot = False
    for line in markdown_text.split("\n"):
        if "EXECUTIVE SNAPSHOT" in line:
            in_snapshot = True
            continue
        if in_snapshot and line.startswith("|") and "Signal" not in line and "---" not in line:
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 2:
                signal = cells[0].strip()
                insight = cells[1].strip()
                signals.append(f"{signal} — {insight}")
        if in_snapshot and line.startswith("##") and "SNAPSHOT" not in line:
            break
    return signals[:3]


def send_slack_dm(
    markdown_text: str,
    report_date: str,
    pdf_path: Optional[str] = None,
    html_url: Optional[str] = None,
) -> bool:
    """Send the brief summary as a Slack DM."""
    if not SLACK_BOT_TOKEN:
        logger.warning("SLACK_BOT_TOKEN not set — skipping Slack delivery")
        return False

    client = WebClient(token=SLACK_BOT_TOKEN)
    signals = _extract_top_signals(markdown_text)

    archive_url = GITHUB_PAGES_URL.rstrip("/") + "/archive.html"
    report_url = html_url or GITHUB_PAGES_URL

    signal_lines = ""
    emojis = ["1️⃣", "2️⃣", "3️⃣"]
    for i, s in enumerate(signals):
        signal_lines += f"{emojis[i]} {s}\n"

    message = f"""🔍 *KLAV-INTEL v2.0 — Week of {report_date}*

*Top signals:*
{signal_lines}
📄 *Full brief:* {report_url}
📊 *Archive:* {archive_url}

_Reply for deeper analysis on any signal._"""

    try:
        response = client.chat_postMessage(
            channel=SLACK_USER_ID,
            text=message,
            unfurl_links=False,
        )
        ts = response["ts"]
        logger.info(f"Slack DM sent: ts={ts}")

        if pdf_path:
            try:
                client.files_upload_v2(
                    channel=SLACK_USER_ID,
                    file=pdf_path,
                    title=f"KLAV-INTEL_{report_date.replace(' ', '_')}.pdf",
                    initial_comment="📎 PDF attached",
                    thread_ts=ts,
                )
                logger.info("PDF uploaded to Slack thread")
            except SlackApiError as e:
                logger.warning(f"PDF upload failed: {e}")

        return True
    except SlackApiError as e:
        logger.error(f"Slack DM failed: {e}")
        return False
