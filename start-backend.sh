#!/bin/bash

echo "Starting AI Path Advisor Backend Services..."
echo "=========================================="

# Navigate to backend directory
cd ai-path-advisor-starter/backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q fastapi uvicorn pydantic python-multipart

# Start the main API server
echo "Starting main API server on port 8000..."
python main.py &
MAIN_PID=$!

# Start the profile API server
echo "Starting profile API server on port 8001..."
python profile_api.py &
PROFILE_PID=$!

echo ""
echo "=========================================="
echo "Backend services are running!"
echo "Main API: http://localhost:8000"
echo "Profile API: http://localhost:8001"
echo "API Documentation: http://localhost:8000/docs"
echo "Profile API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="

# Wait for interrupt
trap "kill $MAIN_PID $PROFILE_PID; exit" INT
wait