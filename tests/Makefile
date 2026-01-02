.PHONY: help up down build logs clean reset test

help:
	@echo "💎 Shiny Jar Business Suite - Development Commands"
	@echo ""
	@echo "Commands:"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make build     - Rebuild containers"
	@echo "  make logs      - View logs"
	@echo "  make clean     - Remove containers and volumes"
	@echo "  make reset     - Reset database and restart"
	@echo "  make test      - Run tests"
	@echo "  make shell     - Open shell in backend container"
	@echo "  make db-shell  - Open PostgreSQL shell"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build --no-cache

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

reset: down clean up
	@echo "🔄 System reset complete!"

test:
	docker-compose exec backend pytest

shell:
	docker-compose exec backend /bin/bash

db-shell:
	docker-compose exec postgres psql -U shinyjar -d shinyjar_db

migrate:
	docker-compose exec backend alembic upgrade head

seed:
	docker-compose exec backend python scripts/seed_data.py

frontend-logs:
	docker-compose logs -f frontend

backend-logs:
	docker-compose logs -f backend