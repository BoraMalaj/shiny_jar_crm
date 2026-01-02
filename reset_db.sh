#!/bin/bash

echo "🔄 Resetting Shiny Jar Database..."

cd ~/shiny_jar_suite

# Stop services
./stop_all.sh > /dev/null 2>&1

# Remove old data
echo "   Removing old database..."
docker-compose down -v

# Start fresh
echo "   Creating fresh database..."
docker-compose up -d postgres
sleep 5

echo ""
echo "✅ Database reset complete!"
echo "Run ./start_all.sh to start services."