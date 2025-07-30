import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from typing import List, Dict, Tuple, Optional
from sqlalchemy.orm import Session
from models import Article, User, ReadingHistory, UserPreference, ArticleFeedback
import json

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

class AIService:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        self.article_vectors = None
        self.articles_df = None
        
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of text using TextBlob"""
        if not text:
            return 0.0
        
        blob = TextBlob(text)
        return blob.sentiment.polarity
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        """Extract top keywords from text using TF-IDF"""
        if not text:
            return []
        
        processed_text = self.preprocess_text(text)
        if not processed_text:
            return []
        
        # Create TF-IDF vectorizer for single document
        vectorizer = TfidfVectorizer(
            max_features=top_n,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        try:
            tfidf_matrix = vectorizer.fit_transform([processed_text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Get top keywords
            tfidf_scores = tfidf_matrix.toarray()[0]
            keyword_scores = list(zip(feature_names, tfidf_scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return [keyword for keyword, score in keyword_scores if score > 0]
        except:
            return []
    
    def calculate_reading_time(self, text: str) -> int:
        """Estimate reading time in minutes (average 200 words per minute)"""
        if not text:
            return 1
        
        word_count = len(text.split())
        return max(1, round(word_count / 200))
    
    def build_user_profile(self, db: Session, user_id: int) -> Dict:
        """Build comprehensive user profile based on reading history and preferences"""
        # Get user preferences
        preferences = db.query(UserPreference).filter(UserPreference.user_id == user_id).all()
        preference_dict = {pref.category: pref.weight for pref in preferences}
        
        # Get reading history
        reading_history = db.query(ReadingHistory).filter(
            ReadingHistory.user_id == user_id
        ).all()
        
        # Get feedback
        feedback = db.query(ArticleFeedback).filter(
            ArticleFeedback.user_id == user_id
        ).all()
        
        # Analyze reading patterns
        categories_read = {}
        sources_read = {}
        sentiment_preference = 0.0
        avg_reading_time = 0.0
        
        for history in reading_history:
            article = history.article
            if article:
                # Category preference
                if article.category:
                    categories_read[article.category] = categories_read.get(article.category, 0) + 1
                
                # Source preference
                if article.source_name:
                    sources_read[article.source_name] = sources_read.get(article.source_name, 0) + 1
                
                # Sentiment preference
                if article.sentiment_score:
                    sentiment_preference += article.sentiment_score
                
                # Reading time preference
                if article.reading_time:
                    avg_reading_time += article.reading_time
        
        # Calculate averages
        total_articles = len(reading_history)
        if total_articles > 0:
            sentiment_preference /= total_articles
            avg_reading_time /= total_articles
        
        # Get liked articles for content analysis
        liked_articles = [f.article for f in feedback if f.liked and f.article]
        liked_keywords = []
        for article in liked_articles:
            if article.description:
                keywords = self.extract_keywords(article.description, top_n=5)
                liked_keywords.extend(keywords)
        
        return {
            "user_id": user_id,
            "preferences": preference_dict,
            "categories_read": categories_read,
            "sources_read": sources_read,
            "sentiment_preference": sentiment_preference,
            "avg_reading_time": avg_reading_time,
            "liked_keywords": liked_keywords,
            "total_articles_read": total_articles
        }
    
    def content_based_recommendations(self, db: Session, user_id: int, limit: int = 20) -> List[Dict]:
        """Generate content-based recommendations"""
        user_profile = self.build_user_profile(db, user_id)
        
        # Get all articles
        articles = db.query(Article).all()
        
        # Calculate similarity scores
        recommendations = []
        
        for article in articles:
            score = 0.0
            
            # Category preference
            if article.category in user_profile["preferences"]:
                score += user_profile["preferences"][article.category] * 2
            
            if article.category in user_profile["categories_read"]:
                score += user_profile["categories_read"][article.category] * 0.5
            
            # Source preference
            if article.source_name in user_profile["sources_read"]:
                score += user_profile["sources_read"][article.source_name] * 0.3
            
            # Sentiment preference
            if article.sentiment_score and user_profile["sentiment_preference"]:
                sentiment_diff = abs(article.sentiment_score - user_profile["sentiment_preference"])
                score += (1 - sentiment_diff) * 0.5
            
            # Reading time preference
            if article.reading_time and user_profile["avg_reading_time"]:
                time_diff = abs(article.reading_time - user_profile["avg_reading_time"])
                score += (1 - min(time_diff / 10, 1)) * 0.3
            
            # Keyword similarity
            if article.description and user_profile["liked_keywords"]:
                article_keywords = set(self.extract_keywords(article.description, top_n=10))
                liked_keywords_set = set(user_profile["liked_keywords"])
                if article_keywords and liked_keywords_set:
                    keyword_overlap = len(article_keywords.intersection(liked_keywords_set))
                    score += keyword_overlap * 0.2
            
            if score > 0:
                recommendations.append({
                    "article": article,
                    "score": score,
                    "type": "content_based"
                })
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:limit]
    
    def collaborative_filtering(self, db: Session, user_id: int, limit: int = 20) -> List[Dict]:
        """Generate collaborative filtering recommendations"""
        # Get all users and their reading history
        users = db.query(User).all()
        
        # Build user-item matrix
        user_article_matrix = {}
        for user in users:
            user_article_matrix[user.id] = {}
            for history in user.reading_history:
                if history.article:
                    user_article_matrix[user.id][history.article.id] = 1
        
        # Find similar users
        target_user_articles = user_article_matrix.get(user_id, {})
        similar_users = []
        
        for other_user_id, other_user_articles in user_article_matrix.items():
            if other_user_id != user_id:
                # Calculate Jaccard similarity
                intersection = len(set(target_user_articles.keys()) & set(other_user_articles.keys()))
                union = len(set(target_user_articles.keys()) | set(other_user_articles.keys()))
                
                if union > 0:
                    similarity = intersection / union
                    if similarity > 0:
                        similar_users.append((other_user_id, similarity))
        
        # Sort by similarity
        similar_users.sort(key=lambda x: x[1], reverse=True)
        
        # Get recommendations from similar users
        recommendations = []
        seen_articles = set(target_user_articles.keys())
        
        for similar_user_id, similarity in similar_users[:10]:  # Top 10 similar users
            similar_user_articles = user_article_matrix[similar_user_id]
            
            for article_id in similar_user_articles:
                if article_id not in seen_articles:
                    article = db.query(Article).filter(Article.id == article_id).first()
                    if article:
                        recommendations.append({
                            "article": article,
                            "score": similarity,
                            "type": "collaborative"
                        })
                        seen_articles.add(article_id)
        
        # Sort by score and return top recommendations
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:limit]
    
    def hybrid_recommendations(self, db: Session, user_id: int, limit: int = 20) -> List[Dict]:
        """Generate hybrid recommendations combining content-based and collaborative filtering"""
        content_based = self.content_based_recommendations(db, user_id, limit)
        collaborative = self.collaborative_filtering(db, user_id, limit)
        
        # Combine recommendations
        article_scores = {}
        
        # Add content-based scores
        for rec in content_based:
            article_id = rec["article"].id
            article_scores[article_id] = {
                "article": rec["article"],
                "content_score": rec["score"],
                "collaborative_score": 0.0,
                "hybrid_score": rec["score"] * 0.7  # Weight content-based more
            }
        
        # Add collaborative scores
        for rec in collaborative:
            article_id = rec["article"].id
            if article_id in article_scores:
                article_scores[article_id]["collaborative_score"] = rec["score"]
                article_scores[article_id]["hybrid_score"] += rec["score"] * 0.3
            else:
                article_scores[article_id] = {
                    "article": rec["article"],
                    "content_score": 0.0,
                    "collaborative_score": rec["score"],
                    "hybrid_score": rec["score"] * 0.3
                }
        
        # Convert to list and sort by hybrid score
        recommendations = []
        for article_id, scores in article_scores.items():
            recommendations.append({
                "article": scores["article"],
                "score": scores["hybrid_score"],
                "type": "hybrid",
                "content_score": scores["content_score"],
                "collaborative_score": scores["collaborative_score"]
            })
        
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        return recommendations[:limit]
    
    def get_personalized_recommendations(self, db: Session, user_id: int, limit: int = 20) -> List[Dict]:
        """Get personalized recommendations using hybrid approach"""
        return self.hybrid_recommendations(db, user_id, limit)
    
    def analyze_article(self, article_data: Dict) -> Dict:
        """Analyze article content and extract features"""
        title = article_data.get("title", "")
        description = article_data.get("description", "")
        content = article_data.get("content", "")
        
        # Combine text for analysis
        full_text = f"{title} {description} {content}"
        
        # Analyze sentiment
        sentiment_score = self.analyze_sentiment(full_text)
        
        # Extract keywords
        keywords = self.extract_keywords(full_text, top_n=15)
        
        # Calculate reading time
        reading_time = self.calculate_reading_time(full_text)
        
        # Determine category based on keywords
        category = self.categorize_article(keywords, title, description)
        
        return {
            "sentiment_score": sentiment_score,
            "keywords": keywords,
            "reading_time": reading_time,
            "category": category
        }
    
    def categorize_article(self, keywords: List[str], title: str, description: str) -> str:
        """Categorize article based on keywords and content"""
        categories = {
            "technology": ["tech", "technology", "software", "ai", "artificial intelligence", "machine learning", "programming", "startup", "innovation"],
            "business": ["business", "economy", "finance", "market", "investment", "stock", "trading", "company", "corporate"],
            "politics": ["politics", "government", "election", "policy", "democrat", "republican", "congress", "senate", "president"],
            "sports": ["sports", "football", "basketball", "baseball", "soccer", "tennis", "olympics", "championship", "game"],
            "entertainment": ["entertainment", "movie", "music", "celebrity", "hollywood", "film", "actor", "actress", "award"],
            "health": ["health", "medical", "medicine", "disease", "treatment", "hospital", "doctor", "patient", "covid"],
            "science": ["science", "research", "study", "discovery", "experiment", "laboratory", "scientist", "physics", "chemistry"]
        }
        
        # Check title and description for category keywords
        text_to_check = f"{title} {description}".lower()
        
        for category, keywords_list in categories.items():
            for keyword in keywords_list:
                if keyword in text_to_check:
                    return category
        
        # Default category
        return "general" 