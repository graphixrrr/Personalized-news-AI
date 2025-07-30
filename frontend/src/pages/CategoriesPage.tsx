import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FaLaptopCode, 
  FaBriefcase, 
  FaFlask, 
  FaHeartbeat, 
  FaFilm, 
  FaFutbol,
  FaArrowRight,
  FaNewspaper,
  FaChartBar
} from 'react-icons/fa';

const CategoriesPage: React.FC = () => {
  const categories = [
    {
      id: 'technology',
      name: 'Technology',
      icon: FaLaptopCode,
      description: 'Latest tech news, AI developments, and digital innovations',
      color: 'from-blue-500 to-cyan-500',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200',
      articleCount: '2.5K+ articles'
    },
    {
      id: 'business',
      name: 'Business',
      icon: FaBriefcase,
      description: 'Market updates, company news, and economic insights',
      color: 'from-green-500 to-emerald-500',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200',
      articleCount: '1.8K+ articles'
    },
    {
      id: 'science',
      name: 'Science',
      icon: FaFlask,
      description: 'Scientific discoveries, research breakthroughs, and innovations',
      color: 'from-purple-500 to-violet-500',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200',
      articleCount: '1.2K+ articles'
    },
    {
      id: 'health',
      name: 'Health',
      icon: FaHeartbeat,
      description: 'Medical news, wellness tips, and healthcare updates',
      color: 'from-red-500 to-pink-500',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200',
      articleCount: '1.5K+ articles'
    },
    {
      id: 'entertainment',
      name: 'Entertainment',
      icon: FaFilm,
      description: 'Movies, music, celebrity news, and pop culture',
      color: 'from-yellow-500 to-orange-500',
      bgColor: 'bg-yellow-50',
      borderColor: 'border-yellow-200',
      articleCount: '2.1K+ articles'
    },
    {
      id: 'sports',
      name: 'Sports',
      icon: FaFutbol,
      description: 'Sports news, game results, and athlete updates',
      color: 'from-indigo-500 to-blue-500',
      bgColor: 'bg-indigo-50',
      borderColor: 'border-indigo-200',
      articleCount: '1.9K+ articles'
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container-professional py-8">
        {/* Header */}
        <div className="section-header text-center">
          <h1 className="section-title">News Categories</h1>
          <p className="section-subtitle">
            Explore news by topic and discover content that matches your interests
          </p>
        </div>

        {/* Categories Grid */}
        <div className="grid-professional mb-12">
          {categories.map((category) => (
            <Link
              key={category.id}
              to={`/news/${category.id}`}
              className="category-card group"
            >
              <div className={`${category.bgColor} ${category.borderColor} border-2 rounded-xl p-8 hover:shadow-xl transition-all duration-300 group-hover:scale-105`}>
                <div className="text-center">
                  {/* Icon */}
                  <div className={`w-16 h-16 bg-gradient-to-r ${category.color} rounded-full flex items-center justify-center mx-auto mb-4 text-2xl text-white shadow-lg`}>
                    <category.icon className="text-2xl" />
                  </div>
                  
                  {/* Title */}
                  <h3 className="font-serif text-xl font-bold mb-3 text-gray-900">
                    {category.name}
                  </h3>
                  
                  {/* Description */}
                  <p className="text-gray-600 mb-4 leading-relaxed">
                    {category.description}
                  </p>
                  
                  {/* Article Count */}
                  <div className="text-sm text-gray-500 mb-6">
                    {category.articleCount}
                  </div>
                  
                  {/* CTA Button */}
                  <div className={`inline-flex items-center px-4 py-2 bg-gradient-to-r ${category.color} text-white rounded-lg font-medium group-hover:shadow-lg transition-all duration-200`}>
                    <span>Explore {category.name}</span>
                    <FaArrowRight className="ml-2 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>

        {/* Call to Action */}
        <div className="text-center">
          <div className="card-professional p-8 max-w-2xl mx-auto">
            <h2 className="font-serif text-2xl font-bold mb-4 text-gray-900">
              Can't find what you're looking for?
            </h2>
            <p className="text-gray-600 mb-6">
              Browse all news articles or check out your personalized analytics to discover more content.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/news"
                className="btn-primary inline-flex items-center"
              >
                <FaNewspaper className="mr-2" />
                <span>Browse All News</span>
              </Link>
              <Link
                to="/analytics"
                className="btn-secondary inline-flex items-center"
              >
                <FaChartBar className="mr-2" />
                <span>View Analytics</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CategoriesPage; 