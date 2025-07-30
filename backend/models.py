from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import json

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    preferences = relationship("UserPreference", back_populates="user")
    reading_history = relationship("ReadingHistory", back_populates="user")
    article_feedback = relationship("ArticleFeedback", back_populates="user")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    content = Column(Text)
    url = Column(String, unique=True, index=True)
    image_url = Column(String)
    source_name = Column(String)
    author = Column(String)
    published_at = Column(DateTime(timezone=True))
    category = Column(String, index=True)
    tags = Column(JSON)  # Store as JSON array
    sentiment_score = Column(Float)
    reading_time = Column(Integer)  # Estimated reading time in minutes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    reading_history = relationship("ReadingHistory", back_populates="article")
    article_feedback = relationship("ArticleFeedback", back_populates="article")

class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String, index=True)
    weight = Column(Float, default=1.0)  # Preference weight (0-1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="preferences")

class ReadingHistory(Base):
    __tablename__ = "reading_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))
    read_duration = Column(Integer)  # Time spent reading in seconds
    completed = Column(Boolean, default=False)  # Whether user finished reading
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="reading_history")
    article = relationship("Article", back_populates="reading_history")

class ArticleFeedback(Base):
    __tablename__ = "article_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))
    rating = Column(Integer)  # 1-5 rating
    liked = Column(Boolean)  # Thumbs up/down
    feedback_text = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="article_feedback")
    article = relationship("Article", back_populates="article_feedback")

class AIRecommendation(Base):
    __tablename__ = "ai_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    article_id = Column(Integer, ForeignKey("articles.id"))
    confidence_score = Column(Float)  # AI confidence in recommendation (0-1)
    recommendation_type = Column(String)  # "content_based", "collaborative", "hybrid"
    features_used = Column(JSON)  # Features used for recommendation
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")
    article = relationship("Article") 