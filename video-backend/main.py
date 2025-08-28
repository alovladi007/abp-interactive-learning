"""
Video Management Backend System
Handles video uploads, storage, streaming, and metadata management
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import os
import json
import shutil
import hashlib
from datetime import datetime
import uuid
from pathlib import Path
import aiofiles
import mimetypes

app = FastAPI(title="E.U.R.E.K.A Video Management System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
VIDEO_STORAGE_DIR = "video_storage"
THUMBNAIL_DIR = "thumbnails"
DATABASE_FILE = "video_database.json"
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB
ALLOWED_VIDEO_FORMATS = {'.mp4', '.webm', '.ogg', '.mov', '.avi', '.mkv'}
CHUNK_SIZE = 1024 * 1024  # 1MB chunks for streaming

# Ensure directories exist
os.makedirs(VIDEO_STORAGE_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)
os.makedirs(f"{VIDEO_STORAGE_DIR}/uploads", exist_ok=True)
os.makedirs(f"{VIDEO_STORAGE_DIR}/processed", exist_ok=True)

# Pydantic Models
class VideoMetadata(BaseModel):
    id: str
    title: str
    description: str
    category: str
    subcategory: str
    instructor: str
    duration: Optional[str] = None
    level: str = "Beginner"  # Beginner, Intermediate, Advanced, Expert
    tags: List[str] = []
    topics: List[str] = []
    prerequisites: List[str] = []
    upload_date: str
    file_path: str
    file_size: int
    format: str
    thumbnail_path: Optional[str] = None
    views: int = 0
    rating: float = 0.0
    is_premium: bool = False
    status: str = "processing"  # processing, active, archived
    checksum: str

class VideoUploadRequest(BaseModel):
    title: str
    description: str
    category: str
    subcategory: str
    instructor: str
    level: str = "Beginner"
    tags: List[str] = []
    topics: List[str] = []
    prerequisites: List[str] = []
    is_premium: bool = False

class VideoUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    level: Optional[str] = None
    tags: Optional[List[str]] = None
    topics: Optional[List[str]] = None
    prerequisites: Optional[List[str]] = None
    is_premium: Optional[bool] = None

class VideoSearchParams(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    level: Optional[str] = None
    instructor: Optional[str] = None
    is_premium: Optional[bool] = None
    tags: Optional[List[str]] = None

# Database Class
class VideoDatabase:
    def __init__(self, db_file: str = DATABASE_FILE):
        self.db_file = db_file
        self.load_database()
    
    def load_database(self):
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {
                "videos": {},
                "categories": {},
                "upload_history": [],
                "statistics": {
                    "total_videos": 0,
                    "total_views": 0,
                    "total_size": 0,
                    "categories_count": 0
                }
            }
            self.save_database()
    
    def save_database(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_video(self, metadata: VideoMetadata):
        self.data["videos"][metadata.id] = metadata.dict()
        self.update_statistics()
        self.save_database()
    
    def get_video(self, video_id: str) -> Optional[Dict]:
        return self.data["videos"].get(video_id)
    
    def update_video(self, video_id: str, updates: Dict):
        if video_id in self.data["videos"]:
            self.data["videos"][video_id].update(updates)
            self.save_database()
            return True
        return False
    
    def delete_video(self, video_id: str) -> bool:
        if video_id in self.data["videos"]:
            video = self.data["videos"][video_id]
            video["status"] = "archived"
            video["archived_date"] = datetime.now().isoformat()
            self.data["upload_history"].append(video)
            del self.data["videos"][video_id]
            self.update_statistics()
            self.save_database()
            return True
        return False
    
    def list_videos(self, filters: Optional[VideoSearchParams] = None) -> List[Dict]:
        videos = list(self.data["videos"].values())
        
        if filters:
            if filters.category:
                videos = [v for v in videos if v["category"] == filters.category]
            if filters.subcategory:
                videos = [v for v in videos if v["subcategory"] == filters.subcategory]
            if filters.level:
                videos = [v for v in videos if v["level"] == filters.level]
            if filters.instructor:
                videos = [v for v in videos if v["instructor"] == filters.instructor]
            if filters.is_premium is not None:
                videos = [v for v in videos if v["is_premium"] == filters.is_premium]
            if filters.query:
                query = filters.query.lower()
                videos = [v for v in videos if 
                         query in v["title"].lower() or 
                         query in v["description"].lower() or
                         any(query in tag.lower() for tag in v.get("tags", []))]
        
        return videos
    
    def update_statistics(self):
        videos = self.data["videos"].values()
        self.data["statistics"]["total_videos"] = len(videos)
        self.data["statistics"]["total_size"] = sum(v["file_size"] for v in videos)
        self.data["statistics"]["total_views"] = sum(v.get("views", 0) for v in videos)
        
        categories = set()
        for v in videos:
            categories.add(v["category"])
        self.data["statistics"]["categories_count"] = len(categories)
    
    def increment_views(self, video_id: str):
        if video_id in self.data["videos"]:
            self.data["videos"][video_id]["views"] += 1
            self.save_database()

# Initialize database
db = VideoDatabase()

# Helper functions
def calculate_checksum(file_content: bytes) -> str:
    return hashlib.sha256(file_content).hexdigest()

def generate_video_id() -> str:
    return str(uuid.uuid4())

def get_file_extension(filename: str) -> str:
    return Path(filename).suffix.lower()

# API Endpoints

@app.get("/")
async def root():
    return {
        "name": "E.U.R.E.K.A Video Management System",
        "version": "1.0.0",
        "endpoints": {
            "upload": "/api/videos/upload",
            "list": "/api/videos/list",
            "stream": "/api/videos/stream/{video_id}",
            "metadata": "/api/videos/{video_id}",
            "search": "/api/videos/search",
            "categories": "/api/categories",
            "statistics": "/api/statistics"
        }
    }

@app.post("/api/videos/upload")
async def upload_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    subcategory: str = Form(...),
    instructor: str = Form(...),
    level: str = Form("Beginner"),
    tags: str = Form(""),  # Comma-separated
    topics: str = Form(""),  # Comma-separated
    prerequisites: str = Form(""),  # Comma-separated
    is_premium: bool = Form(False)
):
    """Upload a new video to the platform"""
    
    # Validate file extension
    file_ext = get_file_extension(file.filename)
    if file_ext not in ALLOWED_VIDEO_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid video format. Allowed: {', '.join(ALLOWED_VIDEO_FORMATS)}"
        )
    
    # Generate unique video ID
    video_id = generate_video_id()
    
    # Create file path
    safe_filename = f"{video_id}{file_ext}"
    file_path = os.path.join(VIDEO_STORAGE_DIR, "uploads", safe_filename)
    
    # Read and save file
    content = await file.read()
    
    # Check file size
    if len(content) > MAX_VIDEO_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {MAX_VIDEO_SIZE / 1024 / 1024}MB"
        )
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(content)
    
    # Parse comma-separated fields
    tags_list = [t.strip() for t in tags.split(',') if t.strip()] if tags else []
    topics_list = [t.strip() for t in topics.split(',') if t.strip()] if topics else []
    prerequisites_list = [p.strip() for p in prerequisites.split(',') if p.strip()] if prerequisites else []
    
    # Create metadata
    metadata = VideoMetadata(
        id=video_id,
        title=title,
        description=description,
        category=category,
        subcategory=subcategory,
        instructor=instructor,
        level=level,
        tags=tags_list,
        topics=topics_list,
        prerequisites=prerequisites_list,
        upload_date=datetime.now().isoformat(),
        file_path=file_path,
        file_size=len(content),
        format=file_ext,
        is_premium=is_premium,
        status="active",
        checksum=calculate_checksum(content)
    )
    
    # Add to database
    db.add_video(metadata)
    
    return {
        "success": True,
        "message": "Video uploaded successfully",
        "video_id": video_id,
        "metadata": metadata.dict()
    }

@app.get("/api/videos/list")
async def list_videos(
    category: Optional[str] = None,
    subcategory: Optional[str] = None,
    level: Optional[str] = None,
    instructor: Optional[str] = None,
    is_premium: Optional[bool] = None,
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0)
):
    """List all videos with optional filters"""
    
    filters = VideoSearchParams(
        category=category,
        subcategory=subcategory,
        level=level,
        instructor=instructor,
        is_premium=is_premium
    )
    
    videos = db.list_videos(filters)
    
    # Apply pagination
    total = len(videos)
    videos = videos[offset:offset + limit]
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "videos": videos
    }

@app.get("/api/videos/{video_id}")
async def get_video_metadata(video_id: str):
    """Get metadata for a specific video"""
    
    video = db.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Increment view count
    db.increment_views(video_id)
    
    return video

@app.get("/api/videos/stream/{video_id}")
async def stream_video(video_id: str):
    """Stream video content"""
    
    video = db.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    file_path = video["file_path"]
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Stream the video
    def iterfile():
        with open(file_path, 'rb') as f:
            while chunk := f.read(CHUNK_SIZE):
                yield chunk
    
    media_type = mimetypes.guess_type(file_path)[0] or "video/mp4"
    
    return StreamingResponse(
        iterfile(),
        media_type=media_type,
        headers={
            "Content-Length": str(file_size),
            "Accept-Ranges": "bytes",
        }
    )

@app.get("/api/videos/download/{video_id}")
async def download_video(video_id: str):
    """Download a video file"""
    
    video = db.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    file_path = video["file_path"]
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        path=file_path,
        media_type="video/mp4",
        filename=f"{video['title']}{video['format']}"
    )

@app.put("/api/videos/{video_id}")
async def update_video(video_id: str, updates: VideoUpdateRequest):
    """Update video metadata"""
    
    if not db.get_video(video_id):
        raise HTTPException(status_code=404, detail="Video not found")
    
    update_dict = {k: v for k, v in updates.dict().items() if v is not None}
    
    if db.update_video(video_id, update_dict):
        return {"success": True, "message": "Video updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update video")

@app.delete("/api/videos/{video_id}")
async def delete_video(video_id: str):
    """Archive/delete a video"""
    
    video = db.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    # Archive the file (don't actually delete)
    old_path = video["file_path"]
    if os.path.exists(old_path):
        archive_dir = os.path.join(VIDEO_STORAGE_DIR, "archived")
        os.makedirs(archive_dir, exist_ok=True)
        archive_path = os.path.join(archive_dir, os.path.basename(old_path))
        shutil.move(old_path, archive_path)
    
    if db.delete_video(video_id):
        return {"success": True, "message": "Video archived successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to delete video")

@app.post("/api/videos/search")
async def search_videos(params: VideoSearchParams):
    """Search videos with advanced filters"""
    
    videos = db.list_videos(params)
    
    return {
        "total": len(videos),
        "results": videos
    }

@app.get("/api/categories")
async def get_categories():
    """Get all available categories and subcategories"""
    
    categories = {}
    for video in db.data["videos"].values():
        cat = video["category"]
        subcat = video["subcategory"]
        
        if cat not in categories:
            categories[cat] = {"name": cat, "subcategories": set()}
        categories[cat]["subcategories"].add(subcat)
    
    # Convert sets to lists
    for cat in categories:
        categories[cat]["subcategories"] = list(categories[cat]["subcategories"])
    
    return categories

@app.get("/api/statistics")
async def get_statistics():
    """Get platform statistics"""
    
    db.update_statistics()
    stats = db.data["statistics"]
    
    # Add more detailed stats
    videos = db.data["videos"].values()
    
    stats["by_category"] = {}
    stats["by_level"] = {}
    stats["top_instructors"] = {}
    
    for video in videos:
        # By category
        cat = video["category"]
        if cat not in stats["by_category"]:
            stats["by_category"][cat] = {"count": 0, "views": 0}
        stats["by_category"][cat]["count"] += 1
        stats["by_category"][cat]["views"] += video.get("views", 0)
        
        # By level
        level = video["level"]
        if level not in stats["by_level"]:
            stats["by_level"][level] = 0
        stats["by_level"][level] += 1
        
        # By instructor
        instructor = video["instructor"]
        if instructor not in stats["top_instructors"]:
            stats["top_instructors"][instructor] = {"videos": 0, "views": 0}
        stats["top_instructors"][instructor]["videos"] += 1
        stats["top_instructors"][instructor]["views"] += video.get("views", 0)
    
    return stats

@app.get("/api/videos/placeholder/{category}/{subcategory}")
async def get_placeholder_videos(category: str, subcategory: str):
    """Get placeholder video data for a category/subcategory"""
    
    # Generate placeholder data
    placeholders = []
    for i in range(10):  # 10 placeholder videos per subcategory
        placeholders.append({
            "id": f"placeholder-{category}-{subcategory}-{i+1}",
            "title": f"{subcategory.replace('-', ' ').title()} - Lesson {i+1}",
            "description": f"This is a placeholder for {subcategory} content. Upload real video to replace.",
            "category": category,
            "subcategory": subcategory,
            "instructor": "Placeholder Instructor",
            "duration": f"{20 + i*5}:00",
            "level": ["Beginner", "Intermediate", "Advanced"][i % 3],
            "thumbnail": "/placeholder-thumbnail.jpg",
            "is_placeholder": True,
            "upload_prompt": "Click to upload real video content"
        })
    
    return {
        "category": category,
        "subcategory": subcategory,
        "placeholders": placeholders,
        "message": "These are placeholder videos. Upload real content to replace them."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)