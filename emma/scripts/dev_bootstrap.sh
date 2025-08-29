#!/bin/bash

# EMMA Development Bootstrap Script
# This script sets up the development environment

set -e

echo "🚀 EMMA Development Bootstrap"
echo "============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}❌ $1 is not installed${NC}"
        exit 1
    else
        echo -e "${GREEN}✅ $1 is installed${NC}"
    fi
}

echo "Checking prerequisites..."
check_command docker
check_command docker-compose
check_command python3
check_command node
check_command npm

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created${NC}"
    echo -e "${YELLOW}⚠️  Please edit .env and add your API keys${NC}"
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p data/{postgres,redis,neo4j,minio}
mkdir -p logs
mkdir -p tmp

# Install Python dependencies (optional for local development)
if [ "$1" == "--install-local" ]; then
    echo -e "${YELLOW}Installing Python dependencies locally...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -U pip setuptools wheel
    pip install -e .
    echo -e "${GREEN}✅ Python dependencies installed${NC}"
fi

# Install Node dependencies for web (optional for local development)
if [ "$1" == "--install-local" ]; then
    echo -e "${YELLOW}Installing Node dependencies...${NC}"
    cd apps/web
    npm install
    cd ../..
    echo -e "${GREEN}✅ Node dependencies installed${NC}"
fi

# Pull Docker images
echo -e "${YELLOW}Pulling Docker images...${NC}"
docker-compose -f infra/compose/docker-compose.dev.yml pull

# Start services
echo -e "${YELLOW}Starting services...${NC}"
docker-compose -f infra/compose/docker-compose.dev.yml up -d

# Wait for services to be healthy
echo "Waiting for services to be healthy..."
sleep 10

# Check service health
check_service() {
    if docker-compose -f infra/compose/docker-compose.dev.yml exec -T $1 $2 &> /dev/null; then
        echo -e "${GREEN}✅ $1 is healthy${NC}"
    else
        echo -e "${YELLOW}⚠️  $1 is starting...${NC}"
    fi
}

check_service postgres "pg_isready -U emma"
check_service redis "redis-cli ping"
check_service api "curl -f http://localhost:8000/v1/health"

# Run database migrations
echo -e "${YELLOW}Running database migrations...${NC}"
docker-compose -f infra/compose/docker-compose.dev.yml exec -T api alembic upgrade head
echo -e "${GREEN}✅ Database migrations complete${NC}"

# Create MinIO bucket
echo -e "${YELLOW}Creating MinIO bucket...${NC}"
docker-compose -f infra/compose/docker-compose.dev.yml exec -T minio \
    mc alias set local http://localhost:9000 minioadmin minioadmin
docker-compose -f infra/compose/docker-compose.dev.yml exec -T minio \
    mc mb local/emma-storage --ignore-existing
echo -e "${GREEN}✅ MinIO bucket created${NC}"

# Summary
echo ""
echo "============================="
echo -e "${GREEN}🎉 EMMA Development Environment Ready!${NC}"
echo ""
echo "Services running:"
echo "  • Web UI:        http://localhost:3000"
echo "  • API:           http://localhost:8000"
echo "  • API Docs:      http://localhost:8000/docs"
echo "  • MinIO Console: http://localhost:9001"
echo "  • Neo4j Browser: http://localhost:7474"
echo ""
echo "Default credentials:"
echo "  • MinIO: minioadmin/minioadmin"
echo "  • Neo4j: neo4j/neo4j_password"
echo ""
echo "Next steps:"
echo "  1. Edit .env file with your API keys"
echo "  2. Load demo data: docker-compose exec api python scripts/load_demo_corpus.py"
echo "  3. Open http://localhost:3000 in your browser"
echo ""
echo "To stop services: docker-compose -f infra/compose/docker-compose.dev.yml down"
echo "To view logs: docker-compose -f infra/compose/docker-compose.dev.yml logs -f"