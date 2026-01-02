#!/bin/bash

echo "🔍 Testing Docker Setup..."

# 1. Check if containers are running
echo "1. Running containers:"
docker ps

echo ""
echo "2. Check backend logs:"
docker logs shinyjar-backend --tail 20

echo ""
echo "3. Check PostgreSQL logs:"
docker logs shinyjar-db --tail 10

echo ""
echo "4. Test backend API:"
curl -s http://localhost:8000/health | python -m json.tool

echo ""
echo "5. Test frontend:"
curl -s -I http://localhost:8501 | head -1

echo ""
echo "📊 Services:"
echo "✅ Backend:  http://localhost:8000"
echo "✅ Frontend: http://localhost:8501"
echo "✅ API Docs: http://localhost:8000/docs"