#!/bin/bash

# ============================================================================
# MAX AI Research Assistant - Development Startup Script
# ============================================================================

set -e

echo "🚀 Starting MAX AI Research Assistant..."
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment not found. Creating...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}.env file not found. Copying from .env.example...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠️  Please edit .env with your configuration before continuing!${NC}"
    exit 1
fi

# Source environment variables
export $(cat .env | grep -v '^#' | xargs)

echo -e "${GREEN}✓${NC} Environment loaded"

# Check PostgreSQL
echo -n "Checking PostgreSQL... "
if command -v psql &> /dev/null; then
    if pg_isready -h ${POSTGRES_HOST:-localhost} -p ${POSTGRES_PORT:-5432} &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${RED}✗${NC}"
        echo -e "${YELLOW}PostgreSQL is not running. Start it with:${NC}"
        echo "  sudo systemctl start postgresql  # Linux"
        echo "  brew services start postgresql@15  # macOS"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠${NC} psql not found (PostgreSQL may still be running)"
fi

# Check Neo4j
echo -n "Checking Neo4j... "
if curl -s http://localhost:7474 &> /dev/null; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${YELLOW}⚠${NC} Neo4j not responding on port 7474"
    echo -e "${YELLOW}Start Neo4j with:${NC}"
    echo "  docker run -d --name neo4j-max -p 7474:7474 -p 7687:7687 \\"
    echo "    -e NEO4J_AUTH=neo4j/dev_password \\"
    echo "    -e NEO4J_PLUGINS='[\"graph-data-science\", \"apoc\"]' \\"
    echo "    neo4j:5.14-community"
fi

# Check Redis (optional)
echo -n "Checking Redis... "
if command -v redis-cli &> /dev/null; then
    if redis-cli ping &> /dev/null; then
        echo -e "${GREEN}✓${NC}"
    else
        echo -e "${YELLOW}⚠${NC} Redis not running (optional - caching disabled)"
    fi
else
    echo -e "${YELLOW}⚠${NC} Redis not installed (optional)"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  MAX AI Research Assistant${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "API Server: http://localhost:${PORT:-8000}"
echo "API Docs:   http://localhost:${PORT:-8000}/api/docs"
echo "Health:     http://localhost:${PORT:-8000}/health"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop${NC}"
echo ""

# Start the application
python main_max.py
