"""EMMA System Prompts Package."""

import os
from pathlib import Path
from typing import Dict

def load_prompt(filename: str) -> str:
    """Load a prompt from a markdown file."""
    prompt_path = Path(__file__).parent / filename
    with open(prompt_path, 'r') as f:
        return f.read()

# Load all system prompts
SYSTEM_PROMPTS: Dict[str, str] = {
    "planner": load_prompt("system_planner.md"),
    "researcher": load_prompt("system_researcher.md"),
    "math": load_prompt("system_math.md"),
    "numeric": load_prompt("system_numeric.md"),
    "code_runner": load_prompt("system_code_runner.md"),
    "verifier": load_prompt("system_verifier.md"),
    "explainer": load_prompt("system_explainer.md"),
}

__all__ = ["SYSTEM_PROMPTS", "load_prompt"]