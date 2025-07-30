import React, { useState, useEffect } from 'react';

const AnalyticsPage: React.FC = () => {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading analytics
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto">
        <div className="text-center py-12">
          <div className="spinner mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Reading Analytics</h1>
        <p className="text-gray-600">
          Track your reading patterns and discover insights about your news consumption.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid md:grid-cols-4 gap-6 mb-8">
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="text-2xl mr-4">📚</div>
            <div>
              <p className="text-sm text-gray-600">Articles Read</p>
              <p className="text-2xl font-bold text-purple-600">0</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="text-2xl mr-4">⏱️</div>
            <div>
              <p className="text-sm text-gray-600">Total Reading Time</p>
              <p className="text-2xl font-bold text-pink-600">0 min</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="text-2xl mr-4">📊</div>
            <div>
              <p className="text-sm text-gray-600">Completion Rate</p>
              <p className="text-2xl font-bold text-purple-500">0%</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="flex items-center">
            <div className="text-2xl mr-4">🎯</div>
            <div>
              <p className="text-sm text-gray-600">Categories</p>
              <p className="text-2xl font-bold text-pink-500">0</p>
            </div>
          </div>
        </div>
      </div>

      {/* Reading Trends */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
        <h2 className="text-xl font-semibold mb-4">Reading Trends (Last 7 Days)</h2>
        <div className="h-64 flex items-end justify-center space-x-2">
          {[0, 0, 0, 0, 0, 0, 0].map((value, index) => (
            <div key={index} className="flex flex-col items-center">
              <div className="w-8 bg-gradient-to-t from-purple-200 to-pink-200 rounded-t"></div>
              <span className="text-xs text-gray-500 mt-2">
                {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][index]}
              </span>
            </div>
          ))}
        </div>
        <p className="text-center text-gray-500 mt-4">No reading data available yet</p>
      </div>

      {/* Favorite Categories */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-8">
        <h2 className="text-xl font-semibold mb-4">Favorite Categories</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <div className="flex items-center">
              <span className="mr-3">💻</span>
              <span>Technology</span>
            </div>
            <span className="text-sm text-gray-500">0 articles</span>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <div className="flex items-center">
              <span className="mr-3">💼</span>
              <span>Business</span>
            </div>
            <span className="text-sm text-gray-500">0 articles</span>
          </div>
        </div>
        <p className="text-center text-gray-500 mt-4">Start reading to see your preferences</p>
      </div>

      {/* AI Insights */}
      <div className="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-4">🤖 AI Insights</h2>
        <div className="space-y-4">
          <div className="bg-white bg-opacity-10 p-4 rounded">
            <h3 className="font-semibold mb-2">Getting Started</h3>
            <p className="text-purple-100">
              Start reading articles to help our AI understand your preferences and provide personalized recommendations.
            </p>
          </div>
          <div className="bg-white bg-opacity-10 p-4 rounded">
            <h3 className="font-semibold mb-2">Personalization</h3>
            <p className="text-purple-100">
              The more you read, the better our recommendations become. We analyze your reading patterns to suggest relevant content.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage; 