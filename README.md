# seo-paa

[![PyPI version](https://badge.fury.io/py/seo-paa.svg)](https://pypi.org/project/seo-paa/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Extract **People Also Ask (PAA)** questions from Google SERP via SerpAPI — for SEO content research and topic clustering.

## Install

```bash
pip install seo-paa
```

## Usage

### Python API

```python
from seo_paa import PAAScraper

scraper = PAAScraper(api_key="your_serpapi_key", lang="en", country="us")

results = scraper.get_paa("best surf camp senegal", max_results=10)
for r in results:
    print(r.question)
    print(r.snippet)
    print()
```

Output:
```
Is Senegal good for surfing?
Yes, Ngor Island is considered one of West Africa's best surf spots...

Best time to surf in Senegal?
The main surf season runs from November to April...
```

### Return as plain dicts (for pandas / JSON)

```python
import pandas as pd

data = scraper.get_paa_dict("surf camp west africa")
df = pd.DataFrame(data)
df.to_csv("paa_results.csv", index=False)
```

### Extract from a product URL

Extracts the product name from a page's JSON-LD Product schema, then fetches PAA:

```python
results = scraper.get_paa_from_url("https://example.com/product/surf-board")
```

### CLI

```bash
# Basic usage (set SERPAPI_KEY env var)
seo-paa "best surf camp senegal"

# With options
seo-paa "best surf camp" --lang fr --country fr --max 5

# JSON output (pipe to jq, save to file, etc.)
seo-paa "surf senegal" --json | jq '.[].question'
```

## Configuration

| Parameter | Description | Default |
|---|---|---|
| `api_key` | SerpAPI key (or `SERPAPI_KEY` env var) | — |
| `lang` | Language code (`en`, `fr`, `es`…) | `"en"` |
| `country` | Country code (`us`, `fr`, `gb`…) | `"us"` |
| `location` | Full location string (e.g. `"Paris,Ile-de-France,France"`) | `None` |

## Why PAA matters for SEO

PAA questions are a direct signal of what users ask around a topic. Mining them at scale lets you:

- Build FAQ sections that target featured snippets
- Identify content gaps vs. competitors
- Cluster topics for pillar/cluster content strategies
- Feed into content briefs and internal linking maps

## Requirements

- Python 3.9+
- SerpAPI key ([serpapi.com](https://serpapi.com))

## License

MIT — [Simon Azoulay](https://github.com/monsiaz)
