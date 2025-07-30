import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Article } from '../types';
import { newsAPI } from '../services/api';
import { readingTracker } from '../services/readingTracker';
import ReadingTracker from '../components/ReadingTracker';
import ArticleReader from '../components/ArticleReader';
import { FaBookmark, FaArrowRight, FaSpinner, FaChartBar, FaFilter, FaSort, FaNewspaper } from 'react-icons/fa';

const NewsPage: React.FC = () => {
  const { category } = useParams<{ category?: string }>();
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedArticle, setSelectedArticle] = useState<Article | null>(null);
  const [showTracker, setShowTracker] = useState(false);
  const [savedArticles, setSavedArticles] = useState<Article[]>([]);

  useEffect(() => {
    fetchArticles();
    loadSavedArticles();
  }, [category]);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await newsAPI.getNews({ category });
      setArticles(response.articles || []);
    } catch (err) {
      setError('Failed to load articles. Please try again.');
      console.error('Error fetching articles:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadSavedArticles = () => {
    const saved = JSON.parse(localStorage.getItem('saved_articles') || '[]');
    setSavedArticles(saved);
  };

  const saveArticle = (article: Article) => {
    const saved = JSON.parse(localStorage.getItem('saved_articles') || '[]');
    const isAlreadySaved = saved.some((a: Article) => a.id === article.id);
    
    if (!isAlreadySaved) {
      const updated = [...saved, article];
      localStorage.setItem('saved_articles', JSON.stringify(updated));
      setSavedArticles(updated);
    }
  };

  const handleArticleClick = (article: Article) => {
    setSelectedArticle(article);
    const sessionId = readingTracker.startReadingSession(article.id);
    // Store session ID for tracking
    localStorage.setItem('current_session', sessionId);
  };

  const handleCloseReader = () => {
    const sessionId = localStorage.getItem('current_session');
    if (sessionId) {
      readingTracker.endReadingSession(sessionId, true);
      localStorage.removeItem('current_session');
    }
    setSelectedArticle(null);
  };

  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return 'Unknown date';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container-professional py-8">
          <div className="text-center py-12">
            <FaSpinner className="animate-spin mx-auto text-blue-600 text-4xl mb-4" />
            <p className="text-gray-600">Loading articles...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="container-professional py-8">
          <div className="text-center py-12">
            <div className="text-4xl mb-4">⚠️</div>
            <h2 className="text-xl font-bold text-gray-900 mb-2">Error Loading Articles</h2>
            <p className="text-gray-600 mb-4">{error}</p>
            <button
              onClick={fetchArticles}
              className="btn-primary"
            >
              Try Again
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container-professional py-8">
        {/* Header */}
        <div className="section-header">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="section-title">
                {category ? `${category.charAt(0).toUpperCase() + category.slice(1)} News` : 'Latest News'}
              </h1>
              <p className="section-subtitle">
                {category 
                  ? `Stay updated with the latest ${category} news and insights`
                  : 'Discover the most recent headlines and breaking stories'
                }
              </p>
            </div>
            <button
              onClick={() => setShowTracker(!showTracker)}
              className="btn-secondary flex items-center"
            >
              <FaChartBar className="text-sm mr-2" />
              <span>{showTracker ? 'Hide' : 'Show'} Tracker</span>
            </button>
          </div>
        </div>

        {/* Reading Tracker */}
        {showTracker && (
          <div className="mb-8">
            <ReadingTracker />
          </div>
        )}

        {/* Articles Grid */}
        {articles.length > 0 ? (
          <div className="grid-professional">
            {articles.map((article) => {
              const isSaved = savedArticles.some(a => a.id === article.id);
              
              return (
                <article key={article.id} className="article-card group cursor-pointer" onClick={() => handleArticleClick(article)}>
                  <div className="article-image">
                    {article.image_url ? (
                      <img 
                        src={article.image_url} 
                        alt={article.title}
                        className="w-full h-full object-cover"
                        onError={(e) => {
                          const target = e.target as HTMLImageElement;
                          target.style.display = 'none';
                        }}
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
                        <FaNewspaper className="text-blue-400 text-4xl" />
                      </div>
                    )}
                  </div>
                  
                  <div className="article-content">
                    <h2 className="article-title">{article.title}</h2>
                    <p className="article-description">{article.description}</p>
                    
                    <div className="article-meta">
                      <div className="flex items-center space-x-4">
                        <span className="article-source">{article.source_name}</span>
                        <span>{formatDate(article.published_at)}</span>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            saveArticle(article);
                          }}
                          className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center"
                        >
                          <FaBookmark className="mr-1" />
                          <span>{isSaved ? 'Saved' : 'Save'}</span>
                        </button>
                        <span className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center group-hover:translate-x-1 transition-transform">
                          <span>Read more</span>
                          <FaArrowRight className="ml-1" />
                        </span>
                      </div>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state-icon">
              <FaNewspaper className="w-full h-full" />
            </div>
            <h3 className="empty-state-title">No articles found</h3>
            <p className="empty-state-description">
              {category 
                ? `No ${category} articles are currently available.`
                : 'No articles are currently available.'
              }
            </p>
          </div>
        )}
      </div>

      {/* Article Reader Modal */}
      {selectedArticle && (
        <ArticleReader
          article={selectedArticle}
          onClose={handleCloseReader}
        />
      )}
    </div>
  );
};

export default NewsPage; 