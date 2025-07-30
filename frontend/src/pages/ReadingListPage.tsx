import React, { useState, useEffect } from 'react';
import { Article } from '../types';
import { readingTracker } from '../services/readingTracker';
import { FaBookmark, FaCheck, FaArrowRight, FaTimes, FaNewspaper, FaHistory, FaTrash } from 'react-icons/fa';

const ReadingListPage: React.FC = () => {
  const [savedArticles, setSavedArticles] = useState<Article[]>([]);
  const [readingHistory, setReadingHistory] = useState<Article[]>([]);
  const [activeTab, setActiveTab] = useState<'saved' | 'history'>('saved');

  useEffect(() => {
    loadSavedArticles();
    loadReadingHistory();
  }, []);

  const loadSavedArticles = () => {
    const saved = JSON.parse(localStorage.getItem('saved_articles') || '[]');
    setSavedArticles(saved);
  };

  const loadReadingHistory = () => {
    const history = JSON.parse(localStorage.getItem('reading_history') || '[]');
    setReadingHistory(history);
  };

  const removeFromSaved = (articleId: number) => {
    const updated = savedArticles.filter(article => article.id !== articleId);
    setSavedArticles(updated);
    localStorage.setItem('saved_articles', JSON.stringify(updated));
  };

  const clearHistory = () => {
    setReadingHistory([]);
    localStorage.setItem('reading_history', JSON.stringify([]));
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

  const ArticleCard: React.FC<{ 
    article: Article; 
    showReadButton?: boolean; 
    showRemoveButton?: boolean;
    onRemove?: () => void;
  }> = ({ article, showReadButton = false, showRemoveButton = false, onRemove }) => (
    <div className="article-card group">
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
            {showReadButton && (
              <button
                onClick={() => {
                  // Mark as read logic here
                }}
                className="text-green-600 hover:text-green-700 font-medium text-sm flex items-center"
              >
                <FaCheck className="mr-1" />
                <span>Mark Read</span>
              </button>
            )}
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center"
            >
              <span>Read</span>
              <FaArrowRight className="ml-1" />
            </a>
          </div>
        </div>
      </div>
      
      {showRemoveButton && onRemove && (
        <button
          onClick={onRemove}
          className="absolute top-2 right-2 w-8 h-8 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors shadow-lg"
          title="Remove from saved"
        >
          <FaTimes className="text-sm" />
        </button>
      )}
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container-professional py-8">
        {/* Header */}
        <div className="section-header">
          <h1 className="section-title">Reading List</h1>
          <p className="section-subtitle">
            Manage your saved articles and track your reading history
          </p>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 bg-white p-1 rounded-lg shadow-sm mb-8 max-w-md">
          <button
            onClick={() => setActiveTab('saved')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'saved'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <FaBookmark className="inline mr-2" />
            Saved Articles ({savedArticles.length})
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
              activeTab === 'history'
                ? 'bg-blue-100 text-blue-700'
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <FaHistory className="inline mr-2" />
            Reading History ({readingHistory.length})
          </button>
        </div>

        {/* Content */}
        {activeTab === 'saved' ? (
          <div>
            {savedArticles.length > 0 ? (
              <div className="grid-professional">
                {savedArticles.map((article) => (
                  <div key={article.id} className="relative">
                    <ArticleCard
                      article={article}
                      showRemoveButton={true}
                      onRemove={() => removeFromSaved(article.id)}
                    />
                  </div>
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-state-icon">
                  <FaBookmark className="w-full h-full" />
                </div>
                <h3 className="empty-state-title">No saved articles yet</h3>
                <p className="empty-state-description">
                  Start reading articles and save them to your list for later.
                </p>
                <div className="mt-6">
                  <a
                    href="/news"
                    className="btn-primary inline-flex items-center"
                  >
                    <FaNewspaper className="mr-2" />
                    <span>Browse News</span>
                  </a>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div>
            {readingHistory.length > 0 ? (
              <div>
                <div className="flex justify-between items-center mb-6">
                  <h2 className="font-serif text-xl font-bold text-gray-900">Recent Reading</h2>
                  <button
                    onClick={clearHistory}
                    className="btn-secondary flex items-center text-red-600 hover:text-red-700"
                  >
                    <FaTrash className="mr-2" />
                    <span>Clear History</span>
                  </button>
                </div>
                <div className="grid-professional">
                  {readingHistory.map((article) => (
                    <ArticleCard
                      key={article.id}
                      article={article}
                      showReadButton={true}
                    />
                  ))}
                </div>
              </div>
            ) : (
              <div className="empty-state">
                <div className="empty-state-icon">
                  <FaHistory className="w-full h-full" />
                </div>
                <h3 className="empty-state-title">No reading history</h3>
                <p className="empty-state-description">
                  Your reading history will appear here once you start reading articles.
                </p>
                <div className="mt-6">
                  <a
                    href="/news"
                    className="btn-primary inline-flex items-center"
                  >
                    <FaNewspaper className="mr-2" />
                    <span>Start Reading</span>
                  </a>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ReadingListPage; 