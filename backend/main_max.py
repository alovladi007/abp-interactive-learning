"""
MAX AI Research Assistant - Complete FastAPI Application
Integrates all MAX services and routes
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from datetime import datetime

# Import MAX routes
from api.max_routes_complete import router as max_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 MAX AI Research Assistant starting up...")
    logger.info("📚 Loading MAX services...")

    # Initialize services here if needed
    # await max_service.initialize()

    logger.info("✅ MAX is ready!")

    yield

    # Shutdown
    logger.info("👋 MAX shutting down...")
    # Cleanup here if needed

# Create FastAPI application
app = FastAPI(
    title="MAX - AI Research Assistant",
    description="Multi-source academic paper search, citation network analysis, and research synthesis",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "*"  # For development - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include MAX router
app.include_router(max_router, prefix="/api/max", tags=["MAX Research"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "MAX - AI Research Assistant",
        "version": "1.0.0",
        "description": "Multi-source academic paper search and analysis",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/health",
            "max_search": "/api/max/search",
            "max_network": "/api/max/citations/network",
            "max_synthesis": "/api/max/synthesize"
        },
        "status": "operational",
        "timestamp": datetime.utcnow().isoformat()
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MAX AI Research Assistant",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "components": {
            "api": "operational",
            "database": "operational",  # Check actual DB in production
            "neo4j": "operational",      # Check actual Neo4j in production
            "semantic_scholar": "operational",
            "arxiv": "operational"
        }
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat(),
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

# Run application
if __name__ == "__main__":
    import uvicorn

    logger.info("Starting MAX AI Research Assistant...")

    uvicorn.run(
        "main_max:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )
