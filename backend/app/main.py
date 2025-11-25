from fastapi import FastAPI
from .routes import articles, sources
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MAVKA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(articles.router, prefix="/api/articles")
app.include_router(sources.router, prefix="/api/sources")
