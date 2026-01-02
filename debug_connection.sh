#!/bin/bash

echo "🔍 Debugging Connection Issues..."
echo "=================================="

echo "1. Checking processes..."
echo "   Backend (uvicorn):"
pgrep -f uvicorn && echo "   ✅ Running" || echo "   ❌ Not running"

echo ""
echo "2. Checking ports..."
echo "   Port 8000 (backend):"
netstat -tuln | grep :8000 && echo "   ✅ Listening" || echo "   ❌ Not listening"

echo "   Port 8501 (frontend):"
netstat -tuln | grep :8501 && echo "   ✅ Listening" || echo "   ❌ Not listening"

echo ""
echo "3. Testing backend API..."
curl -s http://localhost:8000/health || echo "   ❌ Backend not reachable"

echo ""
echo "4. Testing dashboard endpoint..."
curl -s http://localhost:8000/api/dashboard | head -c 200
echo ""

echo ""
echo "5. Checking backend logs..."
tail -5 backend/backend.log 2>/dev/null || echo "   No backend logs found"

echo ""
echo "🎯 Quick fixes:"
echo "   1. Start backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "   2. Check if CORS is enabled in backend"
echo "   3. Make sure backend is on 0.0.0.0 not 127.0.0.1"
