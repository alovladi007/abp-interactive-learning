#!/bin/bash

echo "========================================"
echo "Starting E.U.R.E.K.A Video Backend"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating storage directories..."
mkdir -p video_storage/uploads
mkdir -p video_storage/processed
mkdir -p video_storage/archived
mkdir -p thumbnails

# Start the backend
echo ""
echo "🚀 Starting Video Backend Server..."
echo "   URL: http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"
echo ""

# Run the server
python3 main.py