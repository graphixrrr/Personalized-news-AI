#!/usr/bin/env python3
"""
Script to populate the database with sample articles for testing
"""

import sys
import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Article, Base
import random

# Create database tables
Base.metadata.create_all(bind=engine)

def create_sample_articles():
    """Create sample articles for testing"""
    
    sample_articles = [
        {
            "title": "AI Breakthrough: New Machine Learning Model Achieves 99% Accuracy",
            "description": "Researchers at Stanford University have developed a revolutionary machine learning model that achieves unprecedented accuracy in image recognition tasks.",
            "content": "The new model, called DeepVision-X, uses a novel neural network architecture that combines convolutional and transformer layers. This breakthrough could revolutionize fields from medical imaging to autonomous vehicles.",
            "url": "https://example.com/ai-breakthrough",
            "image_url": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800",
            "source_name": "Tech News Daily",
            "author": "Dr. Sarah Johnson",
            "published_at": datetime.now() - timedelta(hours=2),
            "category": "technology",
            "tags": ["AI", "machine learning", "research"],
            "sentiment_score": 0.8,
            "reading_time": 5
        },
        {
            "title": "Global Markets Rally as Tech Stocks Surge",
            "description": "Major stock indices around the world saw significant gains today, led by strong performance in the technology sector.",
            "content": "The S&P 500 and NASDAQ both reached new record highs as investors showed renewed confidence in tech companies. Analysts attribute the rally to strong quarterly earnings reports.",
            "url": "https://example.com/markets-rally",
            "image_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=800",
            "source_name": "Financial Times",
            "author": "Michael Chen",
            "published_at": datetime.now() - timedelta(hours=4),
            "category": "business",
            "tags": ["markets", "stocks", "finance"],
            "sentiment_score": 0.6,
            "reading_time": 3
        },
        {
            "title": "New Study Reveals Benefits of Mediterranean Diet",
            "description": "A comprehensive study involving over 10,000 participants shows significant health benefits from following a Mediterranean diet.",
            "content": "The research, published in the Journal of Nutrition, found that participants who followed a Mediterranean diet had 30% lower risk of heart disease and improved cognitive function.",
            "url": "https://example.com/mediterranean-diet",
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
            "source_name": "Health Weekly",
            "author": "Dr. Emily Rodriguez",
            "published_at": datetime.now() - timedelta(hours=6),
            "category": "health",
            "tags": ["nutrition", "health", "research"],
            "sentiment_score": 0.7,
            "reading_time": 4
        },
        {
            "title": "SpaceX Successfully Launches Satellite Constellation",
            "description": "SpaceX's Falcon 9 rocket successfully deployed another batch of Starlink satellites into low Earth orbit.",
            "content": "The launch marks the company's 50th successful mission this year. The Starlink constellation now provides internet coverage to remote areas around the world.",
            "url": "https://example.com/spacex-launch",
            "image_url": "https://images.unsplash.com/photo-1446776877081-d282a0f896e2?w=800",
            "source_name": "Space News",
            "author": "Alex Thompson",
            "published_at": datetime.now() - timedelta(hours=8),
            "category": "science",
            "tags": ["space", "satellites", "technology"],
            "sentiment_score": 0.9,
            "reading_time": 6
        },
        {
            "title": "Championship Game Ends in Dramatic Overtime Victory",
            "description": "The championship game went into triple overtime before the underdog team secured a stunning victory with a last-second field goal.",
            "content": "Fans were treated to one of the most exciting games in recent memory, with both teams showing incredible skill and determination throughout the match.",
            "url": "https://example.com/championship-game",
            "image_url": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800",
            "source_name": "Sports Central",
            "author": "James Wilson",
            "published_at": datetime.now() - timedelta(hours=10),
            "category": "sports",
            "tags": ["football", "championship", "overtime"],
            "sentiment_score": 0.8,
            "reading_time": 4
        },
        {
            "title": "New Blockbuster Movie Breaks Box Office Records",
            "description": "The highly anticipated superhero movie has shattered previous box office records, earning over $200 million in its opening weekend.",
            "content": "Critics and audiences alike are praising the film's stunning visual effects and compelling storyline. The movie's success is expected to influence future productions in the genre.",
            "url": "https://example.com/blockbuster-movie",
            "image_url": "https://images.unsplash.com/photo-1489599835382-957593cb2371?w=800",
            "source_name": "Entertainment Weekly",
            "author": "Lisa Park",
            "published_at": datetime.now() - timedelta(hours=12),
            "category": "entertainment",
            "tags": ["movies", "box office", "superhero"],
            "sentiment_score": 0.7,
            "reading_time": 3
        }
    ]
    
    db = next(get_db())
    
    try:
        # Check if articles already exist
        existing_count = db.query(Article).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} articles. Skipping sample data creation.")
            return
        
        # Create sample articles
        for article_data in sample_articles:
            article = Article(**article_data)
            db.add(article)
        
        db.commit()
        print(f"✅ Successfully created {len(sample_articles)} sample articles!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating sample articles: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Creating sample articles for testing...")
    create_sample_articles()
    print("✅ Sample data creation complete!") 