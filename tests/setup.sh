#!/bin/bash

echo "💎 Setting up Shiny Jar Business Suite with Docker..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Please edit it with your configuration."
fi

# Build and start containers
echo "🐳 Building and starting Docker containers..."
docker-compose up --build -d

echo ""
echo "🎉 Setup complete! Services are starting..."
echo ""
echo "📊 Services:"
echo "   Frontend:     http://localhost:8501"
echo "   Backend API:  http://localhost:8000"
echo "   API Docs:     http://localhost:8000/docs"
echo "   Database GUI: http://localhost:8080 (Adminer)"
echo ""
echo "🔍 To view logs: docker-compose logs -f"
echo "🛑 To stop:      docker-compose down"
echo ""
echo "💎 Default login:"
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "🚀 Happy coding! Your Shiny Jar Business Suite is ready!"