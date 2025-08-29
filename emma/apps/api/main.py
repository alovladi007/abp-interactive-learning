"""EMMA API - FastAPI gateway with LangGraph orchestration."""

import os
from contextlib import asynccontextmanager
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from emma_core import ProblemInput, FinalAnswer, RunTrace, get_logger
from .orchestrator import EMMAOrchestrator
from .auth import get_current_user, User
from .database import get_db, init_db
from .tracing import setup_tracing
from .rate_limit import RateLimiter

logger = get_logger(__name__)

# Initialize components
orchestrator = EMMAOrchestrator()
rate_limiter = RateLimiter()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    # Startup
    logger.info("Starting EMMA API...")
    await init_db()
    setup_tracing()
    await orchestrator.initialize()
    yield
    # Shutdown
    logger.info("Shutting down EMMA API...")
    await orchestrator.cleanup()


app = FastAPI(
    title="EMMA API",
    description="Expert Multimodal & Math Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SolveRequest(BaseModel):
    """Request schema for solving a problem."""
    
    question: str
    media: Optional[List[Dict[str, Any]]] = None
    goals: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    preferred_units: Optional[str] = "SI"
    domain_hints: Optional[List[str]] = None
    need_steps: bool = True
    need_citations: bool = True


class SolveResponse(BaseModel):
    """Response schema for solve endpoint."""
    
    run_id: str
    status: str
    answer: Optional[FinalAnswer] = None
    trace_url: Optional[str] = None


@app.post("/v1/chat/solve", response_model=SolveResponse)
async def solve_problem(
    request: SolveRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    _: None = Depends(rate_limiter.check),
) -> SolveResponse:
    """Main entry point for solving problems."""
    try:
        # Create problem input
        problem = ProblemInput(
            user_id=current_user.id,
            question=request.question,
            media=request.media,
            goals=request.goals or [],
            constraints=request.constraints or [],
            preferred_units=request.preferred_units,
            domain_hints=request.domain_hints or [],
            need_steps=request.need_steps,
            need_citations=request.need_citations,
        )
        
        # Start orchestration
        run_id = await orchestrator.start_solve(problem, background_tasks)
        
        return SolveResponse(
            run_id=str(run_id),
            status="processing",
            trace_url=f"/v1/trace/{run_id}",
        )
    except Exception as e:
        logger.error(f"Error solving problem: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/ingest/docs")
async def ingest_documents(
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Upload and ingest documents for RAG."""
    try:
        source_ids = []
        for file in files:
            # Validate file type
            if not any(file.filename.endswith(ext) for ext in [".pdf", ".txt", ".md", ".html"]):
                raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")
            
            # Process file
            content = await file.read()
            source_id = await orchestrator.ingest_document(
                filename=file.filename,
                content=content,
                user_id=current_user.id,
            )
            source_ids.append(source_id)
        
        return {"source_ids": source_ids, "count": len(source_ids)}
    except Exception as e:
        logger.error(f"Error ingesting documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/trace/{run_id}")
async def get_trace(
    run_id: str,
    current_user: User = Depends(get_current_user),
) -> RunTrace:
    """Get step-by-step trace of a run."""
    try:
        trace = await orchestrator.get_trace(run_id, current_user.id)
        if not trace:
            raise HTTPException(status_code=404, detail="Run not found")
        return trace
    except Exception as e:
        logger.error(f"Error getting trace: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/citations/{run_id}")
async def get_citations(
    run_id: str,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Get normalized citations for a run."""
    try:
        citations = await orchestrator.get_citations(run_id, current_user.id)
        return {"run_id": run_id, "citations": citations}
    except Exception as e:
        logger.error(f"Error getting citations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/tools/run")
async def run_tool(
    tool_name: str,
    args: Dict[str, Any],
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """Admin endpoint to invoke a tool directly."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        result = await orchestrator.run_tool(tool_name, args)
        return {"tool": tool_name, "result": result}
    except Exception as e:
        logger.error(f"Error running tool {tool_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    health = await orchestrator.get_health()
    return {
        "status": "healthy" if health["all_healthy"] else "degraded",
        "services": health,
    }


@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "name": "EMMA API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=os.getenv("API_RELOAD", "true").lower() == "true",
        workers=int(os.getenv("API_WORKERS", "4")),
    )