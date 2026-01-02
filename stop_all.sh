#!/bin/bash

echo "🛑 Stopping Shiny Jar services..."

# Stop Frontend
if [ -f "frontend/frontend.pid" ]; then
    echo "   Stopping frontend..."
    kill -9 $(cat frontend/frontend.pid) 2>/dev/null
    rm -f frontend/frontend.pid
fi

# Stop Backend
if [ -f "backend/backend.pid" ]; then
    echo "   Stopping backend..."
    kill -9 $(cat backend/backend.pid) 2>/dev/null
    rm -f backend/backend.pid
fi

# Stop Docker
echo "   Stopping database..."
cd ~/shiny_jar_suite
docker-compose down

echo ""
echo "✅ All services stopped!"