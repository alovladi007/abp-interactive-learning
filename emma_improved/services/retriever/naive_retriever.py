"""
Naive retriever for fallback when pgvector not available
"""
import re
from typing import List, Dict

def naive_search(query: str, top_k: int = 3) -> List[Dict]:
    """Simple search without database."""
    # Mock results for demo
    return [
        {
            "file": "demo.md",
            "sha": "abc123",
            "score": 0.8,
            "highlight": "Demo result for: " + query[:50]
        }
    ]
