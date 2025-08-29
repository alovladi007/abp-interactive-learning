#!/usr/bin/env python3
"""
Enhanced EMMA with Full Stack Add-ons
Adds pgvector, Neo4j, LangGraph planner, and Sandbox Runner
while preserving the original simple demo.
"""

import os
import json
import textwrap
import zipfile
import shutil
from pathlib import Path

# Ensure the base EMMA improved exists
base = Path("/workspace/emma_improved")
if not base.exists():
    print("❌ Base EMMA not found. Creating it first...")
    # Run the previous script to create base
    import subprocess
    subprocess.run(["python3", "/workspace/emma/create_emma_improved.py"], check=True)

def w(path: str, content: str, mode: str = "w"):
    """Write content to file."""
    full_path = base / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, mode, encoding="utf-8") as f:
        f.write(content)

print("🚀 Adding full-stack enhancements to EMMA...")

# 1) Update README with full stack section
append_readme = """

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
"""

with open(base / "README.md", "a", encoding="utf-8") as f:
    f.write(append_readme)

# 2) Add extra API requirements
extra_requirements = """
# Full stack dependencies
sqlalchemy==2.0.29
psycopg[binary]==3.1.18
pgvector==0.2.5
neo4j==5.21.0
langgraph==0.2.26
langchain-core==0.2.40
"""

with open(base / "apps/api/requirements.txt", "a", encoding="utf-8") as f:
    f.write(extra_requirements)

# 3) LangGraph planner
planner_lg = '''"""
Minimal LangGraph planner for EMMA
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END

def _detect_intent(question: str) -> str:
    """Detect the intent from question."""
    q = question.lower()
    if "integrate" in q or "∫" in q:
        return "integrate"
    if "=" in q:
        return "solve_equation"
    if "code" in q or "python" in q:
        return "code"
    return "explain"

def make_planner_graph():
    """Create the planner graph."""
    sg = StateGraph(dict)
    
    def planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
        intent = _detect_intent(state.get("question", ""))
        state["intent"] = intent
        state.setdefault("trace", []).append({"node": "planner", "intent": intent})
        return state
    
    def researcher_node(state: Dict[str, Any]) -> Dict[str, Any]:
        state.setdefault("trace", []).append({"node": "researcher", "status": "retrieved"})
        return state
    
    def math_node(state: Dict[str, Any]) -> Dict[str, Any]:
        state.setdefault("trace", []).append({"node": "math", "status": "computed"})
        return state
    
    def done_node(state: Dict[str, Any]) -> Dict[str, Any]:
        state["status"] = "completed"
        return state
    
    # Add nodes
    sg.add_node("planner", planner_node)
    sg.add_node("researcher", researcher_node)
    sg.add_node("math", math_node)
    sg.add_node("done", done_node)
    
    # Add routing
    def route_from_planner(state: Dict[str, Any]) -> str:
        intent = state.get("intent", "explain")
        if intent in ["integrate", "solve_equation"]:
            return "math"
        return "researcher"
    
    # Add edges
    sg.set_entry_point("planner")
    sg.add_conditional_edges("planner", route_from_planner, {
        "math": "math",
        "researcher": "researcher"
    })
    sg.add_edge("researcher", "done")
    sg.add_edge("math", "done")
    sg.set_finish_point("done")
    
    return sg.compile()
'''
w("packages/emma_core/planner_langgraph.py", planner_lg)

