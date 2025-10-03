from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import logging
import pathlib
import uuid
from datetime import datetime

from config.settings import settings
from services.voice import voice_service, VoiceConfig
from services.music import music_service, MusicConfig
from services.post_processing import post_processing_service, PostProcessConfig
from services.quality_control import qc_service
from services.cdn import storage_service
from services.stripe_service import payment_service

# Import MARIA routes
from api.maria_routes import router as maria_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include MARIA router
app.include_router(maria_router, prefix="/api/maria", tags=["MARIA Medical AI"])

# Request/Response Models
class GenerateVoiceRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None
    provider: str = "elevenlabs"
    emotion: Optional[str] = None
    tempo: float = 1.0

class GenerateMusicRequest(BaseModel):
    prompt: str
    duration: int = 60
    genre: Optional[str] = None
    mood: Optional[str] = None
    tempo: Optional[int] = 90
    provider: str = "suno"

class ProcessVideoRequest(BaseModel):
    video_key: str
    interpolation_factor: int = 2
    upscale_factor: int = 2
    target_fps: int = 60
    normalize_audio: bool = True

class QualityCheckRequest(BaseModel):
    video_key: str
    prompt: Optional[str] = None

class CreateCheckoutRequest(BaseModel):
    package_key: str
    success_url: str
    cancel_url: str

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.APP_VERSION
    }

