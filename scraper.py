import httpx
from bs4 import BeautifulSoup

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