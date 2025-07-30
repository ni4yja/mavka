import httpx
from bs4 import BeautifulSoup

FEED_URL = "https://kontur.media/"

def fetch_articles():
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; NotionFeeder/1.0)"
    }
    response = httpx.get(FEED_URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    records = soup.select(".post-card")

    results = []

    for record in records:
        text = record.select_one(".entry-title").get_text(strip=True)
        link = record.select_one(".entry-title a")

        dot_index = int(text.find('.'))

        author = text[0: dot_index]
        title = text[dot_index + 2: len(text)]

        results.append({
            "author": author,
            "title": title,
            "url": link["href"]
        })

    return results