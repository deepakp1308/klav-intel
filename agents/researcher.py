"""KLAV-INTEL v2.0 — Research agent: 10 intelligence tracks via Tavily API."""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

from tavily import TavilyClient

from config import (
    TAVILY_API_KEY,
    TAVILY_DELAY_MS,
    TAVILY_MAX_RETRIES,
    TAVILY_RESULTS_PER_QUERY,
    RESEARCH_TRACKS,
)

logger = logging.getLogger("klav-intel.researcher")


def _search_with_retry(client: TavilyClient, query: str) -> list[dict[str, Any]]:
    """Execute a single Tavily search with retry and rate limiting."""
    for attempt in range(TAVILY_MAX_RETRIES):
        try:
            time.sleep(TAVILY_DELAY_MS / 1000)
            response = client.search(
                query=query,
                search_depth="advanced",
                max_results=TAVILY_RESULTS_PER_QUERY,
                include_answer=True,
            )
            results = []
            if response.get("answer"):
                results.append({
                    "title": "Tavily Summary",
                    "url": "",
                    "content": response["answer"],
                    "source": "tavily_answer",
                })
            for r in response.get("results", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", ""),
                    "source": "tavily_search",
                })
            return results
        except Exception as e:
            wait = (attempt + 1) * 5
            logger.warning(f"Search retry {attempt + 1}/{TAVILY_MAX_RETRIES} for '{query}': {e}. Waiting {wait}s")
            if attempt < TAVILY_MAX_RETRIES - 1:
                time.sleep(wait)
    logger.error(f"All retries exhausted for query: {query}")
    return []


def run_research(tracks: Optional[dict] = None) -> dict:
    """Run all research tracks. Returns {track_key: [results]}."""
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY not set. Add it to .env")

    client = TavilyClient(api_key=TAVILY_API_KEY)
    tracks = tracks or RESEARCH_TRACKS
    all_results: dict[str, list[dict[str, Any]]] = {}
    seen_urls: set[str] = set()

    total_queries = sum(len(t["queries"]) for t in tracks.values())
    query_num = 0

    for track_key, track_cfg in tracks.items():
        track_name = track_cfg["name"]
        track_results: list[dict[str, Any]] = []

        for query in track_cfg["queries"]:
            query_num += 1
            logger.info(f"[{query_num}/{total_queries}] Track '{track_name}': {query}")
            results = _search_with_retry(client, query)

            for r in results:
                url = r.get("url", "")
                if url and url in seen_urls:
                    continue
                if url:
                    seen_urls.add(url)
                track_results.append(r)

        all_results[track_key] = track_results
        logger.info(f"Track '{track_name}': {len(track_results)} unique results")

    total = sum(len(v) for v in all_results.values())
    logger.info(f"Research complete: {total} total unique results across {len(tracks)} tracks")
    return all_results


def format_research_for_synthesis(results: dict[str, list[dict[str, Any]]]) -> str:
    """Format research results into a text block for LLM synthesis."""
    sections = []
    for track_key, track_results in results.items():
        track_name = RESEARCH_TRACKS.get(track_key, {}).get("name", track_key)
        section = f"\n### {track_name}\n"
        for i, r in enumerate(track_results[:15], 1):  # Cap at 15 per track
            title = r.get("title", "Untitled")
            url = r.get("url", "")
            content = r.get("content", "")[:600]  # Trim content
            section += f"\n**[{i}] {title}**"
            if url:
                section += f" ({url})"
            section += f"\n{content}\n"
        sections.append(section)
    return "\n".join(sections)
