#!/bin/bash

echo "🛑 Stopping Shiny Jar services..."

# Stop frontend
if [ -f "frontend/frontend.pid" ]; then
    kill -9 $(cat frontend/frontend.pid) 2>/dev/null
    rm -f frontend/frontend.pid
fi

# Stop backend
if [ -f "backend/backend.pid" ]; then
    kill -9 $(cat backend/backend.pid) 2>/dev/null
    rm -f backend/backend.pid
fi

# Stop Docker
docker-compose down

echo "✅ All services stopped!"