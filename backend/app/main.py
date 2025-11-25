from fastapi import FastAPI
from .routes import articles, sources

app = FastAPI(title="MAVKA API")

app.include_router(articles.router, prefix="/api/articles")
app.include_router(sources.router, prefix="/api/sources")
