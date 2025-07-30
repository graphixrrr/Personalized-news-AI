from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import ReadingHistory, Article, UserPreference, ArticleFeedback
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta
from collections import Counter

router = APIRouter()

class ReadingAnalytics(BaseModel):
    total_articles_read: int
    total_reading_time: int
    average_reading_time: float
    favorite_categories: List[Dict]
    favorite_sources: List[Dict]
    reading_trends: List[Dict]
    completion_rate: float

@router.get("/{user_id}/reading")
async def get_reading_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get user reading analytics"""
    try:
        # Get reading history
        reading_history = db.query(ReadingHistory).filter(
            ReadingHistory.user_id == user_id
        ).all()
        
        if not reading_history:
            return ReadingAnalytics(
                total_articles_read=0,
                total_reading_time=0,
                average_reading_time=0.0,
                favorite_categories=[],
                favorite_sources=[],
                reading_trends=[],
                completion_rate=0.0
            )
        
        # Calculate basic metrics
        total_articles_read = len(reading_history)
        total_reading_time = sum(h.read_duration or 0 for h in reading_history)
        average_reading_time = total_reading_time / total_articles_read if total_articles_read > 0 else 0
        
        # Get favorite categories
        categories = []
        for history in reading_history:
            if history.article and history.article.category:
                categories.append(history.article.category)
        
        category_counts = Counter(categories)
        favorite_categories = [
            {"category": cat, "count": count}
            for cat, count in category_counts.most_common(5)
        ]
        
        # Get favorite sources
        sources = []
        for history in reading_history:
            if history.article and history.article.source_name:
                sources.append(history.article.source_name)
        
        source_counts = Counter(sources)
        favorite_sources = [
            {"source": source, "count": count}
            for source, count in source_counts.most_common(5)
        ]
        
        # Calculate completion rate
        completed_articles = sum(1 for h in reading_history if h.completed)
        completion_rate = (completed_articles / total_articles_read) * 100 if total_articles_read > 0 else 0
        
        # Get reading trends (last 7 days)
        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_history = [
            h for h in reading_history 
            if h.created_at and h.created_at >= seven_days_ago
        ]
        
        reading_trends = []
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            day_end = day_start + timedelta(days=1)
            
            day_articles = [
                h for h in recent_history
                if h.created_at and day_start <= h.created_at < day_end
            ]
            
            reading_trends.append({
                "date": day_start.strftime("%Y-%m-%d"),
                "articles_read": len(day_articles),
                "reading_time": sum(h.read_duration or 0 for h in day_articles)
            })
        
        reading_trends.reverse()  # Show oldest first
        
        return ReadingAnalytics(
            total_articles_read=total_articles_read,
            total_reading_time=total_reading_time,
            average_reading_time=average_reading_time,
            favorite_categories=favorite_categories,
            favorite_sources=favorite_sources,
            reading_trends=reading_trends,
            completion_rate=completion_rate
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching analytics: {str(e)}")

@router.get("/{user_id}/preferences")
async def get_preference_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get user preference analytics"""
    try:
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).all()
        
        return {
            "preferences": [
                {
                    "category": pref.category,
                    "weight": pref.weight,
                    "created_at": pref.created_at.isoformat() if pref.created_at else None
                }
                for pref in preferences
            ],
            "total_preferences": len(preferences)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching preference analytics: {str(e)}")

@router.get("/{user_id}/feedback")
async def get_feedback_analytics(user_id: int, db: Session = Depends(get_db)):
    """Get user feedback analytics"""
    try:
        feedback = db.query(ArticleFeedback).filter(
            ArticleFeedback.user_id == user_id
        ).all()
        
        if not feedback:
            return {
                "total_feedback": 0,
                "average_rating": 0.0,
                "liked_articles": 0,
                "disliked_articles": 0,
                "rating_distribution": {}
            }
        
        # Calculate metrics
        total_feedback = len(feedback)
        ratings = [f.rating for f in feedback if f.rating]
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        
        liked_articles = sum(1 for f in feedback if f.liked)
        disliked_articles = sum(1 for f in feedback if f.liked is False)
        
        # Rating distribution
        rating_counts = Counter(ratings)
        rating_distribution = {
            str(rating): count for rating, count in rating_counts.items()
        }
        
        return {
            "total_feedback": total_feedback,
            "average_rating": round(average_rating, 2),
            "liked_articles": liked_articles,
            "disliked_articles": disliked_articles,
            "rating_distribution": rating_distribution
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching feedback analytics: {str(e)}")

@router.get("/{user_id}/insights")
async def get_user_insights(user_id: int, db: Session = Depends(get_db)):
    """Get personalized insights for the user"""
    try:
        # Get reading analytics
        reading_analytics = await get_reading_analytics(user_id, db)
        
        # Get preferences
        preferences = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).all()
        
        # Generate insights
        insights = []
        
        # Reading habit insights
        if reading_analytics.total_articles_read > 0:
            if reading_analytics.average_reading_time < 2:
                insights.append({
                    "type": "reading_speed",
                    "title": "Quick Reader",
                    "description": "You tend to read articles quickly. Consider taking more time to absorb complex topics.",
                    "category": "reading_behavior"
                })
            elif reading_analytics.average_reading_time > 8:
                insights.append({
                    "type": "thorough_reader",
                    "title": "Thorough Reader",
                    "description": "You take time to thoroughly read articles. This helps with comprehension and retention.",
                    "category": "reading_behavior"
                })
        
        # Category preference insights
        if reading_analytics.favorite_categories:
            top_category = reading_analytics.favorite_categories[0]
            insights.append({
                "type": "category_preference",
                "title": f"Top Category: {top_category['category'].title()}",
                "description": f"You've read {top_category['count']} articles in this category. Consider exploring related topics.",
                "category": "preferences"
            })
        
        # Completion rate insights
        if reading_analytics.completion_rate < 50:
            insights.append({
                "type": "completion_rate",
                "title": "Article Completion",
                "description": "You complete less than half of the articles you start. Try focusing on shorter articles or topics you're more interested in.",
                "category": "reading_behavior"
            })
        elif reading_analytics.completion_rate > 80:
            insights.append({
                "type": "high_completion",
                "title": "High Completion Rate",
                "description": "You have a high article completion rate. This shows strong engagement with the content.",
                "category": "reading_behavior"
            })
        
        # Preference insights
        if len(preferences) < 3:
            insights.append({
                "type": "preference_diversity",
                "title": "Expand Your Interests",
                "description": "Consider adding more category preferences to get a wider variety of personalized recommendations.",
                "category": "preferences"
            })
        
        return {
            "insights": insights,
            "total_insights": len(insights),
            "reading_analytics": reading_analytics
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}") 