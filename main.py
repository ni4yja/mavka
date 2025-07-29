import httpx
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from notion_client import create_page

load_dotenv()

URL = "https://revisionsjournal.com/feed"

def fetch_articles(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; NotionFeeder/1.0)"
    }
    response = httpx.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    records = soup.select(".storyCard")

    results = []
    for record in records:
        author = record.select_one(".storyCard__author")
        title = record.select_one(".storyCard__text")

        results.append({
            "author": author.get_text(strip=True),
            "title": title.get_text(strip=True),
            "url": title["href"]
        })

    return results

if __name__ == "__main__":
    articles = fetch_articles(URL)
    for article in articles:
        create_page(article)