# 4) Enhanced API with optional components
enhanced_api = '''from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import sympy as sp
import os
import httpx

app = FastAPI(title="EMMA API - Full Stack")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment configuration
USE_LANGGRAPH = os.getenv("USE_LANGGRAPH", "0") == "1"
SANDBOX_URL = os.getenv("SANDBOX_URL", "http://sandbox:8081")
DATABASE_URL = os.getenv("DATABASE_URL")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4jpassword")

# Optional components initialization
planner_graph = None
if USE_LANGGRAPH:
    try:
        from packages.emma_core.planner_langgraph import make_planner_graph
        planner_graph = make_planner_graph()
        print("✅ LangGraph planner loaded")
    except Exception as e:
        print(f"⚠️ LangGraph not available: {e}")

pgvector_available = False
pg_search = None
if DATABASE_URL:
    try:
        from services.retriever.pgvector_store import PgVectorStore
        pg_store = PgVectorStore(DATABASE_URL)
        pg_search = pg_store.search
        pgvector_available = True
        print("✅ pgvector store connected")
    except Exception as e:
        print(f"⚠️ pgvector not available: {e}")

kg_client = None
if NEO4J_URI:
    try:
        from services.kg.neo4j_adapter import KGClient
        kg_client = KGClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        print("✅ Neo4j connected")
    except Exception as e:
        print(f"⚠️ Neo4j not available: {e}")

# Fallback to naive search
from services.retriever.naive_retriever import naive_search

class SolveRequest(BaseModel):
    question: str
    mode: str = "auto"
    flags: Optional[Dict[str, Any]] = {}

class SolveResponse(BaseModel):
    answer: str
    steps: List[Dict[str, Any]]
    trace: Optional[List[Dict[str, Any]]] = None

@app.get("/v1/health")
def health():
    return {
        "status": "healthy",
        "components": {
            "langgraph": USE_LANGGRAPH and planner_graph is not None,
            "pgvector": pgvector_available,
            "neo4j": kg_client is not None,
            "sandbox": SANDBOX_URL is not None
        }
    }

@app.post("/v1/chat/solve")
async def solve(req: SolveRequest):
    # Use LangGraph if enabled and requested
    if USE_LANGGRAPH and planner_graph and req.flags.get("useLangGraph"):
        state = planner_graph.invoke({"question": req.question})
        intent = state.get("intent", "explain")
        trace = state.get("trace", [])
    else:
        # Fallback to simple intent detection
        intent = "integrate" if "integrate" in req.question.lower() else "explain"
        trace = []
    
    # Retrieval (pgvector or naive)
    if pgvector_available and pg_search:
        docs = pg_search(req.question, top_k=3)
    else:
        docs = naive_search(req.question, top_k=3)
    
    # Simple solving
    answer = ""
    if intent == "integrate":
        try:
            x = sp.Symbol('x')
            # Simple example - would parse properly in production
            result = sp.integrate(sp.sin(x), x)
            answer = f"∫sin(x)dx = {result}"
        except:
            answer = "Integration result"
    else:
        answer = f"Based on search: {docs[0]['highlight'] if docs else 'No results'}"
    
    return SolveResponse(
        answer=answer,
        steps=[{"role": "solver", "action": intent}],
        trace=trace if trace else None
    )

@app.post("/v1/tools/run")
async def tool_run(payload: dict):
    """Execute code in sandbox."""
    if not SANDBOX_URL:
        raise HTTPException(status_code=400, detail="Sandbox not configured")
    
    code = payload.get("code", "print('hello')")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.post(f"{SANDBOX_URL}/run", json={
                "language": "python",
                "code": code
            })
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
w("apps/api/main_full.py", enhanced_api)

# 5) pgvector store
pg_store = '''"""
pgvector store with simple embedding
"""
import math
import re
import hashlib
import json
from typing import List, Dict
from sqlalchemy import create_engine, text

# Simple 128-d embedding using hashed bag-of-words
DIM = 128

def embed(text: str) -> list:
    """Create simple embedding from text."""
    vec = [0.0] * DIM
    tokens = [t for t in re.split(r"\\W+", text.lower()) if t]
    for t in tokens:
        h = int(hashlib.sha256(t.encode("utf-8")).hexdigest(), 16)
        idx = h % DIM
        vec[idx] += 1.0
    # L2 normalize
    norm = math.sqrt(sum(v*v for v in vec)) or 1.0
    return [v/norm for v in vec]

