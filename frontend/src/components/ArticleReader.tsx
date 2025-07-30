import React, { useEffect, useState } from 'react';
import { Article } from '../types';
import { readingTracker } from '../services/readingTracker';
import { FaTimes, FaBookmark, FaExternalLinkAlt, FaClock, FaUser } from 'react-icons/fa';

interface ArticleReaderProps {
  article: Article;
  onClose: () => void;
}

const ArticleReader: React.FC<ArticleReaderProps> = ({ article, onClose }) => {
  const [isReading, setIsReading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');

  useEffect(() => {
    setIsReading(true);
    const session = readingTracker.startReadingSession(article.id);
    setSessionId(session);
  }, [article.id]);

  const formatDate = (dateString: string | undefined) => {
    if (!dateString) return 'Unknown date';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleClose = () => {
    if (sessionId) {
      readingTracker.endReadingSession(sessionId, true);
    }
    onClose();
  };

  return (
    <div className="modal-professional" onClick={handleClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="modal-header">
          <div className="flex items-center space-x-4">
            <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <FaBookmark className="text-blue-600" />
            </div>
            <div>
              <h2 className="font-serif text-xl font-bold text-gray-900">Article Reader</h2>
              <p className="text-sm text-gray-600">Reading from {article.source_name}</p>
            </div>
          </div>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <FaTimes className="w-6 h-6" />
          </button>
        </div>

        {/* Article Content */}
        <div className="modal-body">
          {/* Article Header */}
          <div className="mb-8">
            <h1 className="font-serif text-3xl font-bold mb-4 text-gray-900 leading-tight">
              {article.title}
            </h1>
            
            <div className="flex items-center space-x-6 text-sm text-gray-600 mb-6">
              <div className="flex items-center space-x-2">
                <FaUser className="text-gray-400" />
                <span>{article.author || 'Unknown Author'}</span>
              </div>
              <div className="flex items-center space-x-2">
                <FaClock className="text-gray-400" />
                <span>{formatDate(article.published_at)}</span>
              </div>
              <div className="flex items-center space-x-2">
                <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                <span className="font-medium text-blue-600">{article.source_name}</span>
              </div>
            </div>

            {article.image_url && (
              <div className="mb-6">
                <img 
                  src={article.image_url} 
                  alt={article.title}
                  className="w-full h-64 object-cover rounded-lg shadow-md"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                  }}
                />
              </div>
            )}
          </div>

          {/* Article Content */}
          <div className="article-reader">
            {article.content && article.content.length > 200 ? (
              <div className="space-y-6">
                {/* Split content into paragraphs for better readability */}
                {article.content.split('\n\n').map((paragraph, index) => (
                  <p key={index} className="text-lg leading-7 text-gray-700">
                    {paragraph.trim()}
                  </p>
                ))}
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FaBookmark className="text-blue-600 text-2xl" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Full Content Not Available</h3>
                <p className="text-gray-600 mb-6">
                  This article's full content is not available in our reader. 
                  You can read the complete article on the original website.
                </p>
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary inline-flex items-center"
                >
                  <FaExternalLinkAlt className="mr-2" />
                  <span>Read on {article.source_name}</span>
                </a>
              </div>
            )}
          </div>

          {/* Article Footer */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-600">
                <p>Reading time: ~{article.reading_time || 3} minutes</p>
                <p>Category: {article.category || 'General'}</p>
              </div>
              
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => {
                    const saved = JSON.parse(localStorage.getItem('saved_articles') || '[]');
                    const isAlreadySaved = saved.some((a: Article) => a.id === article.id);
                    
                    if (!isAlreadySaved) {
                      const updated = [...saved, article];
                      localStorage.setItem('saved_articles', JSON.stringify(updated));
                    }
                  }}
                  className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center"
                >
                  <FaBookmark className="mr-1" />
                  <span>Save for Later</span>
                </button>
                <a
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-700 font-medium text-sm flex items-center"
                >
                  <FaExternalLinkAlt className="mr-1" />
                  <span>View Original</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleReader; 