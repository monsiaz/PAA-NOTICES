"""
Core PAA extractor — wraps SerpAPI to extract People Also Ask questions.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Optional

import requests


@dataclass
class PAAResult:
    """A single PAA question with its answer snippet."""
    question: str
    snippet: str
    title: Optional[str] = None
    link: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "snippet": self.snippet,
            "title": self.title,
            "link": self.link,
        }


class PAAScraper:
    """
    Extract People Also Ask (PAA) questions from Google SERP via SerpAPI.

    Args:
        api_key: SerpAPI key. Falls back to SERPAPI_KEY environment variable.
        lang: Language code (e.g. "en", "fr"). Default: "en".
        country: Country code (e.g. "us", "fr"). Default: "us".
        location: Optional full location string (e.g. "Paris,Ile-de-France,France").

    Example::

        from seo_paa import PAAScraper

        scraper = PAAScraper(api_key="your_key", lang="en", country="us")
        results = scraper.get_paa("best surf camp senegal")
        for r in results:
            print(r.question, "->", r.snippet)
    """

    _ENDPOINT = "https://serpapi.com/search"

    def __init__(
        self,
        api_key: Optional[str] = None,
        lang: str = "en",
        country: str = "us",
        location: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("SERPAPI_KEY", "")
        if not self.api_key:
            raise ValueError(
                "SerpAPI key required. Pass api_key= or set SERPAPI_KEY env var."
            )
        self.lang = lang
        self.country = country
        self.location = location

    def get_paa(self, query: str, max_results: int = 10) -> list[PAAResult]:
        """
        Fetch PAA questions for a given search query.

        Args:
            query: The search query (e.g. "best surf camp senegal").
            max_results: Maximum number of PAA questions to return.

        Returns:
            List of PAAResult objects.
        """
        params = {
            "q": query,
            "hl": self.lang,
            "gl": self.country,
            "api_key": self.api_key,
            "engine": "google",
            "device": "desktop",
            "output": "json",
        }
        if self.location:
            params["location"] = self.location

        resp = requests.get(self._ENDPOINT, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        raw = data.get("related_questions", [])
        results = []
        for item in raw[:max_results]:
            results.append(
                PAAResult(
                    question=item.get("question", ""),
                    snippet=item.get("snippet", ""),
                    title=item.get("title"),
                    link=item.get("link"),
                )
            )
        return results

    def get_paa_dict(self, query: str, max_results: int = 10) -> list[dict]:
        """Same as get_paa() but returns plain dicts."""
        return [r.to_dict() for r in self.get_paa(query, max_results)]

    def get_paa_from_url(self, url: str, max_results: int = 10) -> list[PAAResult]:
        """
        Extract the product/page name from a URL (via JSON-LD Product schema)
        and fetch PAA questions for it.

        Args:
            url: Page URL with a Product JSON-LD schema.
            max_results: Maximum number of PAA questions to return.
        """
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        html = resp.text

        start = html.find('"@type": "Product"')
        if start == -1:
            raise ValueError(f"No Product JSON-LD schema found at {url}")

        end = html.find("}", start)
        try:
            product = json.loads("{" + html[start : end + 1] + "}")
            name = product.get("name", "")
        except json.JSONDecodeError as exc:
            raise ValueError(f"Could not parse Product JSON-LD at {url}") from exc

        if not name:
            raise ValueError(f"Product name empty in JSON-LD at {url}")

        return self.get_paa(name, max_results)