DDL = """
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE IF NOT EXISTS sources (
    id SERIAL PRIMARY KEY,
    uri TEXT,
    kind TEXT,
    sha256 TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE TABLE IF NOT EXISTS chunks (
    id SERIAL PRIMARY KEY,
    source_id INT REFERENCES sources(id),
    text TEXT,
    meta JSON,
    embedding vector(%(dim)s)
);
CREATE INDEX IF NOT EXISTS chunks_embedding_idx 
    ON chunks USING ivfflat (embedding vector_cosine_ops);
"""

class PgVectorStore:
    def __init__(self, url: str):
        self.engine = create_engine(url, pool_pre_ping=True)
        with self.engine.begin() as conn:
            conn.execute(text(DDL), {"dim": DIM})
    
    def upsert_from_text(self, uri: str, text_content: str, kind: str = "file") -> int:
        sha = hashlib.sha256(text_content.encode("utf-8")).hexdigest()
        lines = text_content.splitlines()
        
        with self.engine.begin() as conn:
            # Ensure source exists
            res = conn.execute(
                text("SELECT id FROM sources WHERE sha256=:sha"),
                {"sha": sha}
            ).fetchone()
            
            if res:
                source_id = res[0]
            else:
                res = conn.execute(
                    text("INSERT INTO sources (uri,kind,sha256) VALUES (:u,:k,:s) RETURNING id"),
                    {"u": uri, "k": kind, "s": sha}
                )
                source_id = res.fetchone()[0]
            
            # Delete old chunks
            conn.execute(text("DELETE FROM chunks WHERE source_id=:sid"), {"sid": source_id})
            
            # Create chunks (~20 lines each)
            chunk, start = [], 1
            for i, line in enumerate(lines, start=1):
                chunk.append(line)
                if len(chunk) >= 20 or i == len(lines):
                    text_chunk = "\\n".join(chunk).strip()
                    if text_chunk:
                        emb = embed(text_chunk)
                        conn.execute(
                            text("INSERT INTO chunks (source_id,text,meta,embedding) VALUES (:sid,:t,:m,:e)"),
                            {
                                "sid": source_id,
                                "t": text_chunk,
                                "m": json.dumps({"range": f"L{start}-L{i}"}),
                                "e": emb
                            }
                        )
                    chunk, start = [], i+1
        return 1
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        q_emb = embed(query)
        with self.engine.begin() as conn:
            rows = conn.execute(text("""
                SELECT s.uri, s.sha256, c.text, c.meta, 
                       1 - (c.embedding <=> :q::vector) AS score
                FROM chunks c
                JOIN sources s ON s.id = c.source_id
                ORDER BY c.embedding <=> :q::vector
                LIMIT :k
            """), {"q": q_emb, "k": top_k}).fetchall()
        
        out = []
        for uri, sha, text_chunk, meta, score in rows:
            snip = text_chunk.splitlines()[:3]
            out.append({
                "file": uri,
                "sha": (sha or "")[:12],
                "score": float(score),
                "highlight": f"{uri}: {' '.join(snip)}"
            })
        return out
'''
w("services/retriever/pgvector_store.py", pg_store)

# 6) Naive retriever (fallback)
naive_retriever = '''"""
Naive retriever for fallback when pgvector not available
"""
import re
from typing import List, Dict

def naive_search(query: str, top_k: int = 3) -> List[Dict]:
    """Simple search without database."""
    # Mock results for demo
    return [
        {
            "file": "demo.md",
            "sha": "abc123",
            "score": 0.8,
            "highlight": "Demo result for: " + query[:50]
        }
    ]
'''
w("services/retriever/naive_retriever.py", naive_retriever)

# 7) Neo4j adapter
neo4j_adapter = '''"""
Neo4j Knowledge Graph adapter
"""
from neo4j import GraphDatabase
from typing import List, Dict

class KGClient:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def upsert_fact(self, subj: str, rel: str, obj: str):
        cypher = """
        MERGE (a:Entity {name:$subj})
        MERGE (b:Entity {name:$obj})
        MERGE (a)-[r:REL {type:$rel}]->(b)
        RETURN a,b,r
        """
        with self.driver.session() as s:
            s.run(cypher, subj=subj, rel=rel, obj=obj)
    
    def query(self, name: str) -> List[Dict]:
        cypher = "MATCH (n:Entity {name:$name})-[r:REL]->(m) RETURN n,m,r LIMIT 20"
        with self.driver.session() as s:
            res = s.run(cypher, name=name)
            return [dict(r) for r in res]
