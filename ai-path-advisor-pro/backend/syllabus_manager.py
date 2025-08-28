"""
Syllabus Management System
Handles upload, storage, tracking, and retrieval of course syllabi
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional, List, Dict
import os
import json
import shutil
from datetime import datetime
import hashlib
import mimetypes
from pathlib import Path

router = APIRouter(prefix="/syllabus", tags=["syllabus"])

# Configuration
SYLLABUS_STORAGE_DIR = "syllabus_storage"
SYLLABUS_DB_FILE = "syllabus_database.json"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.html', '.txt'}

# Ensure storage directory exists
os.makedirs(SYLLABUS_STORAGE_DIR, exist_ok=True)

class SyllabusMetadata(BaseModel):
    course_id: str
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    upload_date: str
    uploaded_by: Optional[str] = "instructor"
    version: int = 1
    status: str = "active"  # active, archived, pending
    checksum: str
    description: Optional[str] = None

class SyllabusDatabase:
    """Simple JSON-based database for syllabus tracking"""
    
    def __init__(self, db_file: str = SYLLABUS_DB_FILE):
        self.db_file = db_file
        self.load_database()
    
    def load_database(self):
        """Load database from JSON file"""
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {"syllabi": {}, "upload_history": []}
            self.save_database()
    
    def save_database(self):
        """Save database to JSON file"""
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_syllabus(self, metadata: SyllabusMetadata):
        """Add or update syllabus metadata"""
        course_id = metadata.course_id
        
        # Archive previous version if exists
        if course_id in self.data["syllabi"]:
            old_metadata = self.data["syllabi"][course_id]
            old_metadata["status"] = "archived"
            old_metadata["archived_date"] = datetime.now().isoformat()
            self.data["upload_history"].append(old_metadata)
        
        # Add new syllabus
        self.data["syllabi"][course_id] = metadata.dict()
        self.save_database()
    
    def get_syllabus(self, course_id: str) -> Optional[Dict]:
        """Get syllabus metadata for a course"""
        return self.data["syllabi"].get(course_id)
    
    def list_syllabi(self) -> List[Dict]:
        """List all active syllabi"""
        return list(self.data["syllabi"].values())
    
    def has_syllabus(self, course_id: str) -> bool:
        """Check if course has a syllabus"""
        return course_id in self.data["syllabi"]
    
    def delete_syllabus(self, course_id: str) -> bool:
        """Delete syllabus metadata"""
        if course_id in self.data["syllabi"]:
            # Archive instead of delete
            metadata = self.data["syllabi"][course_id]
            metadata["status"] = "deleted"
            metadata["deleted_date"] = datetime.now().isoformat()
            self.data["upload_history"].append(metadata)
            del self.data["syllabi"][course_id]
            self.save_database()
            return True
        return False

# Initialize database
db = SyllabusDatabase()

def calculate_checksum(file_content: bytes) -> str:
    """Calculate SHA256 checksum of file content"""
    return hashlib.sha256(file_content).hexdigest()

def generate_safe_filename(course_id: str, original_filename: str) -> str:
    """Generate safe filename for storage"""
    extension = Path(original_filename).suffix.lower()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = f"{course_id}_{timestamp}{extension}"
    return safe_name

@router.post("/upload/{course_id}")
async def upload_syllabus(
    course_id: str,
    file: UploadFile = File(...),
    description: Optional[str] = None
):
    """
    Upload a syllabus file for a specific course
    """
    try:
        # Validate file extension
        file_extension = Path(file.filename).suffix.lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        content = await file.read()
        
        # Validate file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / 1024 / 1024}MB"
            )
        
        # Generate safe filename and save file
        safe_filename = generate_safe_filename(course_id, file.filename)
        file_path = os.path.join(SYLLABUS_STORAGE_DIR, safe_filename)
        
        with open(file_path, 'wb') as f:
            f.write(content)
        
        # Create metadata
        metadata = SyllabusMetadata(
            course_id=course_id,
            filename=safe_filename,
            original_filename=file.filename,
            file_type=file_extension,
            file_size=len(content),
            upload_date=datetime.now().isoformat(),
            checksum=calculate_checksum(content),
            description=description
        )
        
        # Update database
        db.add_syllabus(metadata)
        
        return {
            "success": True,
            "message": f"Syllabus uploaded successfully for {course_id}",
            "metadata": metadata.dict()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download/{course_id}")
async def download_syllabus(course_id: str):
    """
    Download the syllabus file for a specific course
    """
    metadata = db.get_syllabus(course_id)
    
    if not metadata:
        raise HTTPException(
            status_code=404,
            detail=f"No syllabus found for course {course_id}"
        )
    
    file_path = os.path.join(SYLLABUS_STORAGE_DIR, metadata["filename"])
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Syllabus file not found in storage"
        )
    
    # Determine media type
    media_type = mimetypes.guess_type(metadata["original_filename"])[0] or "application/octet-stream"
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=metadata["original_filename"],
        headers={
            "Content-Disposition": f"attachment; filename={metadata['original_filename']}"
        }
    )

@router.get("/view/{course_id}")
async def view_syllabus(course_id: str):
    """
    View the syllabus in browser (for PDF and HTML files)
    """
    metadata = db.get_syllabus(course_id)
    
    if not metadata:
        raise HTTPException(
            status_code=404,
            detail=f"No syllabus found for course {course_id}"
        )
    
    file_path = os.path.join(SYLLABUS_STORAGE_DIR, metadata["filename"])
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Syllabus file not found in storage"
        )
    
    # For HTML files, return as HTML response
    if metadata["file_type"] == ".html":
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    
    # For other files, return as inline display
    media_type = mimetypes.guess_type(metadata["original_filename"])[0] or "application/octet-stream"
    
    return FileResponse(
        path=file_path,
        media_type=media_type,
        filename=metadata["original_filename"],
        headers={
            "Content-Disposition": f"inline; filename={metadata['original_filename']}"
        }
    )

@router.get("/metadata/{course_id}")
async def get_syllabus_metadata(course_id: str):
    """
    Get metadata about the syllabus for a course
    """
    metadata = db.get_syllabus(course_id)
    
    if not metadata:
        return {
            "exists": False,
            "course_id": course_id,
            "message": "No syllabus uploaded for this course"
        }
    
    return {
        "exists": True,
        "metadata": metadata
    }

@router.get("/check/{course_id}")
async def check_syllabus_exists(course_id: str):
    """
    Quick check if a syllabus exists for a course
    """
    exists = db.has_syllabus(course_id)
    return {"course_id": course_id, "has_syllabus": exists}

@router.get("/list")
async def list_all_syllabi():
    """
    List all courses with uploaded syllabi
    """
    syllabi = db.list_syllabi()
    return {
        "total": len(syllabi),
        "syllabi": syllabi
    }

@router.delete("/delete/{course_id}")
async def delete_syllabus(course_id: str):
    """
    Delete (archive) a syllabus for a course
    """
    metadata = db.get_syllabus(course_id)
    
    if not metadata:
        raise HTTPException(
            status_code=404,
            detail=f"No syllabus found for course {course_id}"
        )
    
    # Archive the file (don't actually delete)
    old_path = os.path.join(SYLLABUS_STORAGE_DIR, metadata["filename"])
    archive_dir = os.path.join(SYLLABUS_STORAGE_DIR, "archive")
    os.makedirs(archive_dir, exist_ok=True)
    
    if os.path.exists(old_path):
        archive_path = os.path.join(archive_dir, metadata["filename"])
        shutil.move(old_path, archive_path)
    
    # Update database
    db.delete_syllabus(course_id)
    
    return {
        "success": True,
        "message": f"Syllabus for {course_id} has been archived"
    }

@router.get("/history/{course_id}")
async def get_upload_history(course_id: str):
    """
    Get upload history for a specific course
    """
    history = [
        h for h in db.data["upload_history"] 
        if h["course_id"] == course_id
    ]
    
    return {
        "course_id": course_id,
        "history": history,
        "total_versions": len(history)
    }

@router.get("/stats")
async def get_syllabus_stats():
    """
    Get statistics about syllabus uploads
    """
    syllabi = db.list_syllabi()
    
    stats = {
        "total_syllabi": len(syllabi),
        "total_size": sum(s["file_size"] for s in syllabi),
        "file_types": {},
        "recent_uploads": [],
        "courses_with_syllabi": [s["course_id"] for s in syllabi]
    }
    
    # Count file types
    for s in syllabi:
        file_type = s["file_type"]
        stats["file_types"][file_type] = stats["file_types"].get(file_type, 0) + 1
    
    # Get recent uploads (last 5)
    sorted_syllabi = sorted(syllabi, key=lambda x: x["upload_date"], reverse=True)
    stats["recent_uploads"] = sorted_syllabi[:5]
    
    return stats