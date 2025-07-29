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

def create_page(article: dict):
    payload = {
        "parent": {"database_id": NOTION_DATABASE_ID},
        "properties": {
            "Author": {
                "rich_text": [{"text": {"content": article["author"]}}]
            },
            "Title": {
                "title": [{"text": {"content": article["title"]}}]
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
        timeout=10.0
    )

    if response.status_code == 200:
        print(f"✅ Added: {article['title']}")
    else:
        print(f"❌ Failed to add: {article['title']} | {response.status_code} | {response.text}")