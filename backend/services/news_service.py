import requests
import os
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Article
from services.ai_service import AIService
from services.content_fetcher import ContentFetcher
import json

class NewsService:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY", "6ed6af63cc174b03a5ee8eb8dfad6ca2")
        self.base_url = "https://newsapi.org/v2"
        self.ai_service = AIService()
        self.content_fetcher = ContentFetcher()
        
    def fetch_top_headlines(self, country: str = "us", category: Optional[str] = None, page_size: int = 100) -> List[Dict]:
        """Fetch top headlines from NewsAPI"""
        url = f"{self.base_url}/top-headlines"
        params = {
            "apiKey": self.api_key,
            "country": country,
            "pageSize": page_size
        }
        
        if category:
            params["category"] = category
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "ok":
                return data["articles"]
            else:
                print(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return []
    
    def fetch_everything(self, query: str, from_date: Optional[str] = None, sort_by: str = "publishedAt", page_size: int = 100) -> List[Dict]:
        """Fetch articles from everything endpoint"""
        url = f"{self.base_url}/everything"
        params = {
            "apiKey": self.api_key,
            "q": query,
            "sortBy": sort_by,
            "pageSize": page_size,
            "language": "en"
        }
        
        if from_date:
            params["from"] = from_date
            
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["status"] == "ok":
                return data["articles"]
            else:
                print(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                return []
                
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")
            return []
    
    def fetch_by_category(self, category: str, country: str = "us", page_size: int = 50) -> List[Dict]:
        """Fetch articles by category (case-insensitive)"""
        categories = [
            "business", "entertainment", "general", "health", 
            "science", "sports", "technology"
        ]
        
        # Convert category to lowercase for case-insensitive validation
        category_lower = category.lower() if category else ""
        
        if category_lower not in categories:
            print(f"Invalid category: {category}")
            return []
            
        return self.fetch_top_headlines(country=country, category=category_lower, page_size=page_size)
    
    def fetch_trending_topics(self) -> List[Dict]:
        """Fetch articles on trending topics"""
        trending_queries = [
            "artificial intelligence",
            "climate change",
            "space exploration",
            "cryptocurrency",
            "electric vehicles",
            "renewable energy",
            "mental health",
            "remote work"
        ]
        
        all_articles = []
        for query in trending_queries:
            articles = self.fetch_everything(query, page_size=20)
            all_articles.extend(articles)
            
        return all_articles
    
    def process_article(self, article_data: Dict) -> Dict:
        """Process and analyze a single article"""
        # Analyze article with AI
        analysis = self.ai_service.analyze_article(article_data)
        
        # Parse published date
        published_at = None
        if article_data.get("publishedAt"):
            try:
                published_at = datetime.fromisoformat(article_data["publishedAt"].replace("Z", "+00:00"))
            except:
                published_at = datetime.now()
        
        # Try to fetch full content if not available
        content = article_data.get("content", "")
        if not content or len(content) < 200:  # If content is too short, try to fetch full content
            try:
                full_content = self.content_fetcher.fetch_full_content(article_data.get("url", ""))
                if full_content:
                    content = full_content
                    print(f"✅ Fetched full content for: {article_data.get('title', 'Unknown')}")
                else:
                    print(f"⚠️ Could not fetch full content for: {article_data.get('title', 'Unknown')}")
            except Exception as e:
                print(f"❌ Error fetching content for {article_data.get('title', 'Unknown')}: {e}")
        
        processed_article = {
            "title": article_data.get("title", ""),
            "description": article_data.get("description", ""),
            "content": content,
            "url": article_data.get("url", ""),
            "image_url": article_data.get("urlToImage", ""),
            "source_name": article_data.get("source", {}).get("name", ""),
            "author": article_data.get("author", ""),
            "published_at": published_at,
            "category": analysis["category"],
            "tags": analysis["keywords"],
            "sentiment_score": analysis["sentiment_score"],
            "reading_time": analysis["reading_time"]
        }
        
        return processed_article
    
    def save_articles_to_db(self, db: Session, articles: List[Dict]) -> List[Article]:
        """Save processed articles to database"""
        saved_articles = []
        
        for article_data in articles:
            try:
                # Check if article already exists
                existing_article = db.query(Article).filter(Article.url == article_data["url"]).first()
                if existing_article:
                    continue
                    
                # Create new article
                article = Article(
                    title=article_data["title"],
                    description=article_data["description"],
                    content=article_data["content"],
                    url=article_data["url"],
                    image_url=article_data["image_url"],
                    source_name=article_data["source_name"],
                    author=article_data["author"],
                    published_at=article_data["published_at"],
                    category=article_data["category"],
                    tags=article_data["tags"],
                    sentiment_score=article_data["sentiment_score"],
                    reading_time=article_data["reading_time"]
                )
                
                db.add(article)
                saved_articles.append(article)
                
            except Exception as e:
                print(f"Error processing article {article_data.get('title', 'Unknown')}: {e}")
                continue
        
        try:
            db.commit()
            print(f"Saved {len(saved_articles)} new articles to database")
        except Exception as e:
            db.rollback()
            print(f"Error saving articles: {e}")
            # Try to save articles one by one to avoid losing all articles due to one bad one
            saved_articles = []
            for article_data in articles:
                try:
                    existing_article = db.query(Article).filter(Article.url == article_data["url"]).first()
                    if existing_article:
                        continue
                        
                    article = Article(
                        title=article_data["title"],
                        description=article_data["description"],
                        content=article_data["content"],
                        url=article_data["url"],
                        image_url=article_data["image_url"],
                        source_name=article_data["source_name"],
                        author=article_data["author"],
                        published_at=article_data["published_at"],
                        category=article_data["category"],
                        tags=article_data["tags"],
                        sentiment_score=article_data["sentiment_score"],
                        reading_time=article_data["reading_time"]
                    )
                    
                    db.add(article)
                    db.commit()
                    saved_articles.append(article)
                    
                except Exception as e:
                    db.rollback()
                    print(f"Failed to save article {article_data.get('title', 'Unknown')}: {e}")
                    continue
            
        return saved_articles
    
    def refresh_news_database(self, db: Session) -> int:
        """Refresh the news database with latest articles"""
        print("🔄 Refreshing news database...")
        
        # Fetch articles from different categories
        categories = ["technology", "business", "science", "health", "entertainment", "sports"]
        all_articles = []
        
        for category in categories:
            print(f"Fetching {category} articles...")
            articles = self.fetch_by_category(category, page_size=30)
            all_articles.extend(articles)
        
        # Fetch trending topics
        print("Fetching trending topics...")
        trending_articles = self.fetch_trending_topics()
        all_articles.extend(trending_articles)
        
        # Process articles
        processed_articles = []
        for article in all_articles:
            processed = self.process_article(article)
            if processed["title"] and processed["url"]:  # Only save articles with title and URL
                processed_articles.append(processed)
        
        # Save to database
        saved_articles = self.save_articles_to_db(db, processed_articles)
        
        print(f"✅ Database refresh complete. Added {len(saved_articles)} new articles.")
        return len(saved_articles)
    
    def get_articles_by_category(self, db: Session, category: str, limit: int = 20) -> List[Article]:
        """Get articles from database by category (case-insensitive)"""
        # Convert category to lowercase for case-insensitive matching
        category_lower = category.lower() if category else ""
        return db.query(Article).filter(
            Article.category.ilike(category_lower)
        ).order_by(Article.published_at.desc()).limit(limit).all()
    
    def get_latest_articles(self, db: Session, limit: int = 50) -> List[Article]:
        """Get latest articles from database"""
        return db.query(Article).order_by(
            Article.published_at.desc()
        ).limit(limit).all()
    
    def search_articles(self, db: Session, query: str, limit: int = 20) -> List[Article]:
        """Search articles in database (case-insensitive)"""
        # Convert query to lowercase for case-insensitive search
        query_lower = query.lower() if query else ""
        return db.query(Article).filter(
            Article.title.ilike(f'%{query_lower}%') | 
            Article.description.ilike(f'%{query_lower}%') |
            Article.content.ilike(f'%{query_lower}%')
        ).order_by(Article.published_at.desc()).limit(limit).all()
    
    def get_article_by_id(self, db: Session, article_id: int) -> Optional[Article]:
        """Get article by ID"""
        return db.query(Article).filter(Article.id == article_id).first()
    
    def get_articles_by_source(self, db: Session, source_name: str, limit: int = 20) -> List[Article]:
        """Get articles by source (case-insensitive)"""
        # Convert source name to lowercase for case-insensitive matching
        source_lower = source_name.lower() if source_name else ""
        return db.query(Article).filter(
            Article.source_name.ilike(source_lower)
        ).order_by(Article.published_at.desc()).limit(limit).all() 