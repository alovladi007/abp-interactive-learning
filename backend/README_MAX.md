# MAX AI Research Assistant - Backend

Complete backend implementation for MAX with multi-source paper search, citation networks, and research synthesis.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 15+
- Neo4j 5.14+ (or Docker)
- Redis 7+ (optional)

### Option 1: Automated Setup (Recommended)

```bash
cd backend

# Run the startup script (handles everything)
./run_max.sh
```

The script will:
- Create virtual environment if needed
- Install dependencies
- Check all services
- Start the MAX API server

### Option 2: Manual Setup

```bash
cd backend

# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your database credentials

# 4. Set up databases
# PostgreSQL:
psql -U postgres -c "CREATE DATABASE max_db OWNER max_user;"
psql -U max_user -d max_db < database/max_schema.sql

# Neo4j (Docker):
docker run -d --name neo4j-max \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/dev_password \
  -e NEO4J_PLUGINS='["graph-data-science", "apoc"]' \
  neo4j:5.14-community

# 5. Start the server
python main_max.py
```

### Option 3: Docker Compose (Production)

```bash
# Start all services at once
docker-compose -f docker-compose.max.yml up -d

# Check status
docker-compose -f docker-compose.max.yml ps

# View logs
docker-compose -f docker-compose.max.yml logs -f backend
```

## 📡 API Endpoints

Once running, access:

- **API Documentation**: http://localhost:8000/api/docs
- **Health Check**: http://localhost:8000/health
- **Root Info**: http://localhost:8000/

### Key Endpoints

#### Search Papers
```bash
POST /api/max/search
{
  "query": "machine learning healthcare",
  "sources": ["semantic_scholar", "arxiv"],
  "year_min": 2020,
  "max_results": 20
}
```

#### Build Citation Network
```bash
POST /api/max/citations/network
{
  "paper_ids": ["paper1", "paper2"],
  "depth": 2
}
```

#### Synthesize Research
```bash
POST /api/max/synthesize
{
  "paper_ids": ["paper1", "paper2", "paper3"],
  "include_methodologies": true,
  "include_gaps": true
}
```

## 🗂️ Project Structure

```
backend/
├── main_max.py                    # Main FastAPI application
├── run_max.sh                     # Startup script
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
│
├── api/
│   ├── max_routes_complete.py     # API routes (800+ lines)
│   └── max_routes.py              # Basic routes
│
├── services/
│   ├── max_core_complete.py       # Core logic (1200+ lines)
│   └── max_core.py                # Basic implementation
│
├── database/
│   ├── max_schema.sql             # PostgreSQL schema
│   └── max_neo4j.cypher           # Neo4j schema
│
├── tests/
│   ├── test_max.py                # Unit tests
│   ├── test_max_api.py            # API tests
│   └── conftest.py                # Test fixtures
│
└── docker-compose.max.yml         # Docker deployment
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=services --cov=api --cov-report=html

# Run specific test file
pytest tests/test_max.py::TestSemanticScholarClient -v
```

## 🔧 Configuration

Key environment variables in `.env`:

```env
# Database
POSTGRES_HOST=localhost
POSTGRES_DB=max_db
POSTGRES_USER=max_user
POSTGRES_PASSWORD=your_password

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

# Optional: API Keys for higher rate limits
SEMANTIC_SCHOLAR_API_KEY=
OPENAI_API_KEY=
```

## 📊 Features Implemented

### ✅ Multi-Source Search
- Semantic Scholar (150M+ papers)
- ArXiv (2M+ preprints)
- PubMed (35M+ biomedical)
- Result deduplication
- Advanced filtering

### ✅ Citation Network Analysis
- NetworkX graph construction
- PageRank influence scoring
- Community detection (Louvain)
- Betweenness centrality
- Co-citation analysis

### ✅ Research Synthesis
- TF-IDF key findings extraction
- Methodology identification
- Research gap detection
- Paper similarity matrix

### ✅ Collections Management
- Create/update/delete collections
- Add papers to collections
- Public/private sharing
- Color coding

### ✅ Citation Export
- APA, MLA, Chicago formats
- IEEE, Vancouver styles
- BibTeX export
- RIS format

### ✅ Database Integration
- PostgreSQL with pgvector
- Neo4j knowledge graph
- Redis caching
- Full CRUD operations

## 🐛 Troubleshooting

### Database Connection Errors

```bash
# Check PostgreSQL
pg_isready -h localhost -p 5432

# Check Neo4j
curl http://localhost:7474

# View logs
tail -f logs/max.log
```

### Module Import Errors

```bash
# Ensure backend is in PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or change port in .env
PORT=8001
```

## 📚 Documentation

- **Full Deployment Guide**: See `/DEPLOYMENT-MAX.md`
- **API Documentation**: http://localhost:8000/api/docs (when running)
- **Test Documentation**: See `tests/README.md`

## 🔒 Security Notes

**For Development:**
- Default credentials are in `.env.example`
- CORS is set to allow all origins

**For Production:**
- Change all default passwords
- Restrict CORS origins
- Enable SSL/TLS
- Use environment-specific configs
- Enable rate limiting
- Set up monitoring

## 📈 Performance

**Expected Performance:**
- Search: 100-500ms per query
- Network analysis: 1-5s for 50 papers
- Synthesis: 2-10s for 10 papers
- Concurrent users: 100+ (with proper resources)

**Optimization:**
- Enable Redis caching
- Use connection pooling
- Implement request queuing for heavy operations
- Scale horizontally with multiple workers

## 🤝 Contributing

See main repository CONTRIBUTING.md

## 📄 License

Part of the E.U.R.E.K.A Platform

---

**Version**: 1.0.0
**Last Updated**: 2025-10-02

🤖 Built with Claude AI
