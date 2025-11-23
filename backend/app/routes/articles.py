from fastapi import APIRouter
from app.services.mavka_service import fetch_all, save_article

router = APIRouter()

@router.get("/")
def list_articles(source: str = None):
    sources = source.split() if source else None
    return fetch_all(sources)

@router.post("/save")
def save_article_endpoint(article: dict):
    saved = save_article(article)
    return {"saved": saved}
