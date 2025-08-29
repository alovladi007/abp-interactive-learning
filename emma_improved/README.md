# EMMA — Expert Multimodal & Math Assistant (Enhanced)

## 🚀 Features
- LangGraph orchestration
- Hybrid retrieval
- Multiple math engines
- Secure sandbox
- WebSocket streaming
- Beautiful UI with LaTeX

## Quick Start
```bash
docker compose up --build
# Web: http://localhost:3000
# API: http://localhost:8000
```


---

## 🎯 Optional Full Stack Add-Ons (pgvector + Neo4j + LangGraph + Sandbox)

This repo includes **optional** services you can enable without breaking the basic demo:

- **pgvector** (Postgres 16 + `vector` extension) for proper embedding store
- **Neo4j** (simple KG adapter + tiny seeded graph from demo corpus)
- **LangGraph** planner (set `USE_LANGGRAPH=1` to route through graph)
- **Sandbox Runner** (FastAPI microservice for safe Python execution)

### Start the full stack (Docker)
```bash
cd emma_improved
docker compose -f infra/compose/docker-compose.full.yml up --build
# web:  http://localhost:3000
# api:  http://localhost:8000
# db:   postgres://postgres:postgres@localhost:5432/emma
# neo4j: http://localhost:7474 (neo4j/neo4jpassword)
# sandbox: http://localhost:8081
```

### Seed pgvector from demo corpus
```bash
docker compose -f infra/compose/docker-compose.full.yml exec api python scripts/seed_pgvector.py
```

### Seed Neo4j knowledge graph
```bash
docker compose -f infra/compose/docker-compose.full.yml exec api python scripts/seed_kg.py
```

Toggle "Use LangGraph" in the web UI to use the planner graph.
Click "Run Sandbox Demo" to test code execution.
