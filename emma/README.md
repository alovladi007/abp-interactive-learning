# EMMA - Expert Multimodal & Math Assistant

A production-grade AI system for solving complex mathematical, scientific, and engineering problems using multi-agent orchestration, symbolic computation, and advanced retrieval.

## 🚀 Features

- **Multi-Agent Architecture**: Specialized agents for planning, research, math, numeric computation, code execution, and explanation
- **Hybrid Computation**: Integrates Wolfram, MATLAB, SymPy, NumPy, and JAX
- **Advanced RAG**: Vector search with pgvector, knowledge graphs with Neo4j
- **Secure Sandbox**: Docker-based isolated execution environment
- **Production Ready**: Full observability with OpenTelemetry and Langfuse
- **Modern UI**: Next.js 14 with real-time updates and interactive visualizations

## 📋 Prerequisites

- Docker & Docker Compose (v2.20+)
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space

## 🛠️ Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url> emma
cd emma

# Copy environment variables
cp .env.example .env

# Edit .env with your API keys (OpenAI, Wolfram, etc.)
nano .env
```

### 2. Start with Docker Compose

```bash
# Start all services in development mode
docker compose -f infra/compose/docker-compose.dev.yml up --build

# Or run in background
docker compose -f infra/compose/docker-compose.dev.yml up -d --build
```

This will start:
- **Web UI**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001 (minioadmin/minioadmin)
- **Neo4j Browser**: http://localhost:7474 (neo4j/neo4j_password)

### 3. Initialize Database

```bash
# Run migrations
docker compose -f infra/compose/docker-compose.dev.yml exec api \
  alembic upgrade head

# Load demo corpus (optional)
docker compose -f infra/compose/docker-compose.dev.yml exec api \
  python scripts/load_demo_corpus.py
```

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Next.js   │────▶│   FastAPI   │────▶│  LangGraph  │
│     Web     │     │   Gateway   │     │ Orchestrator│
└─────────────┘     └─────────────┘     └─────────────┘
                            │                    │
                    ┌───────┴────────┐   ┌──────┴──────┐
                    │                 │   │             │
              ┌─────▼─────┐    ┌─────▼───▼─┐    ┌─────▼─────┐
              │PostgreSQL │    │   Redis    │    │   Neo4j   │
              │ pgvector  │    │   Queue    │    │    KG     │
              └───────────┘    └────────────┘    └───────────┘
                                      │
                            ┌─────────┴──────────┐
                            │                    │
                      ┌─────▼─────┐       ┌─────▼─────┐
                      │  Workers  │       │  Sandbox  │
                      │ Dramatiq  │       │   Docker  │
                      └───────────┘       └───────────┘
```

## 📁 Project Structure

```
emma/
├── apps/
│   ├── api/              # FastAPI backend
│   ├── workers/          # Background job processors
│   └── web/              # Next.js frontend
├── packages/
│   ├── emma_core/        # Shared Python libraries
│   ├── emma_prompts/     # System prompts
│   └── emma_ui/          # Shared UI components
├── services/
│   ├── retriever/        # RAG pipeline
│   ├── sandbox/          # Code execution sandbox
│   ├── compute_bridge/   # Math engine adapters
│   └── kg/               # Knowledge graph operations
├── infra/
│   ├── docker/           # Dockerfiles
│   ├── compose/          # Docker Compose configs
│   ├── k8s/              # Kubernetes manifests
│   └── db/               # Database migrations
└── tests/
    ├── api/              # API tests
    ├── e2e/              # End-to-end tests
    └── eval/             # Evaluation suites
```

## 🔧 Configuration

### Environment Variables

Key environment variables in `.env`:

```bash
# LLM Provider
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview

# Compute Engines
WOLFRAM_MODE=cloud  # cloud, alpha, off
WOLFRAM_APP_ID=...
MATLAB_MODE=off     # engine, mps, off

# Features
ENABLE_WEB_SEARCH=true
ENABLE_CODE_EXECUTION=true
SANDBOX_TIMEOUT_SECONDS=30
```

### Compute Bridge Modes

- **Wolfram**: Set `WOLFRAM_MODE=cloud` and provide `WOLFRAM_APP_ID`
- **MATLAB**: Set `MATLAB_MODE=engine` and ensure MATLAB is installed
- **Fallback**: Always uses SymPy/NumPy when external engines are unavailable

## 🧪 Testing

```bash
# Run unit tests
docker compose -f infra/compose/docker-compose.dev.yml exec api \
  pytest tests/api -v

# Run evaluation suite
docker compose -f infra/compose/docker-compose.dev.yml exec api \
  python scripts/run_eval.py --suite gsm8k

# Run E2E tests
npm run test:e2e --prefix apps/web
```

## 📊 API Usage

### Solve a Problem

```bash
curl -X POST http://localhost:8000/v1/chat/solve \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "question": "Solve x^2 + 5x + 6 = 0",
    "need_steps": true,
    "preferred_units": "SI"
  }'
```

### Upload Documents

```bash
curl -X POST http://localhost:8000/v1/ingest/docs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "files=@paper.pdf" \
  -F "files=@notes.md"
```

### Get Execution Trace

```bash
curl http://localhost:8000/v1/trace/{run_id} \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🚢 Production Deployment

### Using Docker Compose

```bash
# Use production compose file
docker compose -f infra/compose/docker-compose.prod.yml up -d
```

### Using Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f infra/k8s/

# Or use Helm
helm install emma infra/k8s/helm-chart/
```

### Environment-Specific Settings

For production:
1. Set strong passwords in `.env`
2. Enable TLS/SSL
3. Configure proper CORS origins
4. Set up monitoring (Prometheus/Grafana)
5. Configure backup strategies

## 🔍 Monitoring

- **Traces**: View in Langfuse dashboard
- **Metrics**: OpenTelemetry exports to configured endpoint
- **Logs**: Structured JSON logs to stdout
- **Health**: GET `/v1/health` endpoint

## 🛡️ Security

- JWT-based authentication
- Rate limiting per user
- Sandboxed code execution
- Input validation and sanitization
- Secrets management via environment variables
- Content filtering for prompt injection

## 📚 Documentation

- **API Docs**: http://localhost:8000/docs
- **Architecture**: See `/docs/architecture.md`
- **Development**: See `/docs/development.md`
- **Deployment**: See `/docs/deployment.md`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Email**: support@emma-ai.com

## 🎯 Roadmap

- [ ] Multi-modal input (images, handwriting)
- [ ] Collaborative problem solving
- [ ] Custom tool creation interface
- [ ] Mobile applications
- [ ] Plugin marketplace
- [ ] Advanced visualization tools

---

Built with ❤️ by the EMMA Team