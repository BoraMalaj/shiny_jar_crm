#!/bin/bash

echo "🚀 Starting Shiny Jar - Local Development Mode"

# Start PostgreSQL in Docker if not running
if ! docker ps | grep -q shinyjar-db; then
    echo "🐳 Starting PostgreSQL container..."
    docker-compose up -d postgres
    sleep 5  # Wait for DB to start
fi

# Set environment variable for local development
export LOCAL_DEV=true

# Start backend
echo "🔧 Starting backend..."
cd backend
source ../venv/bin/activate
python -m app.main