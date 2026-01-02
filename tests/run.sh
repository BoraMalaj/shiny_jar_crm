#!/bin/bash

echo "💎 Starting Shiny Jar Business Suite..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found!"
    echo "   Make sure you're in the project root directory."
    exit 1
fi

# Stop any existing containers
echo "🛑 Stopping any existing containers..."
docker-compose down 2>/dev/null

# Build and start
echo "🔨 Building containers..."
docker-compose build

echo "🚀 Starting all services..."
docker-compose up -d

echo ""
echo "🎉 All services started!"
echo ""
echo "📊 Services:"
echo "   🌐 Frontend:     http://localhost:8501"
echo "   🔧 Backend API:  http://localhost:8000"
echo "   📖 API Docs:     http://localhost:8000/docs"
echo "   🗄️  Database GUI: http://localhost:8080"
echo ""
echo "🔍 View logs:    docker-compose logs -f"
echo "🛑 Stop:         docker-compose down"
echo ""
echo "💎 Default Login:"
echo "   👤 Username: admin"
echo "   🔑 Password: admin123"