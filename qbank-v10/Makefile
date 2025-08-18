.PHONY: help build up down logs clean test migrate

help:
	@echo "Available commands:"
	@echo "  make build    - Build all Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs"
	@echo "  make clean    - Clean up volumes and images"
	@echo "  make test     - Run tests"
	@echo "  make migrate  - Run database migrations"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services starting..."
	@echo "Backend API: http://localhost:8000"
	@echo "Admin UI: http://localhost:3000"
	@echo "Kafka UI: http://localhost:8080"
	@echo "Flower: http://localhost:5555"
	@echo "Grafana: http://localhost:3001"
	@echo "Jaeger: http://localhost:16686"

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

db-shell:
	docker-compose exec postgres psql -U qbank -d qbank

redis-cli:
	docker-compose exec redis redis-cli

# Development shortcuts
dev-backend:
	cd qbank-backend && uvicorn app.main:app --reload

dev-frontend:
	cd admin-ui && npm run dev

dev-worker:
	cd qbank-backend && python -m app.jobs.worker

# Production deployment
deploy-prod:
	kubectl apply -f k8s/

deploy-staging:
	kubectl apply -f k8s/ --namespace=staging