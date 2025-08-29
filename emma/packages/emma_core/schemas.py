"""Core data schemas for EMMA using Pydantic v2."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class AgentRole(str, Enum):
    """Roles for different agents in the system."""
    
    PLANNER = "planner"
    RESEARCHER = "researcher"
    MATH = "math"
    CODE = "code"
    NUMERIC = "numeric"
    EXPLAINER = "explainer"
    VERIFIER = "verifier"


class MediaType(str, Enum):
    """Supported media types for problem inputs."""
    
    IMAGE = "image"
    PDF = "pdf"
    LATEX = "latex"
    MARKDOWN = "markdown"
    CODE = "code"


class CitationType(str, Enum):
    """Types of citations."""
    
    WEB = "web"
    FILE = "file"
    KG = "kg"
    COMPUTATION = "computation"


class ProblemInput(BaseModel):
    """Input schema for a problem to solve."""
    
    id: UUID = Field(default_factory=uuid4)
    user_id: Optional[str] = None
    question: str = Field(..., description="The problem statement in text or markdown")
    media: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Attached media files"
    )
    goals: List[str] = Field(default_factory=list, description="Specific goals to achieve")
    constraints: List[str] = Field(
        default_factory=list, description="Constraints or requirements"
    )
    preferred_units: Optional[str] = Field(None, description="SI or imperial")
    domain_hints: List[str] = Field(
        default_factory=list, description="Domain hints (physics, math, etc.)"
    )
    need_steps: bool = Field(True, description="Whether to show step-by-step solution")
    need_citations: bool = Field(True, description="Whether to include citations")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator("preferred_units")
    @classmethod
    def validate_units(cls, v: Optional[str]) -> Optional[str]:
        if v and v not in ["SI", "imperial"]:
            raise ValueError("preferred_units must be 'SI' or 'imperial'")
        return v


class ToolCall(BaseModel):
    """Record of a tool invocation."""
    
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., description="Tool name")
    args: Dict[str, Any] = Field(..., description="Tool arguments as JSON")
    result: Union[Dict[str, Any], str] = Field(..., description="Tool result")
    latency_ms: int = Field(..., description="Execution time in milliseconds")
    error: Optional[str] = Field(None, description="Error message if failed")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Citation(BaseModel):
    """Citation with provenance information."""
    
    id: UUID = Field(default_factory=uuid4)
    source_id: str = Field(..., description="ID of the source document/URL")
    uri: Optional[str] = Field(None, description="URI of the source")
    chunk_range: Optional[tuple[int, int]] = Field(
        None, description="Character range in source"
    )
    hash: str = Field(..., description="Content hash for verification")
    score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")
    type: CitationType = Field(..., description="Type of citation")
    text: Optional[str] = Field(None, description="Cited text snippet")
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PlanStep(BaseModel):
    """A single step in the execution plan."""
    
    id: UUID = Field(default_factory=uuid4)
    role: AgentRole = Field(..., description="Agent responsible for this step")
    thought: Optional[str] = Field(None, description="Reasoning for this step")
    action: Optional[str] = Field(None, description="Action to take")
    inputs: Dict[str, Any] = Field(default_factory=dict, description="Step inputs")
    outputs: Dict[str, Any] = Field(default_factory=dict, description="Step outputs")
    tool_calls: List[ToolCall] = Field(default_factory=list, description="Tools invoked")
    citations: List[Citation] = Field(default_factory=list, description="Citations collected")
    status: str = Field("pending", description="pending, running, completed, failed")
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class DimensionalCheck(BaseModel):
    """Results of dimensional analysis."""
    
    dimensional_ok: bool = Field(..., description="Whether dimensions are consistent")
    unit_consistency: bool = Field(..., description="Whether units are consistent")
    numeric_residual: Optional[float] = Field(
        None, description="Numerical error if applicable"
    )
    details: Dict[str, Any] = Field(default_factory=dict)


class FinalAnswer(BaseModel):
    """Final answer with metadata."""
    
    id: UUID = Field(default_factory=uuid4)
    problem_id: UUID = Field(..., description="ID of the original problem")
    answer_md: str = Field(..., description="Answer in markdown format")
    summary: str = Field(..., description="Brief summary of the solution")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    checks: DimensionalCheck = Field(..., description="Verification checks")
    citations: List[Citation] = Field(default_factory=list, description="All citations")
    execution_plan: List[PlanStep] = Field(
        default_factory=list, description="Steps taken to solve"
    )
    total_time_ms: int = Field(..., description="Total execution time")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class RunTrace(BaseModel):
    """Complete trace of a problem-solving run."""
    
    id: UUID = Field(default_factory=uuid4)
    problem: ProblemInput
    plan: List[PlanStep]
    answer: Optional[FinalAnswer] = None
    status: str = Field("running", description="running, completed, failed")
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)