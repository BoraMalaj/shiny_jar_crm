#!/bin/bash
echo "🔍 Diagnosing Docker Setup..."
echo "1. Docker version:"
docker --version
echo ""
echo "2. Docker Compose version:"
docker-compose --version
echo ""
echo "3. Current directory structure:"
ls -la
echo ""
echo "4. Checking docker-compose.yml:"
if [ -f "docker-compose.yml" ]; then
    echo "✅ docker-compose.yml exists"
    head -20 docker-compose.yml
else
    echo "❌ docker-compose.yml not found!"
fi
echo ""
echo "5. Checking backend structure:"
if [ -d "backend" ]; then
    find backend -name "*.py" | head -10
else
    echo "❌ backend directory not found!"
fi
