import argparse
import time
from fetchers.revisions import fetch_articles as fetch_revisions
from fetchers.kontur import fetch_articles as fetch_kontur
from notion_client import create_page, is_duplicate

FETCHERS = {
    "revisions": fetch_revisions,
    "kontur": fetch_kontur,
}


def article_exists(url: str) -> bool:
    return is_duplicate(url)


def fetch_all(sources=None):
    records = []
    selected_sources = sources if sources else FETCHERS.keys()

    for name in selected_sources:
        fetch = FETCHERS.get(name)
        if not fetch:
            print(f"❌ Unknown source: {name}")
            continue
        print(f"🔎 Fetching from: {name}")
        records.extend(fetch())
    return records


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and store articles in Notion")
    parser.add_argument(
        "--source", "-s", nargs="+",
        help="List of sources to fetch (e.g. revisions kontur). Fetches all if omitted."
    )
    args = parser.parse_args()

    articles = fetch_all(args.source)
    for article in articles:
        if not article_exists(article["url"]):
            create_page(article)
            time.sleep(1)
        else:
            print(f"⚠️ Skipped duplicate: {article['title']}")
