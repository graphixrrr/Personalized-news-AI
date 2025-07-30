import React, { useState, useEffect } from 'react';
import { readingTracker, ReadingStats, StreakData } from '../services/readingTracker';

const ReadingTracker: React.FC = () => {
  const [stats, setStats] = useState<ReadingStats>(readingTracker.getReadingStats());
  const [streakData, setStreakData] = useState<StreakData>(readingTracker.getStreakData());
  const [isDemo, setIsDemo] = useState(false);

  useEffect(() => {
    // Check if we have any real data
    const realStats = readingTracker.getReadingStats();
    if (realStats.totalArticlesRead === 0) {
      setIsDemo(true);
      // Show demo data
      setStats({
        totalArticlesRead: 15,
        totalReadingTime: 127,
        currentStreak: 7,
        longestStreak: 12,
        averageReadingTime: 8,
        todayReadCount: 3,
        weeklyReadCount: 8,
        monthlyReadCount: 15
      });
      
      // Create demo streak data
      const demoStreakHistory = [];
      for (let i = 29; i >= 0; i--) {
        const date = new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
        const readCount = i >= 23 ? Math.floor(Math.random() * 3) + 1 : 0; // Last 7 days have reading
        demoStreakHistory.push({ date, readCount });
      }
      
      setStreakData({
        currentStreak: 7,
        longestStreak: 12,
        lastReadDate: new Date(),
        streakHistory: demoStreakHistory
      });
    } else {
      // Update stats every minute
      const interval = setInterval(() => {
        setStats(readingTracker.getReadingStats());
        setStreakData(readingTracker.getStreakData());
      }, 60000);

      return () => clearInterval(interval);
    }
  }, []);

  const getStreakEmoji = (streak: number) => {
    if (streak >= 30) return '🔥🔥🔥';
    if (streak >= 20) return '🔥🔥';
    if (streak >= 10) return '🔥';
    if (streak >= 5) return '⚡';
    if (streak >= 1) return '📚';
    return '📖';
  };

  const getStreakMessage = (streak: number) => {
    if (streak >= 30) return 'Incredible! You\'re on fire!';
    if (streak >= 20) return 'Amazing streak! Keep it up!';
    if (streak >= 10) return 'Great job! You\'re building a habit!';
    if (streak >= 5) return 'Nice start! Keep reading daily!';
    if (streak >= 1) return 'Good start! Try to read tomorrow too!';
    return 'Start your reading journey today!';
  };

  const formatTime = (minutes: number) => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  return (
    <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 shadow-lg">
      {/* Header */}
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">Reading Tracker</h2>
        <p className="text-gray-600">Track your reading progress and build streaks</p>
        {isDemo && (
          <div className="mt-2">
            <span className="bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded-full">
              Demo Mode - Click articles to start tracking!
            </span>
          </div>
        )}
      </div>

      {/* Streak Section */}
      <div className="bg-white rounded-lg p-6 mb-6 shadow-sm border border-purple-100">
        <div className="text-center">
          <div className="text-4xl mb-2">{getStreakEmoji(streakData.currentStreak)}</div>
          <div className="text-3xl font-bold text-purple-600 mb-1">
            {streakData.currentStreak} Day{streakData.currentStreak !== 1 ? 's' : ''}
          </div>
          <div className="text-sm text-gray-600 mb-3">Current Streak</div>
          <div className="text-sm text-purple-500 font-medium">
            {getStreakMessage(streakData.currentStreak)}
          </div>
        </div>
        
        {/* Streak Progress */}
        <div className="mt-4">
          <div className="flex justify-between text-sm text-gray-600 mb-2">
            <span>Longest Streak: {streakData.longestStreak} days</span>
            <span>Goal: 30 days</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-500 to-pink-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${Math.min((streakData.currentStreak / 30) * 100, 100)}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-white rounded-lg p-4 shadow-sm border border-purple-100 text-center">
          <div className="text-2xl font-bold text-purple-600">{stats.totalArticlesRead}</div>
          <div className="text-sm text-gray-600">Articles Read</div>
        </div>
        
        <div className="bg-white rounded-lg p-4 shadow-sm border border-purple-100 text-center">
          <div className="text-2xl font-bold text-pink-600">{formatTime(stats.totalReadingTime)}</div>
          <div className="text-sm text-gray-600">Total Time</div>
        </div>
        
        <div className="bg-white rounded-lg p-4 shadow-sm border border-purple-100 text-center">
          <div className="text-2xl font-bold text-green-600">{stats.todayReadCount}</div>
          <div className="text-sm text-gray-600">Today</div>
        </div>
        
        <div className="bg-white rounded-lg p-4 shadow-sm border border-purple-100 text-center">
          <div className="text-2xl font-bold text-blue-600">{stats.weeklyReadCount}</div>
          <div className="text-sm text-gray-600">This Week</div>
        </div>
      </div>

      {/* Streak Calendar */}
      <div className="bg-white rounded-lg p-4 shadow-sm border border-purple-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">30-Day Reading History</h3>
        <div className="grid grid-cols-30 gap-1">
          {streakData.streakHistory.map((day, index) => (
            <div
              key={day.date}
              className={`
                w-6 h-6 rounded-sm text-xs flex items-center justify-center font-medium
                ${day.readCount > 0 
                  ? 'bg-gradient-to-br from-purple-500 to-pink-500 text-white' 
                  : 'bg-gray-100 text-gray-400'
                }
              `}
              title={`${day.date}: ${day.readCount} article${day.readCount !== 1 ? 's' : ''} read`}
            >
              {day.readCount > 0 ? day.readCount : ''}
            </div>
          ))}
        </div>
        <div className="flex justify-between text-xs text-gray-500 mt-2">
          <span>30 days ago</span>
          <span>Today</span>
        </div>
      </div>

      {/* Motivational Quote */}
      <div className="mt-6 text-center">
        <div className="text-lg text-gray-700 italic">
          "The more that you read, the more things you will know. The more that you learn, the more places you'll go."
        </div>
        <div className="text-sm text-gray-500 mt-1">- Dr. Seuss</div>
      </div>
    </div>
  );
};

export default ReadingTracker; 