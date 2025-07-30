export interface ReadingSession {
  id: string;
  articleId: number;
  startTime: Date;
  endTime?: Date;
  duration?: number; // in seconds
  completed: boolean;
}

export interface ReadingStats {
  totalArticlesRead: number;
  totalReadingTime: number; // in minutes
  currentStreak: number;
  longestStreak: number;
  averageReadingTime: number;
  lastReadDate?: Date;
  todayReadCount: number;
  weeklyReadCount: number;
  monthlyReadCount: number;
}

export interface StreakData {
  currentStreak: number;
  longestStreak: number;
  lastReadDate?: Date;
  streakHistory: Array<{
    date: string;
    readCount: number;
  }>;
}

class ReadingTracker {
  private storageKey = 'reading_tracker_data';
  private sessionsKey = 'reading_sessions';
  private statsKey = 'reading_stats';

  // Start a reading session
  startReadingSession(articleId: number): string {
    const sessionId = `session_${Date.now()}_${articleId}`;
    const session: ReadingSession = {
      id: sessionId,
      articleId,
      startTime: new Date(),
      completed: false
    };

    const sessions = this.getSessions();
    sessions.push(session);
    this.saveSessions(sessions);

    return sessionId;
  }

  // End a reading session
  endReadingSession(sessionId: string, completed: boolean = true): void {
    const sessions = this.getSessions();
    const session = sessions.find(s => s.id === sessionId);
    
    if (session) {
      session.endTime = new Date();
      session.duration = Math.floor((session.endTime.getTime() - session.startTime.getTime()) / 1000);
      session.completed = completed;
      
      this.saveSessions(sessions);
      this.updateStats();
    }
  }

  // Get reading statistics
  getReadingStats(): ReadingStats {
    const stats = localStorage.getItem(this.statsKey);
    if (stats) {
      return JSON.parse(stats);
    }

    return {
      totalArticlesRead: 0,
      totalReadingTime: 0,
      currentStreak: 0,
      longestStreak: 0,
      averageReadingTime: 0,
      todayReadCount: 0,
      weeklyReadCount: 0,
      monthlyReadCount: 0
    };
  }

  // Get streak data
  getStreakData(): StreakData {
    const sessions = this.getSessions();
    const completedSessions = sessions.filter(s => s.completed && s.endTime);
    
    if (completedSessions.length === 0) {
      return {
        currentStreak: 0,
        longestStreak: 0,
        streakHistory: []
      };
    }

    // Group sessions by date
    const sessionsByDate = new Map<string, number>();
    completedSessions.forEach(session => {
      const date = session.endTime!.toISOString().split('T')[0];
      sessionsByDate.set(date, (sessionsByDate.get(date) || 0) + 1);
    });

    // Calculate streaks
    const dates = Array.from(sessionsByDate.keys()).sort();
    let currentStreak = 0;
    let longestStreak = 0;
    let tempStreak = 0;
    const today = new Date().toISOString().split('T')[0];
    const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString().split('T')[0];

    for (let i = dates.length - 1; i >= 0; i--) {
      const date = dates[i];
      const expectedDate = new Date(Date.now() - (dates.length - 1 - i) * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
      
      if (date === expectedDate) {
        tempStreak++;
        if (date === today || date === yesterday) {
          currentStreak = tempStreak;
        }
        longestStreak = Math.max(longestStreak, tempStreak);
      } else {
        tempStreak = 0;
      }
    }

    // Create streak history for the last 30 days
    const streakHistory = [];
    for (let i = 29; i >= 0; i--) {
      const date = new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
      streakHistory.push({
        date,
        readCount: sessionsByDate.get(date) || 0
      });
    }

    return {
      currentStreak,
      longestStreak,
      lastReadDate: completedSessions[completedSessions.length - 1].endTime,
      streakHistory
    };
  }

  // Update reading statistics
  private updateStats(): void {
    const sessions = this.getSessions();
    const completedSessions = sessions.filter(s => s.completed && s.endTime);
    
    const totalReadingTime = completedSessions.reduce((total, session) => {
      return total + (session.duration || 0);
    }, 0) / 60; // Convert to minutes

    const today = new Date().toISOString().split('T')[0];
    const todaySessions = completedSessions.filter(s => 
      s.endTime!.toISOString().split('T')[0] === today
    );

    const weekAgo = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
    const weeklySessions = completedSessions.filter(s => 
      s.endTime! >= weekAgo
    );

    const monthAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
    const monthlySessions = completedSessions.filter(s => 
      s.endTime! >= monthAgo
    );

    const streakData = this.getStreakData();

    const stats: ReadingStats = {
      totalArticlesRead: completedSessions.length,
      totalReadingTime: Math.round(totalReadingTime),
      currentStreak: streakData.currentStreak,
      longestStreak: streakData.longestStreak,
      averageReadingTime: completedSessions.length > 0 ? Math.round(totalReadingTime / completedSessions.length) : 0,
      lastReadDate: streakData.lastReadDate,
      todayReadCount: todaySessions.length,
      weeklyReadCount: weeklySessions.length,
      monthlyReadCount: monthlySessions.length
    };

    localStorage.setItem(this.statsKey, JSON.stringify(stats));
  }

  // Get all sessions
  private getSessions(): ReadingSession[] {
    const sessions = localStorage.getItem(this.sessionsKey);
    if (sessions) {
      const parsed = JSON.parse(sessions);
      return parsed.map((s: any) => ({
        ...s,
        startTime: new Date(s.startTime),
        endTime: s.endTime ? new Date(s.endTime) : undefined
      }));
    }
    return [];
  }

  // Save sessions
  private saveSessions(sessions: ReadingSession[]): void {
    localStorage.setItem(this.sessionsKey, JSON.stringify(sessions));
  }

  // Clear all data (for testing)
  clearAllData(): void {
    localStorage.removeItem(this.sessionsKey);
    localStorage.removeItem(this.statsKey);
  }
}

export const readingTracker = new ReadingTracker(); 