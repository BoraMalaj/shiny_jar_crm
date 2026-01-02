#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}💎 Shiny Jar - Docker All-in-One Starter${NC}"
echo "========================================"

# Clean up old stuff
echo -e "${YELLOW}🧹 Cleaning up...${NC}"
docker-compose down -v 2>/dev/null

# Build fresh
echo -e "${YELLOW}🔨 Building containers...${NC}"
docker-compose build

# Start services
echo -e "${YELLOW}🚀 Starting services...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to be ready...${NC}"
sleep 10

# Check status
echo ""
echo -e "${GREEN}📊 Service Status:${NC}"
if docker-compose ps | grep -q "Up"; then
    echo -e "✅ All services are running!"
else
    echo -e "${RED}❌ Some services failed to start${NC}"
    docker-compose logs --tail=20
    exit 1
fi

echo ""
echo -e "${GREEN}🎉 Ready to go!${NC}"
echo ""
echo "🌐 Frontend:     http://localhost:8501"
echo "🔧 Backend API:  http://localhost:8000"
echo "📖 API Docs:     http://localhost:8000/docs"
echo "🗄️  Database:     localhost:5433 (PostgreSQL)"
echo ""
echo -e "${YELLOW}Default Credentials:${NC}"
echo "👤 Username: admin"
echo "🔑 Password: admin123"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "📋 View logs:    docker-compose logs -f"
echo "🛑 Stop:         docker-compose down"
echo "🔍 Check status: docker-compose ps"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"