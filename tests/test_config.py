"""Tests for config module."""

import config


def test_research_tracks_defined():
    assert len(config.RESEARCH_TRACKS) == 10


def test_each_track_has_queries():
    for key, track in config.RESEARCH_TRACKS.items():
        assert "name" in track, f"Track {key} missing 'name'"
        assert "queries" in track, f"Track {key} missing 'queries'"
        assert len(track["queries"]) >= 3, f"Track {key} has < 3 queries"


def test_canonical_urls_defined():
    assert len(config.CANONICAL_URLS) >= 10


def test_key_personnel():
    assert "Andrew Bialecki" in config.KEY_PERSONNEL
    assert "Ed Hallen" in config.KEY_PERSONNEL


def test_output_paths_defined():
    assert config.BASE_DIR
    assert config.REPORTS_OUTPUT_DIR
    assert config.DOCS_DIR
