#!/bin/bash

echo "🚀 Deploying Complete Business Schema..."
cd ~/shiny_jar_suite

# Stop everything
./stop_all.sh

# Reset database completely
docker-compose down -v
docker volume prune -f

# Update init.sql with new schema
# (Copy the new init.sql from above)

# Start fresh
docker-compose up -d postgres
sleep 8

# Test database
docker-compose exec postgres psql -U shinyjar -d shinyjar_db -c "\dt"

# Count records
docker-compose exec postgres psql -U shinyjar -d shinyjar_db -c "
SELECT 'Businesses: ' || COUNT(*) FROM businesses UNION
SELECT 'Customers: ' || COUNT(*) FROM customers UNION
SELECT 'Suppliers: ' || COUNT(*) FROM suppliers UNION
SELECT 'Transactions: ' || COUNT(*) FROM transactions UNION
SELECT 'Budgets: ' || COUNT(*) FROM budgets;
"

echo "✅ New schema deployed!"
echo "Start services: ./start_all.sh"
