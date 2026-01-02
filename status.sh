#!/bin/bash

echo "📊 Shiny Jar Service Status"
echo "=========================="

# Check Database
echo -n "🐳 Database: "
if docker-compose ps | grep -q "Up"; then
    echo "✅ Running"
else
    echo "❌ Stopped"
fi

# Check Backend
echo -n "🔧 Backend API: "
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Running (http://localhost:8000)"
else
    echo "❌ Stopped"
fi

# Check Frontend
echo -n "🎨 Frontend UI: "
if curl -s http://localhost:8501 > /dev/null; then
    echo "✅ Running (http://localhost:8501)"
else
    echo "❌ Stopped"
fi

# Database stats
echo ""
echo "🗄️  Database Stats:"
docker-compose exec postgres psql -U shinyjar -d shinyjar_db -c "SELECT 'Transactions' as table, COUNT(*) as count FROM transactions UNION ALL SELECT 'Customers', COUNT(*) FROM customers;" 2>/dev/null || echo "   (Database not accessible)"