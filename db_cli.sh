#!/bin/bash

cd ~/shiny_jar_suite
echo "🔌 Connecting to PostgreSQL..."
echo "   Database: shinyjar_db"
echo "   User:     shinyjar"
echo ""
echo "Useful commands inside psql:"
echo "   \dt                 - List all tables"
echo "   SELECT * FROM table; - View data"
echo "   \q                 - Exit"
echo ""
docker-compose exec postgres psql -U shinyjar -d shinyjar_db    

# backup database: docker exec -t shinyjar-db pg_dump -U shinyjar -d shinyjar_db > shinyjar_db.sql