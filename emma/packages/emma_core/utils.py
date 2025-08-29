"""Utility functions for EMMA."""

import logging
import time
from contextlib import contextmanager
from typing import Any, Dict, Optional
import hashlib
import json


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger


class Timer:
    """Simple timer for measuring execution time."""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def start(self):
        """Start the timer."""
        self.start_time = time.time()
    
    def stop(self):
        """Stop the timer."""
        self.end_time = time.time()
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0
        end = self.end_time or time.time()
        return end - self.start_time
    
    @property
    def elapsed_ms(self) -> int:
        """Get elapsed time in milliseconds."""
        return int(self.elapsed * 1000)


@contextmanager
def timing_context():
    """Context manager for timing code execution."""
    timer = Timer()
    timer.start()
    try:
        yield timer
    finally:
        timer.stop()


def hash_content(content: str) -> str:
    """Generate SHA256 hash of content."""
    return hashlib.sha256(content.encode()).hexdigest()


def hash_dict(data: Dict[str, Any]) -> str:
    """Generate hash of a dictionary."""
    json_str = json.dumps(data, sort_keys=True)
    return hash_content(json_str)


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_number(num: float, precision: int = 4) -> str:
    """Format number with specified precision."""
    if abs(num) < 1e-10:
        return "0"
    elif abs(num) < 0.01 or abs(num) > 1e6:
        return f"{num:.{precision}e}"
    else:
        return f"{num:.{precision}f}".rstrip('0').rstrip('.')


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Safely divide two numbers."""
    if b == 0:
        return default
    return a / b


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max."""
    return max(min_val, min(value, max_val))


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    def check(self, key: str) -> bool:
        """Check if request is allowed."""
        now = time.time()
        
        # Clean old entries
        self.requests = {
            k: times for k, times in self.requests.items()
            if any(t > now - self.window_seconds for t in times)
        }
        
        # Get request times for key
        if key not in self.requests:
            self.requests[key] = []
        
        # Filter to current window
        self.requests[key] = [
            t for t in self.requests[key]
            if t > now - self.window_seconds
        ]
        
        # Check limit
        if len(self.requests[key]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True