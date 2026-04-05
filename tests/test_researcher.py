"""Tests for the research agent."""

from unittest.mock import MagicMock, patch

from agents.researcher import _search_with_retry, run_research, format_research_for_synthesis


def test_search_with_retry_success(sample_tavily_response):
    client = MagicMock()
    client.search.return_value = sample_tavily_response

    results = _search_with_retry(client, "test query")
    assert len(results) == 3  # 1 answer + 2 results
    assert results[0]["source"] == "tavily_answer"
    assert results[1]["source"] == "tavily_search"


def test_search_with_retry_handles_failure():
    client = MagicMock()
    client.search.side_effect = Exception("API error")

    results = _search_with_retry(client, "test query")
    assert results == []


@patch("agents.researcher.TavilyClient")
@patch("agents.researcher.TAVILY_API_KEY", "test-key")
def test_run_research_returns_all_tracks(mock_client_cls, sample_tavily_response):
    mock_client = MagicMock()
    mock_client.search.return_value = sample_tavily_response
    mock_client_cls.return_value = mock_client

    results = run_research()
    assert len(results) == 10
    for track_key in results:
        assert isinstance(results[track_key], list)


@patch("agents.researcher.TavilyClient")
@patch("agents.researcher.TAVILY_API_KEY", "test-key")
def test_run_research_deduplicates_urls(mock_client_cls):
    mock_client = MagicMock()
    mock_client.search.return_value = {
        "answer": None,
        "results": [
            {"title": "Same Article", "url": "https://example.com/same", "content": "Duplicate"},
            {"title": "Same Article Copy", "url": "https://example.com/same", "content": "Duplicate"},
        ],
    }
    mock_client_cls.return_value = mock_client

    # Use only one track with one query for simplicity
    single_track = {
        "test": {"name": "Test Track", "queries": ["query1"]},
    }
    results = run_research(tracks=single_track)
    assert len(results["test"]) == 1  # Deduped


def test_format_research_for_synthesis(sample_research_text):
    from config import RESEARCH_TRACKS
    # Build a minimal results dict
    results = {
        "product_platform": [
            {"title": "Composer Launch", "url": "https://example.com", "content": "AI campaign generation"},
        ],
        "analytics_reporting": [
            {"title": "Custom Reporting", "url": "https://example.com/reporting", "content": "Public beta launched"},
        ],
    }
    text = format_research_for_synthesis(results)
    assert "Product & Platform" in text
    assert "Analytics" in text
    assert "Composer Launch" in text
