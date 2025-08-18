#!/bin/bash

# Start QBank Backend Services
echo "Starting QBank Backend Services..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi

# Start PostgreSQL
docker run -d \
  --name qbank-postgres \
  -e POSTGRES_DB=qbank \
  -e POSTGRES_USER=qbank \
  -e POSTGRES_PASSWORD=qbank123 \
  -p 5432:5432 \
  postgres:15

# Start Redis
docker run -d \
  --name qbank-redis \
  -p 6379:6379 \
  redis:7-alpine

# Start the FastAPI backend
cd /workspace/qbank-backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

echo "Backend services started!"
echo "API: http://localhost:8000"
echo "PostgreSQL: localhost:5432"
echo "Redis: localhost:6379"