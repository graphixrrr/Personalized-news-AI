export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
}

export interface Article {
  id: number;
  title: string;
  description: string;
  content?: string;
  url: string;
  image_url?: string;
  source_name: string;
  author?: string;
  published_at?: string;
  category: string;
  tags?: string[];
  sentiment_score?: number;
  reading_time?: number;
}

export interface NewsResponse {
  articles: Article[];
  total: number;
  category?: string;
  search?: string;
  personalized: boolean;
}

export interface Category {
  id: string;
  name: string;
  icon: string;
}

export interface UserPreference {
  id: number;
  user_id: number;
  category: string;
  weight: number;
}

export interface ReadingAnalytics {
  total_articles_read: number;
  total_reading_time: number;
  average_reading_time: number;
  favorite_categories: Array<{ category: string; count: number }>;
  favorite_sources: Array<{ source: string; count: number }>;
  reading_trends: Array<{
    date: string;
    articles_read: number;
    reading_time: number;
  }>;
  completion_rate: number;
}

export interface AIInsight {
  type: string;
  title: string;
  description: string;
  category: string;
  confidence?: number;
}

export interface Recommendation {
  article: Article;
  score: number;
  type: string;
  confidence: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
} 