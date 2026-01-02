#!/bin/bash

echo "Adding sample data to Shiny Jar..."

# Add sample transactions
curl -X POST http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"amount": 150, "type": "expense", "category": "Materials", "description": "Silver chains"}' \
  -s | jq

curl -X POST http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"amount": 45, "type": "expense", "category": "Packaging", "description": "Jewelry boxes"}' \
  -s | jq

curl -X POST http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"amount": 89, "type": "income", "category": "Jewelry Sales", "description": "Necklace sale"}' \
  -s | jq

curl -X POST http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"amount": 120, "type": "income", "category": "Custom Orders", "description": "Custom earrings"}' \
  -s | jq

# Add sample customers
curl -X POST http://localhost:8000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "Maria Silva", "instagram_handle": "maria_silva", "email": "maria@email.com", "total_spent": 250}' \
  -s | jq

curl -X POST http://localhost:8000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "instagram_handle": "john_jewelry", "email": "john@email.com", "total_spent": 180}' \
  -s | jq

echo "✅ Sample data added!"
echo "Check dashboard at: http://localhost:8501"
