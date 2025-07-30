import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  FaHome, 
  FaNewspaper, 
  FaFolder, 
  FaBookOpen, 
  FaChartBar,
  FaBars
} from 'react-icons/fa';

const Navigation: React.FC = () => {
  const location = useLocation();
  
  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <nav className="nav-professional sticky top-0 z-40">
      <div className="container-professional">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3">
              <div className="w-12 h-12 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl flex items-center justify-center shadow-lg glow">
                <FaNewspaper className="text-white text-xl" />
              </div>
              <div>
                <span className="font-display text-2xl font-bold gradient-text">NewsAI</span>
                <div className="text-xs text-gray-500 -mt-1">Modern News Platform</div>
              </div>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            <Link
              to="/"
              className={`nav-link rounded-lg ${
                isActive('/') 
                  ? 'nav-link active' 
                  : 'hover:bg-gray-50'
              }`}
            >
              <FaHome className="text-sm mr-2" />
              <span>Home</span>
            </Link>
            
            <Link
              to="/news"
              className={`nav-link rounded-lg ${
                isActive('/news') 
                  ? 'nav-link active' 
                  : 'hover:bg-gray-50'
              }`}
            >
              <FaNewspaper className="text-sm mr-2" />
              <span>Latest News</span>
            </Link>
            
            <Link
              to="/categories"
              className={`nav-link rounded-lg ${
                isActive('/categories') 
                  ? 'nav-link active' 
                  : 'hover:bg-gray-50'
              }`}
            >
              <FaFolder className="text-sm mr-2" />
              <span>Categories</span>
            </Link>
            
            <Link
              to="/reading-list"
              className={`nav-link rounded-lg ${
                isActive('/reading-list') 
                  ? 'nav-link active' 
                  : 'hover:bg-gray-50'
              }`}
            >
              <FaBookOpen className="text-sm mr-2" />
              <span>Reading List</span>
            </Link>
            
            <Link
              to="/analytics"
              className={`nav-link rounded-lg ${
                isActive('/analytics') 
                  ? 'nav-link active' 
                  : 'hover:bg-gray-50'
              }`}
            >
              <FaChartBar className="text-sm mr-2" />
              <span>Analytics</span>
            </Link>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button className="nav-link rounded-lg hover:bg-gray-50">
              <FaBars className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 border-t border-gray-200 mt-4">
            <Link
              to="/"
              className={`block nav-link rounded-lg ${
                isActive('/') ? 'nav-link active' : 'hover:bg-gray-50'
              }`}
            >
              <FaHome className="text-sm mr-2" />
              <span>Home</span>
            </Link>
            <Link
              to="/news"
              className={`block nav-link rounded-lg ${
                isActive('/news') ? 'nav-link active' : 'hover:bg-gray-50'
              }`}
            >
              <FaNewspaper className="text-sm mr-2" />
              <span>Latest News</span>
            </Link>
            <Link
              to="/categories"
              className={`block nav-link rounded-lg ${
                isActive('/categories') ? 'nav-link active' : 'hover:bg-gray-50'
              }`}
            >
              <FaFolder className="text-sm mr-2" />
              <span>Categories</span>
            </Link>
            <Link
              to="/reading-list"
              className={`block nav-link rounded-lg ${
                isActive('/reading-list') ? 'nav-link active' : 'hover:bg-gray-50'
              }`}
            >
              <FaBookOpen className="text-sm mr-2" />
              <span>Reading List</span>
            </Link>
            <Link
              to="/analytics"
              className={`block nav-link rounded-lg ${
                isActive('/analytics') ? 'nav-link active' : 'hover:bg-gray-50'
              }`}
            >
              <FaChartBar className="text-sm mr-2" />
              <span>Analytics</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation; 