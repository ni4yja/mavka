import os
import httpx
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

env_file = Path.cwd() / ".env.test"
load_dotenv(env_file)

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATA_SOURCE_ID = os.getenv("NOTION_DATA_SOURCE_ID")

print("DEBUG DATA_SOURCE_ID:", os.getenv("NOTION_DATA_SOURCE_ID"))

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2025-09-03",
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
        f"https://api.notion.com/v1/data_sources/{NOTION_DATA_SOURCE_ID}/query",
        headers=HEADERS,
        json=query_payload,
        timeout=30.0
    )

    if response.status_code != 200:
        print(f"❌ Failed to query database: {response.status_code} | {response.text}")
        return False

    data = response.json()
    return len(data.get("results", [])) > 0

def is_archive(status: str) -> bool:
    return status != "todo"

def create_page(article: dict):
    if is_duplicate(article["url"]):
        print(f"⚠️ Duplicate found, skipping: {article['title']}")
        return

    payload = {
        "parent": {
            "type": "data_source_id",
            "data_source_id": NOTION_DATA_SOURCE_ID,
        },
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
            "Status": {
                "select": {"name": "todo"}
            },
            "Date": {
                "date": {
                    "start": datetime.now(ZoneInfo("Europe/Warsaw")).isoformat()
                }
            }
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