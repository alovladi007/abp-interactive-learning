#!/usr/bin/env node

/**
 * Simple Video Upload Server - Node.js Version
 * Works without complex dependencies
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { parse } = require('querystring');

const PORT = 8001;
const VIDEO_STORAGE_DIR = path.join(__dirname, 'video_storage');
const DATABASE_FILE = path.join(__dirname, 'video_database.json');

// Ensure directories exist
const dirs = [
    path.join(VIDEO_STORAGE_DIR, 'uploads'),
    path.join(VIDEO_STORAGE_DIR, 'processed'),
    path.join(VIDEO_STORAGE_DIR, 'archived')
];

dirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
});

// Initialize database
if (!fs.existsSync(DATABASE_FILE)) {
    fs.writeFileSync(DATABASE_FILE, JSON.stringify({ videos: {}, statistics: {} }, null, 2));
}

// Load database
function loadDatabase() {
    try {
        return JSON.parse(fs.readFileSync(DATABASE_FILE, 'utf8'));
    } catch (e) {
        return { videos: {}, statistics: {} };
    }
}

// Save database
function saveDatabase(data) {
    fs.writeFileSync(DATABASE_FILE, JSON.stringify(data, null, 2));
}

// Parse multipart form data (simplified)
function parseMultipartData(buffer, boundary) {
    const parts = {};
    const boundaryBuffer = Buffer.from(`--${boundary}`);
    const sections = [];
    let start = 0;
    
    // Split by boundary
    for (let i = 0; i < buffer.length - boundaryBuffer.length; i++) {
        if (buffer.slice(i, i + boundaryBuffer.length).equals(boundaryBuffer)) {
            if (start !== 0) {
                sections.push(buffer.slice(start, i));
            }
            start = i + boundaryBuffer.length;
        }
    }
    
    // Parse each section
    sections.forEach(section => {
        const headerEnd = section.indexOf('\r\n\r\n');
        if (headerEnd === -1) return;
        
        const header = section.slice(0, headerEnd).toString();
        const content = section.slice(headerEnd + 4, -2); // Remove trailing \r\n
        
        // Extract field name
        const nameMatch = header.match(/name="([^"]+)"/);
        if (nameMatch) {
            const fieldName = nameMatch[1];
            
            // Check if it's a file
            const filenameMatch = header.match(/filename="([^"]+)"/);
            if (filenameMatch) {
                parts[fieldName] = {
                    filename: filenameMatch[1],
                    data: content
                };
            } else {
                parts[fieldName] = content.toString();
            }
        }
    });
    
    return parts;
}

// Create server
const server = http.createServer((req, res) => {
    // Enable CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    // Handle OPTIONS (CORS preflight)
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // GET endpoints
    if (req.method === 'GET') {
        if (req.url === '/') {
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
                name: 'E.U.R.E.K.A Video Backend (Node.js)',
                version: '1.0.0',
                status: 'running',
                endpoints: {
                    upload: '/api/videos/upload',
                    list: '/api/videos/list',
                    statistics: '/api/statistics'
                }
            }));
        } else if (req.url === '/api/videos/list') {
            const db = loadDatabase();
            const videos = Object.values(db.videos || {});
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ videos, total: videos.length }));
        } else if (req.url === '/api/statistics') {
            const db = loadDatabase();
            const videos = Object.values(db.videos || {});
            const stats = {
                total_videos: videos.length,
                total_views: videos.reduce((sum, v) => sum + (v.views || 0), 0),
                categories: [...new Set(videos.map(v => v.category))]
            };
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(stats));
        } else {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Not found' }));
        }
    }
    
    // POST endpoints
    else if (req.method === 'POST' && req.url === '/api/videos/upload') {
        let body = [];
        
        req.on('data', chunk => {
            body.push(chunk);
        });
        
        req.on('end', () => {
            try {
                const buffer = Buffer.concat(body);
                const boundary = req.headers['content-type'].split('boundary=')[1];
                
                if (!boundary) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'No boundary in content-type' }));
                    return;
                }
                
                const parts = parseMultipartData(buffer, boundary);
                
                // Check for file
                if (!parts.file || !parts.file.filename) {
                    res.writeHead(400, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({ error: 'No file uploaded' }));
                    return;
                }
                
                // Generate unique ID
                const videoId = Date.now() + '-' + Math.random().toString(36).substr(2, 9);
                const filename = `${videoId}-${parts.file.filename}`;
                const filepath = path.join(VIDEO_STORAGE_DIR, 'uploads', filename);
                
                // Save file
                fs.writeFileSync(filepath, parts.file.data);
                
                // Create metadata
                const metadata = {
                    id: videoId,
                    title: parts.title || 'Untitled',
                    description: parts.description || '',
                    category: parts.category || 'general',
                    subcategory: parts.subcategory || 'general',
                    instructor: parts.instructor || 'Unknown',
                    level: parts.level || 'Beginner',
                    filename: filename,
                    original_filename: parts.file.filename,
                    file_path: filepath,
                    upload_date: new Date().toISOString(),
                    views: 0,
                    status: 'active'
                };
                
                // Save to database
                const db = loadDatabase();
                if (!db.videos) db.videos = {};
                db.videos[videoId] = metadata;
                saveDatabase(db);
                
                // Send response
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({
                    success: true,
                    message: 'Video uploaded successfully',
                    video_id: videoId,
                    metadata: metadata
                }));
            } catch (error) {
                console.error('Upload error:', error);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ error: 'Upload failed: ' + error.message }));
            }
        });
    }
    
    else {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'Not found' }));
    }
});

// Start server
server.listen(PORT, () => {
    console.log(`
========================================
E.U.R.E.K.A Video Backend (Node.js)
========================================

Server running at: http://localhost:${PORT}

Endpoints:
- GET  /                     - Server info
- POST /api/videos/upload    - Upload video
- GET  /api/videos/list      - List videos
- GET  /api/statistics       - Get stats

Press Ctrl+C to stop
========================================
    `);
});

// Handle shutdown
process.on('SIGINT', () => {
    console.log('\nServer stopped');
    process.exit();
});