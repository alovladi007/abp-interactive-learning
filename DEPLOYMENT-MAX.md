# MAX AI Research Assistant - Complete Deployment Guide

Complete guide to deploying the MAX AI Research Assistant fullstack application.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start (Development)](#quick-start-development)
3. [Production Deployment with Docker](#production-deployment-with-docker)
4. [Manual Setup](#manual-setup)
5. [Configuration](#configuration)
6. [Testing](#testing)
7. [Troubleshooting](#troubleshooting)

---

## 🖥️ System Requirements

### Minimum
- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB
- **OS**: Linux, macOS, or Windows with WSL2

### Recommended (Production)
- **CPU**: 4+ cores
- **RAM**: 16GB
- **Storage**: 100GB SSD
- **OS**: Ubuntu 22.04 LTS or similar

### Software Dependencies
- Python 3.10+
- PostgreSQL 15+
- Neo4j 5.14+ (Community or Enterprise)
- Redis 7+ (optional, for caching)
- Docker & Docker Compose (for containerized deployment)

---

## 🚀 Quick Start (Development)

### 1. Clone Repository

```bash
cd abp-interactive-learning
```

### 2. Set Up Python Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env  # or use your preferred editor
```

**Minimum required settings for development:**

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=max_db
POSTGRES_USER=max_user
POSTGRES_PASSWORD=dev_password

NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=dev_password
```

### 4. Set Up Databases

#### PostgreSQL

```bash
# Install PostgreSQL (if not already installed)
# Ubuntu/Debian:
sudo apt-get install postgresql postgresql-contrib

# macOS with Homebrew:
brew install postgresql@15

# Start PostgreSQL
sudo systemctl start postgresql  # Linux
brew services start postgresql@15  # macOS

# Create database and user
sudo -u postgres psql <<EOF
CREATE USER max_user WITH PASSWORD 'dev_password';
CREATE DATABASE max_db OWNER max_user;
GRANT ALL PRIVILEGES ON DATABASE max_db TO max_user;
\c max_db
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
EOF

# Load schema
psql -U max_user -d max_db < database/max_schema.sql
```

#### Neo4j

```bash
# Option 1: Docker (Easiest)
docker run -d \
  --name neo4j-max \
  -p 7474:7474 \
  -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/dev_password \
  -e NEO4J_PLUGINS='["graph-data-science", "apoc"]' \
  neo4j:5.14-community

# Option 2: Native installation
# Download from https://neo4j.com/download/
# Follow installation instructions for your OS

# Initialize Neo4j schema
# Wait for Neo4j to start, then:
cat database/max_neo4j.cypher | cypher-shell -u neo4j -p dev_password
```

#### Redis (Optional but recommended)

```bash
# Install Redis
# Ubuntu/Debian:
sudo apt-get install redis-server

# macOS:
brew install redis

# Start Redis
sudo systemctl start redis  # Linux
brew services start redis    # macOS

# Or use Docker:
docker run -d --name redis-max -p 6379:6379 redis:7-alpine
```

### 5. Run Backend

```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate

# Run the MAX application
python main_max.py

# Server will start at http://localhost:8000
```

### 6. Access the Application

- **Frontend Landing Page**: Open `frontend/max-complete.html` in your browser
- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health

---

## 🐳 Production Deployment with Docker

The easiest way to deploy MAX in production.

### 1. Prerequisites

```bash
# Install Docker & Docker Compose
# Follow official guide: https://docs.docker.com/get-docker/

# Verify installation
docker --version
docker-compose --version
```

### 2. Configure Environment

```bash
cd backend

# Copy and edit environment file
cp .env.example .env
nano .env

# Set production values:
# - Strong passwords for databases
# - Set DEBUG=False
# - Configure CORS_ORIGINS for your domain
# - Add API keys if available
```

### 3. Deploy with Docker Compose

```bash
# Start all services
docker-compose -f docker-compose.max.yml up -d

# Check status
docker-compose -f docker-compose.max.yml ps

# View logs
docker-compose -f docker-compose.max.yml logs -f backend
```

### 4. Initialize Databases

```bash
# PostgreSQL schema (runs automatically on first start)
# If you need to re-run:
docker-compose -f docker-compose.max.yml exec postgres \
  psql -U max_user -d max_db < /docker-entrypoint-initdb.d/01-schema.sql

# Neo4j schema
docker-compose -f docker-compose.max.yml exec neo4j \
  cypher-shell -u neo4j -p YOUR_PASSWORD < /var/lib/neo4j/import/schema.cypher
```

### 5. Access Services

- **MAX API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Neo4j Browser**: http://localhost:7474
- **Celery Flower** (monitoring): http://localhost:5555

### 6. Production Checklist

- [ ] Set strong passwords for all services
- [ ] Configure firewall (only expose port 80/443)
- [ ] Set up SSL/TLS with Let's Encrypt
- [ ] Configure proper CORS origins
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure backups for PostgreSQL and Neo4j
- [ ] Set up log rotation
- [ ] Enable rate limiting on Nginx
- [ ] Add authentication/API keys for public APIs

---

## 🔧 Manual Setup (Advanced)

### 1. System Packages

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install -y \
  python3.10 python3.10-venv python3-pip \
  postgresql-15 postgresql-contrib \
  redis-server \
  nginx \
  supervisor

# Install Neo4j separately (see official guide)
```

### 2. Application Setup

```bash
# Create application user
sudo useradd -r -s /bin/bash -m max

# Set up application directory
sudo mkdir -p /opt/max
sudo chown max:max /opt/max

# Copy application files
sudo cp -r backend /opt/max/
sudo cp -r frontend /opt/max/
sudo chown -R max:max /opt/max

# Set up virtual environment
sudo -u max python3.10 -m venv /opt/max/venv
sudo -u max /opt/max/venv/bin/pip install -r /opt/max/backend/requirements.txt
```

### 3. Systemd Service

```bash
# Create systemd service file
sudo nano /etc/systemd/system/max.service
```

```ini
[Unit]
Description=MAX AI Research Assistant
After=network.target postgresql.service neo4j.service

[Service]
Type=simple
User=max
Group=max
WorkingDirectory=/opt/max/backend
Environment="PATH=/opt/max/venv/bin"
EnvironmentFile=/opt/max/backend/.env
ExecStart=/opt/max/venv/bin/python main_max.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable max
sudo systemctl start max
sudo systemctl status max
```

### 4. Nginx Configuration

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/max
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /opt/max/frontend;
        index max-complete.html;
        try_files $uri $uri/ =404;
    }

    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts for long-running requests
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
    }

    # Health check
    location /health {
        proxy_pass http://127.0.0.1:8000;
        access_log off;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/max /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. SSL with Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

---

## ⚙️ Configuration

### Environment Variables

See `.env.example` for all available options.

### Key Configuration Options

#### Database Connection Pooling

```env
# PostgreSQL
POSTGRES_POOL_SIZE=20
POSTGRES_MAX_OVERFLOW=10
POSTGRES_POOL_TIMEOUT=30

# Neo4j
NEO4J_MAX_CONNECTION_POOL_SIZE=50
```

#### Rate Limiting

```env
# Requests per minute
SEMANTIC_SCHOLAR_RATE_LIMIT=100
ARXIV_RATE_LIMIT=50

# Enable API rate limiting
API_RATE_LIMIT_PER_MINUTE=60
```

#### Caching

```env
ENABLE_CACHE=True
CACHE_TTL_SECONDS=3600
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## 🧪 Testing

### Unit Tests

```bash
cd backend

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_max.py -v

# Run with coverage
pytest tests/ --cov=services --cov=api --cov-report=html

# View coverage report
open htmlcov/index.html
```

### API Integration Tests

```bash
# Start the server
python main_max.py

# In another terminal, run API tests
pytest tests/test_max_api.py -v
```

### Load Testing

```bash
# Install locust
pip install locust

# Create load test file (locustfile.py)
# Run load test
locust -f locustfile.py --host=http://localhost:8000
```

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Database Connection Errors

**Error**: `could not connect to server: Connection refused`

**Solution**:
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check if PostgreSQL is listening
sudo netstat -plnt | grep 5432

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

#### 2. Neo4j Connection Issues

**Error**: `Unable to retrieve routing information`

**Solution**:
```bash
# Check Neo4j status
docker logs neo4j-max  # if using Docker
# or
sudo systemctl status neo4j

# Verify Neo4j is accessible
curl http://localhost:7474

# Check credentials
cypher-shell -u neo4j -p YOUR_PASSWORD "RETURN 1"
```

#### 3. Module Import Errors

**Error**: `ModuleNotFoundError: No module named 'services'`

**Solution**:
```bash
# Make sure you're in the backend directory
cd backend

# Reinstall requirements
pip install -r requirements.txt

# Add backend to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 4. CORS Errors in Frontend

**Error**: `Access to fetch blocked by CORS policy`

**Solution**:
```bash
# Update .env
CORS_ORIGINS=http://localhost:3000,http://your-frontend-domain.com

# Restart backend
sudo systemctl restart max
```

### Logging

```bash
# View application logs
tail -f /opt/max/logs/max.log

# View systemd service logs
sudo journalctl -u max -f

# Docker logs
docker-compose -f docker-compose.max.yml logs -f backend
```

### Performance Issues

```bash
# Check system resources
htop

# Check database connections
psql -U max_user -d max_db -c "SELECT count(*) FROM pg_stat_activity;"

# Check Neo4j memory
curl http://localhost:7474/db/system/tx/commit \
  -H "Content-Type: application/json" \
  -d '{"statements":[{"statement":"CALL dbms.listConfig() YIELD name, value WHERE name CONTAINS \"memory\" RETURN name, value"}]}'
```

---

## 📊 Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# PostgreSQL
pg_isready -h localhost -p 5432 -U max_user

# Neo4j
curl http://localhost:7474/db/system/tx/commit \
  -H "Content-Type: application/json" \
  -d '{"statements":[{"statement":"RETURN 1"}]}'

# Redis
redis-cli ping
```

### Metrics

Access Prometheus metrics (if enabled):
```bash
curl http://localhost:8000/metrics
```

### Celery Monitoring

Access Flower dashboard:
```
http://localhost:5555
```

---

## 🔐 Security

### Firewall Configuration

```bash
# UFW (Ubuntu)
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable

# Block direct database access from outside
sudo ufw deny 5432/tcp
sudo ufw deny 7687/tcp
```

### Database Security

```bash
# PostgreSQL: Edit /etc/postgresql/15/main/pg_hba.conf
# Only allow local connections
local   all             max_user                                md5
host    all             max_user        127.0.0.1/32            md5

# Reload PostgreSQL
sudo systemctl reload postgresql
```

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Neo4j Documentation](https://neo4j.com/docs/)
- [Docker Documentation](https://docs.docker.com/)

---

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review logs for error messages
3. Check the [GitHub Issues](https://github.com/your-repo/issues)
4. Contact support: support@eureka-platform.com

---

**Version**: 1.0.0
**Last Updated**: 2025-10-02