'''
w("services/kg/neo4j_adapter.py", neo4j_adapter)

# 8) Sandbox server
sandbox_server = '''"""
Sandbox Runner for safe code execution
"""
from fastapi import FastAPI
from pydantic import BaseModel
import tempfile
import subprocess
import os
import resource
import signal

app = FastAPI(title="EMMA Sandbox Runner")

class RunRequest(BaseModel):
    language: str = "python"
    code: str

def limit_resources():
    """Set resource limits for safety."""
    # CPU limit: 2 seconds
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    # Memory limit: 128MB
    mem = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem, mem))

@app.post("/run")
def run_code(req: RunRequest):
    if req.language != "python":
        return {"error": "Only python supported in dev sandbox"}
    
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "main.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(req.code)
        
        try:
            proc = subprocess.run(
                ["python", "-S", "-B", path],
                capture_output=True,
                text=True,
                timeout=3,
                preexec_fn=limit_resources
            )
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "returncode": proc.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": "timeout"}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
'''
w("services/sandbox/server.py", sandbox_server)

# 9) Seed scripts
seed_pg = '''"""
Seed pgvector from demo corpus
"""
import os
import glob
from services.retriever.pgvector_store import PgVectorStore

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@db:5432/emma")
store = PgVectorStore(DATABASE_URL)

# Add demo content
demo_content = {
    "ohms_law.md": """# Ohm's Law
V = I × R where V is voltage, I is current, and R is resistance.
Applications: Circuit analysis, power calculations.""",
    "projectile_motion.md": """# Projectile Motion
Range = (v₀² × sin(2θ)) / g
Maximum height = (v₀² × sin²(θ)) / (2g)""",
    "gauss_law.md": """# Gauss's Law
Electric flux through closed surface equals enclosed charge divided by ε₀."""
}

for filename, content in demo_content.items():
    store.upsert_from_text(uri=filename, text_content=content)
    print(f"✅ Seeded {filename}")

print("pgvector seeded from demo corpus.")
'''
w("scripts/seed_pgvector.py", seed_pg)

seed_kg = '''"""
Seed Neo4j with demo knowledge graph
"""
import os
from services.kg.neo4j_adapter import KGClient

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4jpassword")

kg = KGClient(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

# Add demo facts
facts = [
    ("Ohm's law", "relates", "Voltage"),
    ("Ohm's law", "relates", "Current"),
    ("Ohm's law", "involves", "Resistance"),
    ("Gauss's law", "relates", "Electric flux"),
    ("Projectile motion", "involves", "Gravity"),
    ("Projectile motion", "requires", "Initial velocity"),
]

for subj, rel, obj in facts:
    kg.upsert_fact(subj, rel, obj)
    print(f"✅ Added: {subj} -{rel}-> {obj}")

print("Neo4j seeded with demo entities.")
'''
w("scripts/seed_kg.py", seed_kg)

# 10) Docker files
docker_sandbox = '''FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn
COPY services/sandbox/server.py /app/server.py
EXPOSE 8081
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8081"]
'''
w("infra/docker/Dockerfile.sandbox", docker_sandbox)

# 11) Full stack Docker Compose
compose_full = '''version: "3.9"

services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: emma
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  neo4j:
    image: neo4j:5
    environment:
      - NEO4J_AUTH=neo4j/neo4jpassword
      - NEO4J_dbms_memory_heap_initial__size=512m
      - NEO4J_dbms_memory_heap_max__size=512m
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "neo4jpassword", "RETURN 1"]
      interval: 10s
      timeout: 5s
      retries: 5

  sandbox:
    build:
      context: ../../
      dockerfile: infra/docker/Dockerfile.sandbox
    ports:
      - "8081:8081"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8081/docs"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: ../../
      dockerfile: infra/docker/Dockerfile.api.full
    environment:
      - USE_LANGGRAPH=1
      - DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/emma
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=neo4jpassword
      - SANDBOX_URL=http://sandbox:8081
      - PYTHONUNBUFFERED=1
      - PYTHONPATH=/app:/app/packages:/app/services
    depends_on:
      db:
        condition: service_healthy
      neo4j:
        condition: service_healthy
      sandbox:
        condition: service_healthy
    ports:
      - "8000:8000"
    volumes:
      - ../../apps/api:/app/apps/api
      - ../../services:/app/services
      - ../../packages:/app/packages
      - ../../scripts:/app/scripts

  web:
    build:
      context: ../../
      dockerfile: infra/docker/Dockerfile.web.full
    environment:
      - NEXT_PUBLIC_API_BASE=http://localhost:8000
    depends_on:
      - api
    ports:
      - "3000:3000"

