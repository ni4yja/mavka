from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from collections import Counter
from backend.app.services.mavka_service import fetch_all, save_article

router = APIRouter(tags=["articles"])

# Узгоджені джерела (список /api/sources)
KNOWN_SOURCES = ["revisions", "kontur"]

class ArticleCreate(BaseModel):
    title: str
    author: Optional[str] = None
    url: str
    status: Optional[str] = "todo"
    date: Optional[str] = None
    source: Optional[str]

class ArticleResponse(BaseModel):
    total: int
    articles: List[dict] = []

def detect_source(url: str) -> str:
    """Визначає джерело по URL або повертає 'unknown'"""
    url_lower = url.lower()
    for src in KNOWN_SOURCES:
        if src in url_lower:
            return src
    return "unknown"

def enrich_articles_with_source(articles: List[dict]) -> List[dict]:
    """Гарантує наявність поля 'source' у кожної статті"""
    for article in articles:
        if not article.get("source"):
            article["source"] = detect_source(article.get("url", ""))
    return articles

@router.get("/", response_model=ArticleResponse)
def list_articles(sources: Optional[str] = Query(None, description="Джерела через кому")):
    """Список статей з опційним фільтром по джерелах"""
    try:
        articles = fetch_all()
        articles = enrich_articles_with_source(articles)

        if sources:
            sources_list = [s.strip() for s in sources.split(",")]
            articles = [a for a in articles if a.get("source") in sources_list]

        return {"total": len(articles), "articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка при отриманні статей: {str(e)}")

@router.get("/stats")
def get_stats():
    """Статистика по джерелах"""
    try:
        articles = fetch_all()
        articles = enrich_articles_with_source(articles)

        counter = Counter()
        for article in articles:
            src = article.get("source")
            if src not in KNOWN_SOURCES:
                src = "unknown"
            counter[src] += 1

        return {"total": len(articles), "by_source": dict(counter)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка при розрахунку статистики: {str(e)}")

@router.post("/save")
def save_article_endpoint(article: ArticleCreate):
    """Збереження нової статті"""
    try:
        if not article.title or not article.url:
            raise HTTPException(status_code=400, detail="Вимагаються поля: title, url")

        if not article.source:
            article.source = detect_source(article.url)

        saved = save_article(article.dict())
        if saved:
            return {"success": True, "message": f"Статтю '{article.title}' збережено"}
        else:
            return {"success": False, "message": f"Дубль: '{article.title}'"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Помилка при збереженні статті: {str(e)}")
