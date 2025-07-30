from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.ai_service import AIService
from pydantic import BaseModel
from typing import List, Dict, Optional

router = APIRouter()
ai_service = AIService()

class RecommendationRequest(BaseModel):
    user_id: int
    limit: int = 20
    algorithm: str = "hybrid"  # "content_based", "collaborative", "hybrid"

class ArticleAnalysisRequest(BaseModel):
    title: str
    description: str
    content: Optional[str] = ""

@router.post("/recommendations")
async def get_ai_recommendations(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):
    """Get AI-powered article recommendations"""
    try:
        if request.algorithm == "content_based":
            recommendations = ai_service.content_based_recommendations(
                db, request.user_id, request.limit
            )
        elif request.algorithm == "collaborative":
            recommendations = ai_service.collaborative_filtering(
                db, request.user_id, request.limit
            )
        else:  # hybrid
            recommendations = ai_service.hybrid_recommendations(
                db, request.user_id, request.limit
            )
        
        # Format response
        formatted_recommendations = []
        for rec in recommendations:
            article = rec["article"]
            formatted_recommendations.append({
                "article": {
                    "id": article.id,
                    "title": article.title,
                    "description": article.description,
                    "url": article.url,
                    "image_url": article.image_url,
                    "source_name": article.source_name,
                    "category": article.category,
                    "sentiment_score": article.sentiment_score,
                    "reading_time": article.reading_time
                },
                "score": rec["score"],
                "type": rec["type"],
                "confidence": min(rec["score"] * 100, 100)  # Convert to percentage
            })
        
        return {
            "recommendations": formatted_recommendations,
            "algorithm": request.algorithm,
            "total": len(formatted_recommendations)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

@router.post("/analyze-article")
async def analyze_article(request: ArticleAnalysisRequest):
    """Analyze article content using AI"""
    try:
        article_data = {
            "title": request.title,
            "description": request.description,
            "content": request.content
        }
        
        analysis = ai_service.analyze_article(article_data)
        
        return {
            "sentiment_score": analysis["sentiment_score"],
            "keywords": analysis["keywords"],
            "reading_time": analysis["reading_time"],
            "category": analysis["category"],
            "sentiment_label": "positive" if analysis["sentiment_score"] > 0.1 else "negative" if analysis["sentiment_score"] < -0.1 else "neutral"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing article: {str(e)}")

@router.get("/user-profile/{user_id}")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get AI-generated user profile"""
    try:
        profile = ai_service.build_user_profile(db, user_id)
        
        return {
            "user_id": profile["user_id"],
            "preferences": profile["preferences"],
            "categories_read": profile["categories_read"],
            "sources_read": profile["sources_read"],
            "sentiment_preference": profile["sentiment_preference"],
            "avg_reading_time": profile["avg_reading_time"],
            "liked_keywords": profile["liked_keywords"],
            "total_articles_read": profile["total_articles_read"],
            "profile_strength": min(len(profile["categories_read"]) * 10, 100)  # Profile completeness score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building user profile: {str(e)}")

@router.get("/algorithms")
async def get_available_algorithms():
    """Get available recommendation algorithms"""
    return {
        "algorithms": [
            {
                "id": "content_based",
                "name": "Content-Based Filtering",
                "description": "Recommends articles similar to what you've liked before based on content features",
                "strengths": ["Personalized", "No cold start for new users", "Explainable"],
                "weaknesses": ["Limited discovery", "Feature engineering required"]
            },
            {
                "id": "collaborative",
                "name": "Collaborative Filtering",
                "description": "Recommends articles based on what similar users have liked",
                "strengths": ["Discovers new content", "No content analysis needed"],
                "weaknesses": ["Cold start problem", "Sparsity issues"]
            },
            {
                "id": "hybrid",
                "name": "Hybrid Approach",
                "description": "Combines content-based and collaborative filtering for better recommendations",
                "strengths": ["Best of both worlds", "More accurate", "Better coverage"],
                "weaknesses": ["More complex", "Higher computational cost"]
            }
        ]
    }

@router.get("/insights/{user_id}")
async def get_ai_insights(user_id: int, db: Session = Depends(get_db)):
    """Get AI-generated insights about user behavior"""
    try:
        profile = ai_service.build_user_profile(db, user_id)
        
        insights = []
        
        # Reading pattern insights
        if profile["total_articles_read"] > 0:
            if profile["avg_reading_time"] < 3:
                insights.append({
                    "type": "reading_speed",
                    "title": "Fast Reader",
                    "description": "You read articles quickly. Consider longer, in-depth articles for complex topics.",
                    "confidence": 85
                })
            elif profile["avg_reading_time"] > 10:
                insights.append({
                    "type": "reading_depth",
                    "title": "Deep Reader",
                    "description": "You prefer thorough, detailed articles. Our AI will prioritize longer content.",
                    "confidence": 90
                })
        
        # Category preference insights
        if profile["categories_read"]:
            top_category = max(profile["categories_read"].items(), key=lambda x: x[1])
            insights.append({
                "type": "category_preference",
                "title": f"Top Interest: {top_category[0].title()}",
                "description": f"You've read {top_category[1]} articles in this category. Consider exploring related topics.",
                "confidence": 95
            })
        
        # Sentiment preference insights
        if profile["sentiment_preference"] > 0.2:
            insights.append({
                "type": "sentiment_preference",
                "title": "Positive Content Preference",
                "description": "You tend to prefer positive or uplifting content.",
                "confidence": 80
            })
        elif profile["sentiment_preference"] < -0.2:
            insights.append({
                "type": "sentiment_preference",
                "title": "Critical Content Preference",
                "description": "You prefer analytical or critical content.",
                "confidence": 80
            })
        
        # Source preference insights
        if profile["sources_read"]:
            top_source = max(profile["sources_read"].items(), key=lambda x: x[1])
            insights.append({
                "type": "source_preference",
                "title": f"Preferred Source: {top_source[0]}",
                "description": f"You frequently read from {top_source[0]}. We'll prioritize content from trusted sources.",
                "confidence": 85
            })
        
        return {
            "insights": insights,
            "total_insights": len(insights),
            "profile_strength": min(len(profile["categories_read"]) * 10, 100)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating AI insights: {str(e)}") 