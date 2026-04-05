"""Tests for PDF report generation."""

import os
import tempfile

import pytest

from reports.html_generator import generate_html
from reports.pdf_generator import generate_pdf


def test_generate_pdf_creates_file(sample_brief_markdown):
    html = generate_html(sample_brief_markdown, "April 4, 2026")

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "test_report.pdf")
        result = generate_pdf(html, pdf_path)
        assert os.path.exists(result)
        assert os.path.getsize(result) > 1000  # At least 1KB


def test_pdf_output_is_valid_pdf(sample_brief_markdown):
    html = generate_html(sample_brief_markdown, "April 4, 2026")

    with tempfile.TemporaryDirectory() as tmpdir:
        pdf_path = os.path.join(tmpdir, "test_report.pdf")
        generate_pdf(html, pdf_path)
        with open(pdf_path, "rb") as f:
            header = f.read(5)
        assert header == b"%PDF-"
