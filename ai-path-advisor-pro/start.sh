#!/bin/bash

echo "🚀 Starting AI Path Advisor Pro..."
echo "=================================="

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "⚠️  Port $1 is already in use. Please stop the existing service."
        return 1
    fi
    return 0
}

# Check required ports
check_port 8000
BACKEND_PORT_FREE=$?
check_port 3000
FRONTEND_PORT_FREE=$?

if [ $BACKEND_PORT_FREE -ne 0 ] || [ $FRONTEND_PORT_FREE -ne 0 ]; then
    echo "Please free up the required ports and try again."
    exit 1
fi

# Start backend
echo "📦 Starting Backend Server..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
echo "Installing backend dependencies..."
pip install -q -r requirements.txt

# Start backend server in background
echo "Starting FastAPI server on port 8000..."
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Wait for backend to start
sleep 3

# Start frontend
echo ""
echo "📱 Starting Frontend Server..."
cd ../frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Start frontend server
echo "Starting Next.js server on port 3000..."
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "=================================="
echo "✅ AI Path Advisor Pro is running!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=================================="

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Services stopped."
    exit 0
}

# Set up trap to cleanup on Ctrl+C
trap cleanup INT

# Wait for processes
wait