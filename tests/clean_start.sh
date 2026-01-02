#!/bin/bash

echo "🧹 Cleaning everything..."
docker-compose down -v 2>/dev/null
docker rm -f $(docker ps -aq) 2>/dev/null
docker rmi -f $(docker images -q) 2>/dev/null

echo "🐳 Building fresh containers..."
docker-compose build --no-cache

echo "🚀 Starting all services..."
docker-compose up