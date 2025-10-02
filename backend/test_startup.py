#!/usr/bin/env python3
"""
Test script to verify all routes are loaded correctly
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("🔍 Testing route imports...")
    from api.emma_routes import router as emma_router
    print("✓ EMMA routes loaded")

    from api.max_routes import router as max_router
    print("✓ MAX routes loaded")

    print("\n📊 Route Information:")
    print(f"  EMMA: {emma_router.prefix} ({len(emma_router.routes)} endpoints)")
    print(f"  MAX:  {max_router.prefix} ({len(max_router.routes)} endpoints)")

    print("\n✅ All routes loaded successfully!")
    print("\n🚀 To start the server, run:")
    print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")

except Exception as e:
    print(f"\n❌ Error loading routes: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
