# Personalized News AI

A sophisticated news aggregation platform that uses AI to deliver personalized news content based on user reading patterns and preferences.

## Features

- **AI-Powered Personalization**: Machine learning algorithms analyze user reading behavior to recommend relevant articles
- **Real-time News**: Latest news from multiple sources via NewsAPI
- **User Preferences**: Customizable categories and topics
- **Reading Analytics**: Track reading patterns and preferences
- **Modern UI**: Clean, responsive design with dark/light mode
- **Smart Recommendations**: Content-based and collaborative filtering

## Tech Stack

- **Backend**: Python (FastAPI)
- **Frontend**: React with TypeScript
- **Database**: PostgreSQL with Prisma ORM
- **AI/ML**: Scikit-learn, pandas, numpy
- **News API**: NewsAPI.org integration
- **Styling**: Tailwind CSS

## Getting Started

1. Install dependencies:
   ```bash
   pnpm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Add your NewsAPI key: NEWS_API_KEY=your_api_key_here
   ```

3. Run the development server:
   ```bash
   pnpm dev
   ```

## API Endpoints

- `GET /api/news` - Get personalized news feed
- `POST /api/preferences` - Update user preferences
- `GET /api/analytics` - Get reading analytics
- `POST /api/feedback` - Submit article feedback

## AI Features

- Content-based filtering based on article categories and keywords
- Collaborative filtering using user similarity
- Reading time prediction
- Topic clustering and trend analysis