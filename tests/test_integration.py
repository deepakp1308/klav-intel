"""Integration tests: full pipeline with fixture data (mocked APIs)."""

import os
import tempfile
from unittest.mock import patch, MagicMock

from reports.html_generator import generate_html, save_html
from reports.pdf_generator import generate_pdf
from delivery.slack_notify import _extract_top_signals
from delivery.github_pages import deploy_to_pages


def test_full_report_generation_pipeline(sample_brief_markdown):
    """End-to-end: markdown → HTML → PDF."""
    html = generate_html(sample_brief_markdown, "April 4, 2026")
    assert "<html" in html

    with tempfile.TemporaryDirectory() as tmpdir:
        html_path = os.path.join(tmpdir, "report.html")
        save_html(html, html_path)
        assert os.path.exists(html_path)

        pdf_path = os.path.join(tmpdir, "report.pdf")
        generate_pdf(html, pdf_path)
        assert os.path.exists(pdf_path)
        assert os.path.getsize(pdf_path) > 1000


def test_extract_top_signals(sample_brief_markdown):
    signals = _extract_top_signals(sample_brief_markdown)
    assert len(signals) >= 2
    assert any("Composer" in s for s in signals)


def test_deploy_creates_docs_files(sample_brief_markdown):
    html = generate_html(sample_brief_markdown, "April 4, 2026")

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("delivery.github_pages.DOCS_DIR", tmpdir):
            archive_file = deploy_to_pages(html, "April 4, 2026")
            assert os.path.exists(os.path.join(tmpdir, "index.html"))
            assert os.path.exists(os.path.join(tmpdir, archive_file))
            assert os.path.exists(os.path.join(tmpdir, "archive.html"))


def test_archive_html_contains_links(sample_brief_markdown):
    html = generate_html(sample_brief_markdown, "April 4, 2026")

    with tempfile.TemporaryDirectory() as tmpdir:
        with patch("delivery.github_pages.DOCS_DIR", tmpdir):
            deploy_to_pages(html, "April 4, 2026")
            with open(os.path.join(tmpdir, "archive.html")) as f:
                archive = f.read()
            assert "April 4, 2026" in archive
            assert "KLAV-INTEL" in archive