# Voice Generation Endpoints
@app.post("/api/v1/generate/voice")
async def generate_voice(
    request: GenerateVoiceRequest,
    background_tasks: BackgroundTasks
):
    """Generate voice-over from text"""
    try:
        # Check prompt compliance
        passed, issues = await qc_service.check_prompt_compliance(request.text)
        if not passed:
            raise HTTPException(400, detail={"error": "Content policy violation", "issues": issues})
        
        # Generate voice
        config = VoiceConfig(
            text=request.text,
            voice_id=request.voice_id,
            provider=request.provider,
            emotion=request.emotion,
            tempo=request.tempo
        )
        
        audio_data = await voice_service.generate_voice(config)
        
        # Upload to CDN
        filename = f"voice_{uuid.uuid4().hex}.mp3"
        result = await storage_service.upload_audio(audio_data, filename)
        
        return {
            "success": True,
            "url": result["url"],
            "key": result["key"],
            "duration": len(audio_data) / (44100 * 2),  # Approximate duration
            "size": result["size"]
        }
        
    except Exception as e:
        logger.error(f"Voice generation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.get("/api/v1/voice/options")
async def get_voice_options(provider: str = "elevenlabs"):
    """Get available voice options"""
    return voice_service.get_voice_options(provider)

# Music Generation Endpoints
@app.post("/api/v1/generate/music")
async def generate_music(request: GenerateMusicRequest):
    """Generate music from prompt"""
    try:
        # Check prompt compliance
        passed, issues = await qc_service.check_prompt_compliance(request.prompt)
        if not passed:
            raise HTTPException(400, detail={"error": "Content policy violation", "issues": issues})
        
        # Generate music
        config = MusicConfig(
            prompt=request.prompt,
            duration=request.duration,
            genre=request.genre,
            mood=request.mood,
            tempo=request.tempo,
            provider=request.provider
        )
        
        result = await music_service.generate_music(config)
        
        return {
            "success": True,
            "url": result["url"],
            "id": result["id"],
            "duration": result["duration"],
            "provider": result["provider"]
        }
        
    except Exception as e:
        logger.error(f"Music generation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.get("/api/v1/music/presets")
async def get_music_presets():
    """Get available music presets"""
    return music_service.get_music_presets()

# Video Processing Endpoints
@app.post("/api/v1/process/video")
async def process_video(
    request: ProcessVideoRequest,
    background_tasks: BackgroundTasks
):
    """Post-process video with enhancement"""
    try:
        # Download video from CDN
        temp_dir = pathlib.Path("/tmp") / f"process_{uuid.uuid4().hex}"
        temp_dir.mkdir(exist_ok=True)
        
        video_path = await storage_service.download_file(
            request.video_key,
            temp_dir / "input.mp4"
        )
        
        # Process video
        config = PostProcessConfig(
            interpolation_factor=request.interpolation_factor,
            upscale_factor=request.upscale_factor,
            target_fps=request.target_fps,
            normalize_audio=request.normalize_audio
        )
        
        output_path = await post_processing_service.process_video(video_path, config)
        
        # Upload processed video
        result = await storage_service.upload_video(output_path, folder="processed")
        
        # Cleanup
        background_tasks.add_task(cleanup_temp_dir, temp_dir)
        
        return {
            "success": True,
            "url": result["url"],
            "key": result["key"],
            "size": result["size"],
            "processing_config": config.dict()
        }
        
    except Exception as e:
        logger.error(f"Video processing error: {e}")
        raise HTTPException(500, detail=str(e))

@app.get("/api/v1/video/info/{video_key:path}")
async def get_video_info(video_key: str):
    """Get video information"""
    try:
        info = await storage_service.get_file_info(video_key)
        if not info:
            raise HTTPException(404, detail="Video not found")
        
        return info
        
    except Exception as e:
        logger.error(f"Get video info error: {e}")
        raise HTTPException(500, detail=str(e))

# Quality Control Endpoints
@app.post("/api/v1/qc/check")
async def quality_check(request: QualityCheckRequest):
    """Perform quality control check on video"""
    try:
        # Download video
        temp_path = pathlib.Path("/tmp") / f"qc_{uuid.uuid4().hex}.mp4"
        video_path = await storage_service.download_file(request.video_key, temp_path)
        
        # Perform QC
        result = await qc_service.check_video(
            video_path,
            prompt=request.prompt
        )
        
        # Generate report
        report = await qc_service.generate_qc_report(result)
        
        # Cleanup
        temp_path.unlink(missing_ok=True)
        
        return {
            "success": True,
            "passed": result.passed,
            "compliance_score": result.compliance_score,
            "report": report
        }
        
    except Exception as e:
        logger.error(f"Quality check error: {e}")
        raise HTTPException(500, detail=str(e))

# Payment Endpoints
@app.post("/api/v1/payment/checkout")
async def create_checkout(
    request: CreateCheckoutRequest,
    user_id: str = "demo_user"  # In production, get from auth
):
    """Create Stripe checkout session"""
    try:
        result = await payment_service.create_checkout_session(
            user_id=user_id,
            package_key=request.package_key,
            success_url=request.success_url,
            cancel_url=request.cancel_url
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Checkout creation error: {e}")
        raise HTTPException(500, detail=str(e))

@app.post("/api/v1/payment/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    try:
        payload = await request.body()
        signature = request.headers.get("stripe-signature")
        
        result = await payment_service.handle_webhook(payload, signature)
        
        # Process the webhook result (update user credits, etc.)
        # This would typically update your database
        
        return {"received": True}
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        raise HTTPException(400, detail=str(e))

@app.get("/api/v1/payment/packages")
async def get_credit_packages():
    """Get available credit packages"""
    return payment_service.get_credit_packages()

# Storage/CDN Endpoints
@app.post("/api/v1/storage/upload")
async def upload_file(
    file: UploadFile = File(...),
    folder: str = "uploads"
):
    """Upload file to CDN"""
    try:
        # Save uploaded file temporarily
        temp_path = pathlib.Path("/tmp") / f"upload_{uuid.uuid4().hex}_{file.filename}"
        
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Upload to CDN
        key = f"{folder}/{datetime.utcnow().strftime('%Y%m%d')}/{file.filename}"
        result = await storage_service.upload_file(
            temp_path,
            key,
            content_type=file.content_type
        )
        
        # Cleanup
        temp_path.unlink(missing_ok=True)
        
        return result
        
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(500, detail=str(e))

@app.get("/api/v1/storage/list")
async def list_files(prefix: str = "", limit: int = 100):
    """List files in storage"""
    try:
        files = await storage_service.list_files(prefix, limit)
        return {"files": files, "count": len(files)}
        
    except Exception as e:
        logger.error(f"List files error: {e}")
        raise HTTPException(500, detail=str(e))

@app.get("/api/v1/storage/stats")
async def get_storage_stats(prefix: str = ""):
    """Get storage statistics"""
    try:
        stats = await storage_service.get_storage_stats(prefix)
        return stats
        
    except Exception as e:
        logger.error(f"Storage stats error: {e}")
        raise HTTPException(500, detail=str(e))

# Utility functions
async def cleanup_temp_dir(temp_dir: pathlib.Path):
    """Clean up temporary directory"""
    try:
        import shutil
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
    except Exception as e:
        logger.error(f"Cleanup error: {e}")

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        workers=settings.WORKERS
    )