"""EMMA Core - Shared schemas, utilities, and tool wrappers."""

from .schemas import (
    ProblemInput,
    PlanStep,
    ToolCall,
    Citation,
    FinalAnswer,
    AgentRole,
    MediaType,
)
from .tools import ToolRegistry, BaseTool
from .graph import GraphNode, GraphEdge, ExecutionGraph
from .utils import get_logger, timing_context

__version__ = "1.0.0"

__all__ = [
    "ProblemInput",
    "PlanStep",
    "ToolCall",
    "Citation",
    "FinalAnswer",
    "AgentRole",
    "MediaType",
    "ToolRegistry",
    "BaseTool",
    "GraphNode",
    "GraphEdge",
    "ExecutionGraph",
    "get_logger",
    "timing_context",
]