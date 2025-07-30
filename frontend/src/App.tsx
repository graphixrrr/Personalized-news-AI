import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navigation from './components/Navigation';
import HomePage from './pages/HomePage';
import NewsPage from './pages/NewsPage';
import CategoriesPage from './pages/CategoriesPage';
import ReadingListPage from './pages/ReadingListPage';
import AnalyticsPage from './pages/AnalyticsPage';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/news" element={<NewsPage />} />
          <Route path="/news/:category" element={<NewsPage />} />
          <Route path="/categories" element={<CategoriesPage />} />
          <Route path="/reading-list" element={<ReadingListPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
        </Routes>
      </main>
    </div>
  );
}

export default App; 