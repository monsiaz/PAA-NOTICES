"""Basic tests for seo-paa (no live API calls)."""

import pytest
from unittest.mock import patch, MagicMock

from seo_paa import PAAScraper
from seo_paa.extractor import PAAResult


def test_paa_result_to_dict():
    r = PAAResult(question="What is SEO?", snippet="Search engine optimization.")
    d = r.to_dict()
    assert d["question"] == "What is SEO?"
    assert d["snippet"] == "Search engine optimization."
    assert d["title"] is None


def test_scraper_requires_api_key(monkeypatch):
    monkeypatch.delenv("SERPAPI_KEY", raising=False)
    with pytest.raises(ValueError, match="SerpAPI key required"):
        PAAScraper()


def test_get_paa_parses_response():
    mock_response = {
        "related_questions": [
            {"question": "Is Senegal good for surfing?", "snippet": "Yes, Ngor Island is world-class."},
            {"question": "Best time to surf in Senegal?", "snippet": "November to April."},
        ]
    }
    with patch("seo_paa.extractor.requests.get") as mock_get:
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: mock_response,
        )
        mock_get.return_value.raise_for_status = lambda: None
        scraper = PAAScraper(api_key="test_key")
        results = scraper.get_paa("surf senegal")

    assert len(results) == 2
    assert results[0].question == "Is Senegal good for surfing?"
    assert results[1].snippet == "November to April."


def test_get_paa_dict():
    mock_response = {"related_questions": [{"question": "Q?", "snippet": "A."}]}
    with patch("seo_paa.extractor.requests.get") as mock_get:
        mock_get.return_value = MagicMock(json=lambda: mock_response)
        mock_get.return_value.raise_for_status = lambda: None
        scraper = PAAScraper(api_key="test_key")
        result = scraper.get_paa_dict("test")
    assert isinstance(result[0], dict)
    assert "question" in result[0]
