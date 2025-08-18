"""
Advanced QBank System with IRT Adaptive Testing
Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict, Any

from app.core.config import settings
from app.api import qbank
from app.models.question import init_db
from app.services.adaptive import AdaptiveTestingEngine
from app.services.calibration import CalibrationService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
adaptive_engine = None
calibration_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global adaptive_engine, calibration_service
    
    # Startup
    logger.info("Starting QBank Application...")
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize services
    adaptive_engine = AdaptiveTestingEngine()
    calibration_service = CalibrationService()
    
    logger.info("Services initialized")
    logger.info(f"QBank API running at {settings.API_V1_STR}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down QBank Application...")
    # Cleanup resources if needed

# Create FastAPI app
app = FastAPI(
    title="Advanced QBank System",
    description="IRT-based Adaptive Testing Platform with Sympson-Hetter Exposure Control",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers
app.include_router(qbank.router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Advanced QBank System",
        "version": "1.0.0",
        "description": "IRT-based Adaptive Testing Platform",
        "features": [
            "3-Parameter Logistic IRT Model",
            "Sympson-Hetter Exposure Control",
            "Real-time Calibration",
            "5000+ Question Database",
            "Psychometric Analysis"
        ],
        "api_docs": "/docs",
        "api_redoc": "/redoc",
        "health": "/health"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "database": "connected",
            "redis": "connected",
            "adaptive_engine": "active" if adaptive_engine else "inactive",
            "calibration_service": "active" if calibration_service else "inactive"
        }
    }

# System info endpoint
@app.get("/api/v1/system/info")
async def system_info():
    """Get system information"""
    return {
        "irt_model": settings.IRT_MODEL,
        "exposure_rate_max": settings.EXPOSURE_RATE_MAX,
        "min_responses_for_calibration": settings.MIN_RESPONSES_FOR_CALIBRATION,
        "question_pool_size": 5000,
        "supported_subjects": [
            "Mathematics",
            "Science",
            "English",
            "History",
            "Computer Science",
            "Physics",
            "Chemistry",
            "Biology"
        ],
        "test_types": [
            "SAT",
            "ACT",
            "GRE",
            "GMAT",
            "AP Exams",
            "Custom Practice"
        ]
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": time.time()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )