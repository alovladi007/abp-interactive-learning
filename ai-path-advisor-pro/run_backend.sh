#!/bin/bash
echo "Starting AI Path Advisor Pro Backend..."
cd /workspace/ai-path-advisor-pro/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload