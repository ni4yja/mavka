import argparse
import time
from fetchers.revisions import fetch_articles as fetch_revisions
from fetchers.kontur import fetch_articles as fetch_kontur
from backend.app.services.notion_client import create_page, is_duplicate

FETCHERS = {
    "revisions": fetch_revisions,
    "kontur": fetch_kontur,
}


def article_exists(url: str) -> bool:
    return is_duplicate(url)


def fetch_all(sources=None):
    """
    Отримати статті з усіх (або заданих) джерел.
    Додає поле 'source' та зберігає нові статті в Notion.
    """
    all_articles = []
    selected_sources = sources if sources else FETCHERS.keys()

    for source_name in selected_sources:
        fetch_function = FETCHERS.get(source_name)
        if not fetch_function:
            print(f"❌ Unknown source: {source_name}")
            continue

        print(f"🔎 Fetching from: {source_name}")
        articles_from_source = fetch_function()  # скрейпер повертає список словників

        for article in articles_from_source:
            # Додаємо поле source до кожної статті
            article["source"] = source_name

            # Зберігаємо нові статті в Notion
            if not article_exists(article["url"]):
                create_page(article)
                print(f"✅ Saved: {article.get('title')}")
            else:
                print(f"⚠️ Skipped duplicate: {article.get('title')}")

        all_articles.extend(articles_from_source)

    return all_articles

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