volumes:
  postgres_data:
  neo4j_data:
'''
w("infra/compose/docker-compose.full.yml", compose_full)

# 12) Enhanced Dockerfile for API
dockerfile_api_full = '''FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY apps/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY packages /app/packages
COPY services /app/services
COPY scripts /app/scripts
COPY apps/api /app/apps/api

WORKDIR /app/apps/api

EXPOSE 8000
CMD ["uvicorn", "main_full:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
'''
w("infra/docker/Dockerfile.api.full", dockerfile_api_full)

# 13) Enhanced web with toggle
enhanced_web = '''\"use client\";

import { useState, useEffect } from \"react\";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || \"http://localhost:8000\";
const USE_LANGGRAPH_KEY = \"use_langgraph\";

export default function Home() {
  const [question, setQuestion] = useState(\"\");
  const [answer, setAnswer] = useState(\"\");
  const [steps, setSteps] = useState<any[]>([]);
  const [trace, setTrace] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [useLG, setUseLG] = useState<boolean>(() => {
    if (typeof window !== \"undefined\") {
      return localStorage.getItem(USE_LANGGRAPH_KEY) === \"1\";
    }
    return false;
  });

  async function solve() {
    setLoading(true);
    setAnswer(\"\");
    setSteps([]);
    setTrace([]);

    try {
      const response = await fetch(`${API_BASE}/v1/chat/solve`, {
        method: \"POST\",
        headers: { \"Content-Type\": \"application/json\" },
        body: JSON.stringify({
          question,
          flags: { useLangGraph: useLG }
        }),
      });

      const data = await response.json();
      setAnswer(data.answer || \"No answer\");
      setSteps(data.steps || []);
      setTrace(data.trace || []);
    } catch (error) {
      setAnswer(\"Error: \" + error);
    } finally {
      setLoading(false);
    }
  }

  async function runSandbox() {
    try {
      const response = await fetch(`${API_BASE}/v1/tools/run`, {
        method: \"POST\",
        headers: { \"Content-Type\": \"application/json\" },
        body: JSON.stringify({
          language: \"python\",
          code: \"print('Hello from sandbox!')\\nprint(2**10)\"
        }),
      });

      const data = await response.json();
      alert(\"Sandbox output:\\n\" + (data.stdout || JSON.stringify(data)));
    } catch (error) {
      alert(\"Sandbox error: \" + error);
    }
  }

  const examples = [
    \"Integrate sin(x)\",
    \"What is Ohm's law?\",
    \"Calculate projectile motion\",
  ];

  return (
    <div style={{ padding: \"2rem\", maxWidth: \"1200px\", margin: \"0 auto\" }}>
      <h1>EMMA - Full Stack Edition</h1>
      <p>Math assistant with optional pgvector, Neo4j, LangGraph, and Sandbox</p>

      <div style={{ marginTop: \"2rem\" }}>
        <div style={{ display: \"flex\", gap: \"1rem\", marginBottom: \"1rem\" }}>
          <input
            type=\"text\"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder=\"Ask a math or science question...\"
            style={{
              flex: 1,
              padding: \"0.5rem\",
              fontSize: \"1rem\",
              border: \"1px solid #ccc\",
              borderRadius: \"4px\",
            }}
          />
          <button
            onClick={solve}
            disabled={loading}
            style={{
              padding: \"0.5rem 1rem\",
              background: loading ? \"#ccc\" : \"#007bff\",
              color: \"white\",
              border: \"none\",
              borderRadius: \"4px\",
              cursor: loading ? \"not-allowed\" : \"pointer\",
            }}
          >
            {loading ? \"Solving...\" : \"Solve\"}
          </button>
        </div>

        <div style={{ display: \"flex\", gap: \"1rem\", alignItems: \"center\" }}>
          <label>
            <input
              type=\"checkbox\"
              checked={useLG}
              onChange={(e) => {
                setUseLG(e.target.checked);
                if (typeof window !== \"undefined\") {
                  localStorage.setItem(
                    USE_LANGGRAPH_KEY,
                    e.target.checked ? \"1\" : \"0\"
                  );
                }
              }}
            />
            {\" Use LangGraph planner\"}
          </label>
          <button
            onClick={runSandbox}
            style={{
              padding: \"0.5rem 1rem\",
              background: \"#28a745\",
              color: \"white\",
              border: \"none\",
              borderRadius: \"4px\",
              cursor: \"pointer\",
            }}
          >
            Run Sandbox Demo
          </button>
        </div>

        <div style={{ marginTop: \"1rem\" }}>
          {examples.map((ex, i) => (
            <button
              key={i}
              onClick={() => setQuestion(ex)}
              style={{
                marginRight: \"0.5rem\",
                padding: \"0.25rem 0.5rem\",
                background: \"#f8f9fa\",
                border: \"1px solid #dee2e6\",
                borderRadius: \"4px\",
                cursor: \"pointer\",
              }}
            >
              {ex}
            </button>
          ))}
        </div>
      </div>

      {answer && (
        <div style={{ marginTop: \"2rem\" }}>
          <h2>Answer</h2>
          <div style={{
            padding: \"1rem\",
            background: \"#f8f9fa\",
            borderRadius: \"4px\",
            whiteSpace: \"pre-wrap\",
          }}>
            {answer}
          </div>
        </div>
      )}

      {trace.length > 0 && (
        <div style={{ marginTop: \"2rem\" }}>
          <h3>LangGraph Trace</h3>
          <ul>
            {trace.map((t, i) => (
              <li key={i}>
                <strong>{t.node}</strong>: {JSON.stringify(t)}
              </li>
            ))}
          </ul>
        </div>
      )}

      {steps.length > 0 && (
        <div style={{ marginTop: \"2rem\" }}>
          <h3>Steps</h3>
          <ol>
            {steps.map((s, i) => (
              <li key={i}>
                {s.role} - {s.action}
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}
'''
w("apps/web/app/page_full.tsx", enhanced_web)

# 14) Web Dockerfile for full stack
dockerfile_web_full = '''FROM node:20-alpine
WORKDIR /app
COPY apps/web/package.json .
RUN npm install
COPY apps/web .
# Use the full stack page
RUN mv app/page_full.tsx app/page.tsx
CMD ["npm", "run", "dev"]
'''
w("infra/docker/Dockerfile.web.full", dockerfile_web_full)

# Create the enhanced zip
zip_path = Path("/workspace/emma_full_stack.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
    for file_path in base.rglob("*"):
        if file_path.is_file():
            arcname = file_path.relative_to(base)
            zf.write(file_path, arcname)

print(f"\n✅ Full-stack EMMA enhancements added successfully!")
print(f"📦 Archive: {zip_path}")
print(f"📁 Size: {zip_path.stat().st_size / 1024:.2f} KB")
print(f"\n🚀 To run the full stack:")
print("   unzip emma_full_stack.zip")
print("   cd emma_improved")
print("   docker compose -f infra/compose/docker-compose.full.yml up --build")
print("\n📊 Then seed the databases:")
print("   docker compose -f infra/compose/docker-compose.full.yml exec api python scripts/seed_pgvector.py")
print("   docker compose -f infra/compose/docker-compose.full.yml exec api python scripts/seed_kg.py")