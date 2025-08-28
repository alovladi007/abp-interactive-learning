#!/usr/bin/env python3
"""
Quick test to verify the backend can start
"""
import sys
import os

# Test imports
try:
    import fastapi
    print("✓ FastAPI imported successfully")
except ImportError as e:
    print(f"✗ Failed to import FastAPI: {e}")
    sys.exit(1)

try:
    import uvicorn
    print("✓ Uvicorn imported successfully")
except ImportError as e:
    print(f"✗ Failed to import Uvicorn: {e}")
    sys.exit(1)

try:
    import pydantic
    print("✓ Pydantic imported successfully")
except ImportError as e:
    print(f"✗ Failed to import Pydantic: {e}")
    sys.exit(1)

try:
    import pulp
    print("✓ PuLP imported successfully")
except ImportError as e:
    print(f"✗ Failed to import PuLP: {e}")
    sys.exit(1)

# Test data files
data_dir = os.path.join(os.path.dirname(__file__), "backend", "data")
data_files = ["skills.json", "modules.json", "resources.json", "roles.json"]

for file in data_files:
    path = os.path.join(data_dir, file)
    if os.path.exists(path):
        print(f"✓ Data file exists: {file}")
    else:
        print(f"✗ Missing data file: {file}")
        sys.exit(1)

print("\n✅ All dependencies and data files are ready!")
print("\nTo start the backend server, run:")
print("  cd backend")
print("  python3 -m uvicorn main:app --reload --port 8000")
print("\nTo start the frontend, run:")
print("  cd frontend")
print("  npm run dev")