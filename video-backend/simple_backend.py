#!/usr/bin/env python3
"""
Simple Video Upload Backend
A minimal working backend for video uploads
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
import cgi
import uuid
from datetime import datetime
import urllib.parse

# Configuration
VIDEO_STORAGE_DIR = "video_storage"
DATABASE_FILE = "video_database.json"
PORT = 8001

# Ensure directories exist
os.makedirs(f"{VIDEO_STORAGE_DIR}/uploads", exist_ok=True)
os.makedirs(f"{VIDEO_STORAGE_DIR}/processed", exist_ok=True)
os.makedirs(f"{VIDEO_STORAGE_DIR}/archived", exist_ok=True)

class VideoUploadHandler(SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        
        if parsed_path.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "name": "E.U.R.E.K.A Video Backend (Simple)",
                "version": "1.0.0",
                "status": "running",
                "endpoints": {
                    "upload": "/api/videos/upload",
                    "list": "/api/videos/list",
                    "statistics": "/api/statistics"
                }
            }
            self.wfile.write(json.dumps(response).encode())
            
        elif parsed_path.path == '/api/videos/list':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            videos = self.load_videos()
            self.wfile.write(json.dumps({"videos": videos, "total": len(videos)}).encode())
            
        elif parsed_path.path == '/api/statistics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            stats = self.get_statistics()
            self.wfile.write(json.dumps(stats).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        # Enable CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        
        if self.path == '/api/videos/upload':
            try:
                # Parse multipart form data
                content_type = self.headers.get('Content-Type')
                if not content_type or 'multipart/form-data' not in content_type:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Invalid content type"}).encode())
                    return
                
                # Parse the form
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                
                # Extract video file
                video_file = form['file'] if 'file' in form else None
                if not video_file or not video_file.filename:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "No file provided"}).encode())
                    return
                
                # Generate unique ID
                video_id = str(uuid.uuid4())
                
                # Save file
                filename = f"{video_id}_{video_file.filename}"
                filepath = os.path.join(VIDEO_STORAGE_DIR, "uploads", filename)
                
                with open(filepath, 'wb') as f:
                    f.write(video_file.file.read())
                
                # Extract metadata
                metadata = {
                    "id": video_id,
                    "title": form.getvalue('title', 'Untitled'),
                    "description": form.getvalue('description', ''),
                    "category": form.getvalue('category', 'general'),
                    "subcategory": form.getvalue('subcategory', 'general'),
                    "instructor": form.getvalue('instructor', 'Unknown'),
                    "level": form.getvalue('level', 'Beginner'),
                    "tags": form.getvalue('tags', '').split(','),
                    "topics": form.getvalue('topics', '').split(','),
                    "prerequisites": form.getvalue('prerequisites', '').split(','),
                    "is_premium": form.getvalue('is_premium', 'false') == 'true',
                    "upload_date": datetime.now().isoformat(),
                    "file_path": filepath,
                    "filename": filename,
                    "original_filename": video_file.filename,
                    "status": "active",
                    "views": 0
                }
                
                # Save to database
                self.save_video(metadata)
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {
                    "success": True,
                    "message": "Video uploaded successfully",
                    "video_id": video_id,
                    "metadata": metadata
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def load_database(self):
        """Load the video database"""
        if os.path.exists(DATABASE_FILE):
            with open(DATABASE_FILE, 'r') as f:
                return json.load(f)
        else:
            return {"videos": {}, "statistics": {}}
    
    def save_database(self, data):
        """Save the video database"""
        with open(DATABASE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_videos(self):
        """Load all videos"""
        db = self.load_database()
        return list(db.get("videos", {}).values())
    
    def save_video(self, metadata):
        """Save video metadata"""
        db = self.load_database()
        if "videos" not in db:
            db["videos"] = {}
        db["videos"][metadata["id"]] = metadata
        self.save_database(db)
    
    def get_statistics(self):
        """Get platform statistics"""
        db = self.load_database()
        videos = db.get("videos", {}).values()
        
        total_size = 0
        for video in videos:
            if os.path.exists(video.get("file_path", "")):
                total_size += os.path.getsize(video["file_path"])
        
        categories = set(v.get("category", "") for v in videos)
        
        return {
            "total_videos": len(videos),
            "total_views": sum(v.get("views", 0) for v in videos),
            "total_size": total_size,
            "categories_count": len(categories),
            "categories": list(categories)
        }

def run_server():
    """Run the simple HTTP server"""
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, VideoUploadHandler)
    
    print(f"""
    ========================================
    E.U.R.E.K.A Video Backend (Simple)
    ========================================
    
    Server running at: http://localhost:{PORT}
    
    Endpoints:
    - GET  /                     - Server info
    - POST /api/videos/upload    - Upload video
    - GET  /api/videos/list      - List videos
    - GET  /api/statistics       - Get stats
    
    Press Ctrl+C to stop
    ========================================
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    run_server()