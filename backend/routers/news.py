from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from services.news_service import NewsService
from services.ai_service import AIService
from models import Article, ReadingHistory
from datetime import datetime
import json

router = APIRouter()
news_service = NewsService()
ai_service = AIService()

@router.get("/")
async def get_news(
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search query"),
    limit: int = Query(20, description="Number of articles to return"),
    user_id: Optional[int] = Query(None, description="User ID for personalization"),
    db: Session = Depends(get_db)
):
    """Get news articles with optional filtering and personalization"""
    try:
        if search:
            articles = news_service.search_articles(db, search, limit)
        elif category:
            articles = news_service.get_articles_by_category(db, category, limit)
        elif user_id:
            # Get personalized recommendations
            recommendations = ai_service.get_personalized_recommendations(db, user_id, limit)
            articles = [rec["article"] for rec in recommendations]
        else:
            articles = news_service.get_latest_articles(db, limit)
        
        # Convert to response format
        response_articles = []
        for article in articles:
            response_articles.append({
                "id": article.id,
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "image_url": article.image_url,
                "source_name": article.source_name,
                "author": article.author,
                "published_at": article.published_at.isoformat() if article.published_at else None,
                "category": article.category,
                "tags": article.tags,
                "sentiment_score": article.sentiment_score,
                "reading_time": article.reading_time
            })
        
        return {
            "articles": response_articles,
            "total": len(response_articles),
            "category": category,
            "search": search,
            "personalized": user_id is not None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")

@router.get("/categories")
async def get_categories():
    """Get available news categories"""
    categories = [
        {"id": "technology", "name": "Technology", "icon": "💻"},
        {"id": "business", "name": "Business", "icon": "💼"},
        {"id": "science", "name": "Science", "icon": "🔬"},
        {"id": "health", "name": "Health", "icon": "🏥"},
        {"id": "entertainment", "name": "Entertainment", "icon": "🎬"},
        {"id": "sports", "name": "Sports", "icon": "⚽"},
        {"id": "politics", "name": "Politics", "icon": "🏛️"},
        {"id": "general", "name": "General", "icon": "📰"}
    ]
    return {"categories": categories}

@router.get("/trending")
async def get_trending_news(db: Session = Depends(get_db)):
    """Get trending news articles"""
    try:
        # Get articles from the last 24 hours with high engagement
        articles = db.query(Article).filter(
            Article.published_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ).order_by(Article.published_at.desc()).limit(10).all()
        
        response_articles = []
        for article in articles:
            response_articles.append({
                "id": article.id,
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "image_url": article.image_url,
                "source_name": article.source_name,
                "category": article.category,
                "published_at": article.published_at.isoformat() if article.published_at else None
            })
        
        return {"articles": response_articles}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching trending news: {str(e)}")

@router.get("/{article_id}")
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific article by ID"""
    try:
        article = news_service.get_article_by_id(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        return {
            "id": article.id,
            "title": article.title,
            "description": article.description,
            "content": article.content,
            "url": article.url,
            "image_url": article.image_url,
            "source_name": article.source_name,
            "author": article.author,
            "published_at": article.published_at.isoformat() if article.published_at else None,
            "category": article.category,
            "tags": article.tags,
            "sentiment_score": article.sentiment_score,
            "reading_time": article.reading_time
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching article: {str(e)}")

@router.post("/{article_id}/read")
async def mark_article_read(
    article_id: int,
    user_id: int,
    read_duration: Optional[int] = None,
    completed: bool = False,
    db: Session = Depends(get_db)
):
    """Mark an article as read and track reading behavior"""
    try:
        # Check if article exists
        article = news_service.get_article_by_id(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Create or update reading history
        reading_history = ReadingHistory(
            user_id=user_id,
            article_id=article_id,
            read_duration=read_duration,
            completed=completed
        )
        
        db.add(reading_history)
        db.commit()
        
        return {"message": "Article marked as read", "article_id": article_id}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error marking article as read: {str(e)}")

@router.post("/refresh")
async def refresh_news_database(db: Session = Depends(get_db)):
    """Refresh the news database with latest articles from NewsAPI"""
    try:
        count = news_service.refresh_news_database(db)
        return {
            "message": "News database refreshed successfully",
            "articles_added": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error refreshing news database: {str(e)}")

@router.get("/sources/{source_name}")
async def get_articles_by_source(
    source_name: str,
    limit: int = Query(20, description="Number of articles to return"),
    db: Session = Depends(get_db)
):
    """Get articles from a specific source"""
    try:
        articles = news_service.get_articles_by_source(db, source_name, limit)
        
        response_articles = []
        for article in articles:
            response_articles.append({
                "id": article.id,
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "image_url": article.image_url,
                "category": article.category,
                "published_at": article.published_at.isoformat() if article.published_at else None
            })
        
        return {
            "articles": response_articles,
            "source": source_name,
            "total": len(response_articles)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles by source: {str(e)}") 