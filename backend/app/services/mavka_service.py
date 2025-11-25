from fetchers.revisions import fetch_articles as fetch_revisions
from fetchers.kontur import fetch_articles as fetch_kontur
from .notion_client import create_page, is_duplicate

FETCHERS = {
    "revisions": fetch_revisions,
    "kontur": fetch_kontur,
}

def fetch_all(sources=None):
    selected = sources or FETCHERS.keys()
    records = []

    for src in selected:
        fetcher = FETCHERS.get(src)
        if not fetcher:
            continue
        records.extend(fetcher())
    return records

def save_article(article):
    create_page(article)
