import os
import httpx
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

def is_duplicate(url: str) -> bool:
    query_payload = {
        "filter": {
            "property": "Link",
            "url": {
                "equals": url
            }
        }
    }

    response = httpx.post(
        f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query",
        headers=HEADERS,
        json=query_payload,
        timeout=30.0
    )

    if response.status_code != 200:
        print(f"❌ Failed to query database: {response.status_code} | {response.text}")
        return False

    data = response.json()
    return len(data.get("results", [])) > 0

def create_page(article: dict):
    if is_duplicate(article["url"]):
        print(f"⚠️ Duplicate found, skipping: {article['title']}")
        return

    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Title": {
                "title": [{"text": {"content": article["title"]}}]
            },
            "Author": {
                "rich_text": [{"text": {"content": article["author"]}}] if article.get("author") else []
            },
            "Link": {
                "url": article["url"]
            },
        }
    }

    response = httpx.post(
        "https://api.notion.com/v1/pages",
        headers=HEADERS,
        json=payload,
        timeout=30.0
    )

    if response.status_code == 200:
        print(f"✅ Added: {article['title']}")
    else:
        print(f"❌ Failed to add: {article['title']} | {response.status_code} | {response.text}")