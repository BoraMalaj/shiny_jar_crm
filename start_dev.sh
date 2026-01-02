#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}💎 Shiny Jar - Development Mode${NC}"
echo "======================================"

# Function to check port
check_port() {
    lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1
}

# 1. Start PostgreSQL
echo -e "${BLUE}[1/3] 🐳 Starting PostgreSQL...${NC}"
if check_port 5433; then
    echo -e "   ✅ PostgreSQL already running"
else
    docker-compose up -d postgres
    echo -e "   ✅ PostgreSQL started on port 5433"
    sleep 3
fi

# 2. Instructions for Terminal 1 (Backend)
echo -e "${BLUE}[2/3] 📋 Open NEW Terminal 1 and run:${NC}"
echo ""
echo "cd ~/shiny_jar_suite/backend"
echo "source venv/bin/activate"
echo "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo -e "${YELLOW}Expected output: 'Uvicorn running on http://0.0.0.0:8000'${NC}"
echo ""

# 3. Instructions for Terminal 2 (Frontend)  
echo -e "${BLUE}[3/3] 📋 Open NEW Terminal 2 and run:${NC}"
echo ""
echo "cd ~/shiny_jar_suite/frontend"
echo "source venv/bin/activate"
echo "streamlit run app.py --server.port=8501"
echo ""
echo -e "${YELLOW}Expected output: 'You can now view your Streamlit app in your browser'${NC}"
echo ""

echo -e "${GREEN}🎯 ACCESS LINKS:${NC}"
echo "   🌐 Frontend:     http://localhost:8501"
echo "   🔧 Backend API:  http://localhost:8000"
echo "   📖 API Docs:     http://localhost:8000/docs"
echo "   🗄️  Database CLI: docker-compose exec postgres psql -U shinyjar -d shinyjar_db"
echo ""
echo -e "${YELLOW}🔑 Default Login: admin / admin123${NC}"
echo ""
echo -e "${GREEN}🚀 Happy developing! Press Ctrl+C in each terminal to stop.${NC}"