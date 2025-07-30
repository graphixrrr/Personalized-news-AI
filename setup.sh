#!/bin/bash

echo "🚀 Setting up Personalized News AI..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo "❌ pnpm is required but not installed. Please install pnpm and try again."
    exit 1
fi

echo "📦 Installing dependencies..."

# Install backend dependencies
echo "Installing Python dependencies..."
cd backend
python3 -m pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "Installing Node.js dependencies..."
cd frontend
pnpm install
cd ..

# Install root dependencies
pnpm install

echo "✅ Dependencies installed successfully!"

echo "📋 Next steps:"
echo "1. Set up your database (PostgreSQL recommended)"
echo "2. Create a .env file with your configuration:"
echo "   DATABASE_URL=postgresql://username:password@localhost:5432/personalized_news_ai"
echo "   NEWS_API_KEY=6ed6af63cc174b03a5ee8eb8dfad6ca2"
echo "   SECRET_KEY=your-secret-key"
echo ""
echo "3. Run the database setup:"
echo "   pnpm run db:setup"
echo ""
echo "4. Start the development servers:"
echo "   pnpm run dev"
echo ""
echo "🎉 Your Personalized News AI application is ready!" 