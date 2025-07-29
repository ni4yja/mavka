from scraper import fetch_articles
from notion_client import create_page

URL = "https://revisionsjournal.com/feed"

if __name__ == "__main__":
    articles = fetch_articles(URL)
    for article in articles:
        create_page(article)