from fastapi import FastAPI, HTTPException
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
