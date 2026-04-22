"""CLI entry point for seo-paa."""

import argparse
import json
import sys

from .extractor import PAAScraper


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="seo-paa",
        description="Extract People Also Ask questions from Google SERP",
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("--api-key", help="SerpAPI key (or set SERPAPI_KEY env var)")
    parser.add_argument("--lang", default="en", help="Language code (default: en)")
    parser.add_argument("--country", default="us", help="Country code (default: us)")
    parser.add_argument("--max", type=int, default=10, dest="max_results",
                        help="Max PAA results (default: 10)")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    try:
        scraper = PAAScraper(
            api_key=args.api_key,
            lang=args.lang,
            country=args.country,
        )
        results = scraper.get_paa(args.query, max_results=args.max_results)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2, ensure_ascii=False))
    else:
        for i, r in enumerate(results, 1):
            print(f"{i}. {r.question}")
            if r.snippet:
                print(f"   {r.snippet}\n")


if __name__ == "__main__":
    main()
