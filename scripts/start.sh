#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}💎 Shiny Jar Business Suite - Local Development${NC}"
echo "=============================================="

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        return 0
    else
        return 1
    fi
}

# 1. Start PostgreSQL in Docker
echo -e "${YELLOW}🐳 Starting PostgreSQL in Docker...${NC}"
if check_port 5433; then
    echo -e "✅ PostgreSQL already running on port 5433"
else
    docker-compose up -d postgres
    echo -e "✅ PostgreSQL started on localhost:5433"
    sleep 3  # Give DB time to start
fi

# 2. Install backend dependencies
echo -e "${YELLOW}📦 Installing backend dependencies...${NC}"
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# 3. Install frontend dependencies
echo -e "${YELLOW}🎨 Installing frontend dependencies...${NC}"
cd frontend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# 4. Start backend
echo -e "${YELLOW}🚀 Starting backend API...${NC}"
if check_port 8000; then
    echo -e "✅ Backend already running on port 8000"
else
    cd backend
    source venv/bin/activate
    nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > backend.pid
    cd ..
    sleep 2
    echo -e "✅ Backend started on http://localhost:8000"
fi

# 5. Start frontend
echo -e "${YELLOW}🎨 Starting frontend...${NC}"
if check_port 8501; then
    echo -e "✅ Frontend already running on port 8501"
else
    cd frontend
    source venv/bin/activate
    nohup streamlit run app.py --server.port=8501 > frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > frontend.pid
    cd ..
    sleep 3
    echo -e "✅ Frontend started on http://localhost:8501"
fi

echo ""
echo -e "${GREEN}🎉 All services started successfully!${NC}"
echo ""
echo "📊 Services:"
echo -e "  🌐 ${GREEN}Frontend:${NC}     http://localhost:8501"
echo -e "  🔧 ${GREEN}Backend API:${NC}  http://localhost:8000"
echo -e "  📖 ${GREEN}API Docs:${NC}     http://localhost:8000/docs"
echo -e "  🗄️  ${GREEN}Database:${NC}    localhost:5433 (PostgreSQL in Docker)"
echo ""
echo -e "${YELLOW}🔑 Default Credentials:${NC}"
echo "  👤 Username: admin"
echo "  🔑 Password: admin123"
echo ""
echo -e "${YELLOW}📋 Useful Commands:${NC}"
echo "  View backend logs:   tail -f backend/backend.log"
echo "  View frontend logs:  tail -f frontend/frontend.log"
echo "  Stop all services:   ./stop.sh"
echo "  View database:       docker-compose exec postgres psql -U shinyjar -d shinyjar_db"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"