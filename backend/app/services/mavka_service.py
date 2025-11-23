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
            continue
        records.extend(fetch())
    return records

def save_article(article: dict) -> bool:
    print(f"🔹 Checking article: {article['title']}")
    if not article_exists(article["url"]):
        print(f"🔹 Not duplicate, creating page")
        create_page(article)
        return True
    else:
        print(f"⚠️ Duplicate found, skipping")
    return False

