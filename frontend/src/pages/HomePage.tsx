import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { readingTracker } from '../services/readingTracker';
import ReadingTracker from '../components/ReadingTracker';
import { FaChartBar, FaNewspaper, FaBookOpen, FaClock, FaFire } from 'react-icons/fa';

const HomePage: React.FC = () => {
  const [showTracker, setShowTracker] = useState(false);
  const [stats, setStats] = useState({
    totalArticles: 0,
    totalReadingTime: 0,
    currentStreak: 0,
    totalSessions: 0
  });

  useEffect(() => {
    const readingStats = readingTracker.getReadingStats();
    setStats({
      totalArticles: readingStats.totalArticlesRead,
      totalReadingTime: readingStats.totalReadingTime,
      currentStreak: readingStats.currentStreak,
      totalSessions: readingStats.totalArticlesRead
    });
  }, []);

  return (
    <div className="main-content">
      <div className="container-professional py-8">
        {/* Hero Section */}
        <div className="section-header text-center">
          <h1 className="section-title">Welcome to NewsAI</h1>
          <p className="section-subtitle">
            Your modern news reading platform with intelligent curation and beautiful design
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid-professional mb-12">
          <div className="stats-card">
            <div className="flex items-center justify-between">
              <div>
                <div className="stats-number">{stats.totalArticles}</div>
                <div className="stats-label">Articles Read</div>
              </div>
              <div className="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                <FaBookOpen className="w-8 h-8 text-white" />
              </div>
            </div>
          </div>

          <div className="stats-card">
            <div className="flex items-center justify-between">
              <div>
                <div className="stats-number">{Math.round(stats.totalReadingTime)}</div>
                <div className="stats-label">Minutes Read</div>
              </div>
              <div className="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                <FaClock className="w-8 h-8 text-white" />
              </div>
            </div>
          </div>

          <div className="stats-card">
            <div className="flex items-center justify-between">
              <div>
                <div className="stats-number">{stats.currentStreak}</div>
                <div className="stats-label">Day Streak</div>
              </div>
              <div className="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                <FaFire className="w-8 h-8 text-white" />
              </div>
            </div>
          </div>

          <div className="stats-card">
            <div className="flex items-center justify-between">
              <div>
                <div className="stats-number">{stats.totalSessions}</div>
                <div className="stats-label">Reading Sessions</div>
              </div>
              <div className="w-16 h-16 bg-white bg-opacity-20 rounded-2xl flex items-center justify-center backdrop-blur-sm">
                <FaChartBar className="w-8 h-8 text-white" />
              </div>
            </div>
          </div>
        </div>

        {/* Reading Tracker Toggle */}
        <div className="text-center mb-8">
          <button
            onClick={() => setShowTracker(!showTracker)}
            className="btn-secondary flex items-center mx-auto"
          >
            <FaChartBar className="text-sm mr-2" />
            <span>{showTracker ? 'Hide' : 'Show'} Detailed Analytics</span>
          </button>
        </div>

        {/* Reading Tracker */}
        {showTracker && (
          <div className="mb-12">
            <ReadingTracker />
          </div>
        )}

        {/* Quick Actions */}
        <div className="section-header">
          <h2 className="section-title">Quick Actions</h2>
          <p className="section-subtitle">Start exploring the latest news and insights</p>
        </div>

        <div className="grid-professional mb-12">
          <Link
            to="/news"
            className="category-card group"
          >
            <div className="category-icon">
              <FaNewspaper className="text-2xl" />
            </div>
            <h3 className="font-serif text-xl font-bold mb-2 text-gray-900">Latest News</h3>
            <p className="text-gray-600 mb-4">
              Discover the most recent headlines and breaking stories from around the world
            </p>
            <div className="inline-flex items-center text-blue-600 font-medium group-hover:translate-x-1 transition-transform">
              <span>Browse News</span>
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </Link>

          <Link
            to="/categories"
            className="category-card group"
          >
            <div className="category-icon">
              <FaChartBar className="text-2xl" />
            </div>
            <h3 className="font-serif text-xl font-bold mb-2 text-gray-900">Categories</h3>
            <p className="text-gray-600 mb-4">
              Explore news by topic - technology, business, science, health, and more
            </p>
            <div className="inline-flex items-center text-blue-600 font-medium group-hover:translate-x-1 transition-transform">
              <span>View Categories</span>
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </Link>

          <Link
            to="/reading-list"
            className="category-card group"
          >
            <div className="category-icon">
              <FaBookOpen className="text-2xl" />
            </div>
            <h3 className="font-serif text-xl font-bold mb-2 text-gray-900">Reading List</h3>
            <p className="text-gray-600 mb-4">
              Access your saved articles and reading history in one organized place
            </p>
            <div className="inline-flex items-center text-blue-600 font-medium group-hover:translate-x-1 transition-transform">
              <span>View List</span>
              <svg className="ml-2 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </Link>
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <div className="card-professional p-8 max-w-2xl mx-auto">
            <h2 className="font-serif text-2xl font-bold mb-4 text-gray-900">
              Ready to start reading?
            </h2>
            <p className="text-gray-600 mb-6">
              Dive into the latest news with our professional reading experience. 
              Track your progress, discover new topics, and stay informed.
            </p>
            <Link
              to="/news"
              className="btn-primary inline-flex items-center"
            >
              <FaNewspaper className="mr-2" />
              <span>Start Reading</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 