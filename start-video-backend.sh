#!/bin/bash

echo "========================================"
echo "Starting Video Upload Backend"
echo "========================================"
echo ""

cd /workspace/video-backend

# Kill any existing process on port 8001
echo "Checking for existing processes on port 8001..."
lsof -ti:8001 | xargs kill -9 2>/dev/null

echo "Starting simple video backend..."
python3 simple_backend.py