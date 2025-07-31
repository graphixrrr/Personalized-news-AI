import axios from 'axios';
import { 
  NewsResponse, 
  Article, 
  Category, 
  UserPreference, 
  ReadingAnalytics, 
  AIInsight,
  Recommendation,
  LoginCredentials,
  RegisterData,
  AuthResponse,
  User
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  maxRedirects: 5, // Allow redirects
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await api.post('/api/users/login', credentials);
    return response.data;
  },

  register: async (data: RegisterData): Promise<User> => {
    const response = await api.post('/api/users/register', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/api/users/me');
    return response.data;
  },
};

// News API
export const newsAPI = {
  getNews: async (params?: {
    category?: string;
    search?: string;
    limit?: number;
    user_id?: number;
  }): Promise<NewsResponse> => {
    const response = await api.get('/api/news', { params });
    return response.data;
  },

  getCategories: async (): Promise<{ categories: Category[] }> => {
    const response = await api.get('/api/news/categories');
    return response.data;
  },

  getTrending: async (): Promise<{ articles: Article[] }> => {
    const response = await api.get('/api/news/trending');
    return response.data;
  },

  getArticle: async (id: number): Promise<Article> => {
    const response = await api.get(`/api/news/${id}`);
    return response.data;
  },

  markAsRead: async (articleId: number, userId: number, data?: {
    read_duration?: number;
    completed?: boolean;
  }): Promise<{ message: string; article_id: number }> => {
    const response = await api.post(`/api/news/${articleId}/read`, {
      user_id: userId,
      ...data,
    });
    return response.data;
  },

  refreshNews: async (): Promise<{ message: string; articles_added: number }> => {
    const response = await api.post('/api/news/refresh');
    return response.data;
  },
};

// Preferences API
export const preferencesAPI = {
  getUserPreferences: async (userId: number): Promise<UserPreference[]> => {
    const response = await api.get(`/api/preferences/${userId}`);
    return response.data;
  },

  createPreference: async (userId: number, preference: {
    category: string;
    weight: number;
  }): Promise<{ message: string }> => {
    const response = await api.post(`/api/preferences/${userId}`, preference);
    return response.data;
  },

  deletePreference: async (userId: number, category: string): Promise<{ message: string }> => {
    const response = await api.delete(`/api/preferences/${userId}/${category}`);
    return response.data;
  },
};

// Analytics API
export const analyticsAPI = {
  getReadingAnalytics: async (userId: number): Promise<ReadingAnalytics> => {
    const response = await api.get(`/api/analytics/${userId}/reading`);
    return response.data;
  },

  getPreferenceAnalytics: async (userId: number): Promise<{
    preferences: Array<{
      category: string;
      weight: number;
      created_at: string;
    }>;
    total_preferences: number;
  }> => {
    const response = await api.get(`/api/analytics/${userId}/preferences`);
    return response.data;
  },

  getFeedbackAnalytics: async (userId: number): Promise<{
    total_feedback: number;
    average_rating: number;
    liked_articles: number;
    disliked_articles: number;
    rating_distribution: Record<string, number>;
  }> => {
    const response = await api.get(`/api/analytics/${userId}/feedback`);
    return response.data;
  },

  getUserInsights: async (userId: number): Promise<{
    insights: AIInsight[];
    total_insights: number;
    reading_analytics: ReadingAnalytics;
  }> => {
    const response = await api.get(`/api/analytics/${userId}/insights`);
    return response.data;
  },
};

// AI API
export const aiAPI = {
  getRecommendations: async (data: {
    user_id: number;
    limit?: number;
    algorithm?: string;
  }): Promise<{
    recommendations: Recommendation[];
    algorithm: string;
    total: number;
  }> => {
    const response = await api.post('/api/ai/recommendations', data);
    return response.data;
  },

  analyzeArticle: async (data: {
    title: string;
    description: string;
    content?: string;
  }): Promise<{
    sentiment_score: number;
    keywords: string[];
    reading_time: number;
    category: string;
    sentiment_label: string;
  }> => {
    const response = await api.post('/api/ai/analyze-article', data);
    return response.data;
  },

  getUserProfile: async (userId: number): Promise<{
    user_id: number;
    preferences: Record<string, number>;
    categories_read: Record<string, number>;
    sources_read: Record<string, number>;
    sentiment_preference: number;
    avg_reading_time: number;
    liked_keywords: string[];
    total_articles_read: number;
    profile_strength: number;
  }> => {
    const response = await api.get(`/api/ai/user-profile/${userId}`);
    return response.data;
  },

  getAlgorithms: async (): Promise<{
    algorithms: Array<{
      id: string;
      name: string;
      description: string;
      strengths: string[];
      weaknesses: string[];
    }>;
  }> => {
    const response = await api.get('/api/ai/algorithms');
    return response.data;
  },

  getAIInsights: async (userId: number): Promise<{
    insights: AIInsight[];
    total_insights: number;
    profile_strength: number;
  }> => {
    const response = await api.get(`/api/ai/insights/${userId}`);
    return response.data;
  },
};

export default api; 