#!/usr/bin/env python3
"""
Database setup script for Personalized News AI
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Base, User, UserPreference
from services.news_service import NewsService
from passlib.context import CryptContext

load_dotenv()

def setup_database():
    """Setup database tables and initial data"""
    print("🚀 Setting up Personalized News AI Database...")
    
    # Database configuration
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./personalized_news_ai.db"
    )
    
    # Create engine
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
    )
    
    try:
        # Create all tables
        print("📋 Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        
        # Create session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Create demo user
        print("👤 Creating demo user...")
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # Check if demo user already exists
        existing_user = db.query(User).filter(User.email == "demo@newsai.com").first()
        
        if not existing_user:
            demo_user = User(
                email="demo@newsai.com",
                username="demo_user",
                hashed_password=pwd_context.hash("demo123")
            )
            db.add(demo_user)
            db.commit()
            db.refresh(demo_user)
            print(f"✅ Demo user created with ID: {demo_user.id}")
            
            # Create demo preferences
            print("⚙️ Creating demo preferences...")
            demo_preferences = [
                UserPreference(user_id=demo_user.id, category="technology", weight=1.0),
                UserPreference(user_id=demo_user.id, category="science", weight=0.8),
                UserPreference(user_id=demo_user.id, category="business", weight=0.6)
            ]
            
            for pref in demo_preferences:
                db.add(pref)
            
            db.commit()
            print("✅ Demo preferences created successfully!")
        else:
            print("ℹ️ Demo user already exists")
        
        # Initialize news service and fetch initial articles
        print("📰 Fetching initial news articles...")
        news_service = NewsService()
        articles_added = news_service.refresh_news_database(db)
        print(f"✅ Added {articles_added} articles to database")
        
        print("\n🎉 Database setup completed successfully!")
        print("\n📋 Summary:")
        print(f"   - Database URL: {database_url}")
        print(f"   - Demo user: demo@newsai.com / demo123")
        print(f"   - Articles in database: {articles_added}")
        print("\n🚀 You can now start the application!")
        
    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    setup_database() 