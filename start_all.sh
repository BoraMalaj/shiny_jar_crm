#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}💎 Shiny Jar Business Suite${NC}"
echo "==============================="

# Start Database
echo -e "${BLUE}[1/3] Starting PostgreSQL...${NC}"
cd ~/shiny_jar_suite
docker-compose up -d postgres
sleep 3
echo -e "   ✅ Database: localhost:5433"

# Start Backend
echo -e "${BLUE}[2/3] Starting Backend API...${NC}"
cd backend
export PYTHONPATH=/home/beni/shiny_jar_suite/backend:$PYTHONPATH
source venv/bin/activate
nohup uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
echo $! > backend.pid
sleep 2
echo -e "   ✅ Backend: http://localhost:8000"

# Start Frontend
echo -e "${BLUE}[3/3] Starting Frontend...${NC}"
cd ../frontend
source venv/bin/activate
nohup streamlit run app.py --server.port=8501 > frontend.log 2>&1 &
echo $! > frontend.pid
sleep 3
echo -e "   ✅ Frontend: http://localhost:8501"

echo ""
echo -e "${GREEN}🎉 All services running!${NC}"
echo ""
echo -e "${YELLOW}📊 Quick Access:${NC}"
echo "   🌐 Frontend UI:     http://localhost:8501"
echo "   🔧 API & Docs:      http://localhost:8000/docs"
echo "   🗄️  Database CLI:    ./db_cli.sh"
echo ""
echo -e "${YELLOW}📋 Logs:${NC}"
echo "   Backend logs:  tail -f backend/backend.log"
echo "   Frontend logs: tail -f frontend/frontend.log"
echo "   Docker logs:   docker-compose logs -f"
echo ""
echo -e "${YELLOW}🛑 Stop all: ./stop_all.sh${NC}"