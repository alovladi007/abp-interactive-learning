.PHONY: help build up down logs clean test migrate backup restore

help:
	@echo "QBank Full Stack Management Commands:"
	@echo "  make build    - Build all Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs"
	@echo "  make clean    - Clean up volumes and images"
	@echo "  make test     - Run tests"
	@echo "  make migrate  - Run database migrations"
	@echo "  make backup   - Backup database"
	@echo "  make restore  - Restore database"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ QBank is running!"
	@echo "📍 Frontend: http://localhost"
	@echo "📍 Backend API: http://localhost:8000"
	@echo "📍 pgAdmin: http://localhost:5050"
	@echo "📍 Flower (Celery): http://localhost:5555"

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -af

test:
	docker-compose exec backend pytest

migrate:
	docker-compose exec backend alembic upgrade head

backup:
	@mkdir -p backups
	docker-compose exec postgres pg_dump -U qbank_admin qbank_production > backups/qbank_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ Database backed up to backups/"

restore:
	@echo "Restoring from latest backup..."
	docker-compose exec -T postgres psql -U qbank_admin qbank_production < $(shell ls -t backups/*.sql | head -1)
	@echo "✅ Database restored"

# Development commands
dev-backend:
	cd qbank-backend && uvicorn app.main:app --reload

dev-frontend:
	python -m http.server 3000

# Production deployment
deploy:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Database management
db-shell:
	docker-compose exec postgres psql -U qbank_admin -d qbank_production

redis-cli:
	docker-compose exec redis redis-cli

# Monitoring
monitor:
	@echo "Opening monitoring dashboards..."
	@open http://localhost:5050  # pgAdmin
	@open http://localhost:5555  # Flower