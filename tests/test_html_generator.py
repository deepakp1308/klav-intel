"""Tests for HTML report generation."""

from reports.html_generator import generate_html, _classify_tables


def test_generate_html_contains_template_elements(sample_brief_markdown):
    html = generate_html(sample_brief_markdown, "April 4, 2026")
    assert "KLAV-INTEL" in html
    assert "April 4, 2026" in html
    assert "Confidential" in html
    assert "<table" in html
    assert "Helvetica" in html


def test_generate_html_renders_markdown_tables(sample_brief_markdown):
    html = generate_html(sample_brief_markdown, "April 4, 2026")
    assert "<th>" in html or "<td>" in html


def test_generate_html_includes_all_sections(sample_brief_markdown):
    html = generate_html(sample_brief_markdown, "April 4, 2026")
    assert "PRODUCT" in html
    assert "ANALYTICS" in html
    assert "MARKET SIGNALS" in html
    assert "STRATEGIC IMPLICATIONS" in html


def test_classify_tables_adds_snapshot_class():
    html = "<table>\n<tr><td>First</td></tr>\n</table>\n<table>\n<tr><td>Second</td></tr>\n</table>"
    result = _classify_tables(html)
    assert 'class="snapshot-table"' in result
