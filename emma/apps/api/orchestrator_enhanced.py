"""Enhanced LangGraph orchestration with proper routing and tool selection."""

import asyncio
from typing import Any, Dict, List, Optional, TypedDict, Literal
from uuid import UUID, uuid4
from enum import Enum

from langchain.schema import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, StateGraph
from langgraph.checkpoint import MemorySaver

from emma_core import (
    ProblemInput,
    PlanStep,
    FinalAnswer,
    RunTrace,
    Citation,
    AgentRole,
    get_logger,
)
from emma_prompts import SYSTEM_PROMPTS
from .agents import (
    PlannerAgent,
    ResearcherAgent,
    MathSymbolicAgent,
    NumericComputeAgent,
    CodeRunnerAgent,
    ExplainerAgent,
    VerifierAgent,
)
from .tools import EnhancedToolRegistry
from .compute_selector import ComputeSelector

logger = get_logger(__name__)


class ProblemType(str, Enum):
    """Types of problems for routing."""
    SYMBOLIC = "symbolic"
    NUMERIC = "numeric"
    CODE = "code"
    HYBRID = "hybrid"


class GraphState(TypedDict):
    """Enhanced state for LangGraph execution."""
    
    problem: ProblemInput
    messages: List[BaseMessage]
    plan: List[PlanStep]
    current_step: Optional[PlanStep]
    problem_type: Optional[ProblemType]
    citations: List[Citation]
    artifacts: List[Dict[str, Any]]  # Plots, files, etc.
    verification_results: Dict[str, Any]
    final_answer: Optional[FinalAnswer]
    error: Optional[str]
    metadata: Dict[str, Any]


class EnhancedOrchestrator:
    """Enhanced orchestrator with proper flow control and tool selection."""
    
    def __init__(self):
        self.graph = self._build_enhanced_graph()
        self.memory = MemorySaver()
        self.tool_registry = EnhancedToolRegistry()
        self.compute_selector = ComputeSelector()
        self.agents = self._initialize_agents()
        self.active_runs: Dict[UUID, RunTrace] = {}
    
    def _initialize_agents(self) -> Dict[AgentRole, Any]:
        """Initialize all agents with enhanced capabilities."""
        return {
            AgentRole.PLANNER: PlannerAgent(
                self.tool_registry,
                system_prompt=SYSTEM_PROMPTS["planner"]
            ),
            AgentRole.RESEARCHER: ResearcherAgent(
                self.tool_registry,
                system_prompt=SYSTEM_PROMPTS["researcher"]
            ),
            AgentRole.MATH: MathSymbolicAgent(
                self.tool_registry,
                self.compute_selector,
                system_prompt=SYSTEM_PROMPTS["math"]
            ),
            AgentRole.NUMERIC: NumericComputeAgent(
                self.tool_registry,
                self.compute_selector,
                system_prompt=SYSTEM_PROMPTS["numeric"]
            ),
            AgentRole.CODE: CodeRunnerAgent(
                self.tool_registry,
                system_prompt=SYSTEM_PROMPTS["code_runner"]
            ),
            AgentRole.EXPLAINER: ExplainerAgent(
                self.tool_registry,
                system_prompt=SYSTEM_PROMPTS["explainer"]
            ),
            AgentRole.VERIFIER: VerifierAgent(
                self.tool_registry,
                system_prompt=SYSTEM_PROMPTS["verifier"]
            ),
        }
    
    def _build_enhanced_graph(self) -> StateGraph:
        """Build enhanced LangGraph with proper routing."""
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("math_symbolic", self._math_symbolic_node)
        workflow.add_node("numeric_compute", self._numeric_compute_node)
        workflow.add_node("code_runner", self._code_runner_node)
        workflow.add_node("verifier", self._verifier_node)
        workflow.add_node("explainer", self._explainer_node)
        
        # Entry point
        workflow.set_entry_point("planner")
        
        # Planner routing based on problem type
        workflow.add_conditional_edges(
            "planner",
            self._route_from_planner,
            {
                "researcher": "researcher",
                "math_symbolic": "math_symbolic",
                "numeric_compute": "numeric_compute",
                "code_runner": "code_runner",
                "explainer": "explainer",
                "end": END,
            },
        )
        
        # Researcher can route to any computational node
        workflow.add_conditional_edges(
            "researcher",
            self._route_from_researcher,
            {
                "math_symbolic": "math_symbolic",
                "numeric_compute": "numeric_compute",
                "code_runner": "code_runner",
                "planner": "planner",
            },
        )
        
        # Math symbolic can request numeric verification
        workflow.add_conditional_edges(
            "math_symbolic",
            self._route_from_math,
            {
                "numeric_compute": "numeric_compute",
                "verifier": "verifier",
                "researcher": "researcher",
                "planner": "planner",
            },
        )
        
        # Numeric can request symbolic derivation
        workflow.add_conditional_edges(
            "numeric_compute",
            self._route_from_numeric,
            {
                "math_symbolic": "math_symbolic",
                "code_runner": "code_runner",
                "verifier": "verifier",
                "planner": "planner",
            },
        )
        
        # Code runner routes to verifier
        workflow.add_conditional_edges(
            "code_runner",
            self._route_from_code,
            {
                "verifier": "verifier",
                "planner": "planner",
            },
        )
        
        # Verifier can bounce back or proceed to explainer
        workflow.add_conditional_edges(
            "verifier",
            self._route_from_verifier,
            {
                "math_symbolic": "math_symbolic",
                "numeric_compute": "numeric_compute",
                "explainer": "explainer",
                "planner": "planner",
            },
        )
        
        # Explainer is terminal
        workflow.add_edge("explainer", END)
        
        return workflow.compile(checkpointer=self.memory)
    
    async def _planner_node(self, state: GraphState) -> GraphState:
        """Enhanced planner with problem type detection."""
        logger.info("Executing enhanced planner node")
        agent = self.agents[AgentRole.PLANNER]
        
        # Analyze problem type
        problem_type = await agent.analyze_problem_type(state["problem"])
        state["problem_type"] = problem_type
        
        # Create step DAG
        plan = await agent.create_step_dag(
            problem=state["problem"],
            problem_type=problem_type,
            existing_plan=state.get("plan", [])
        )
        state["plan"] = plan
        
        # Select next step
        next_step = self._get_next_pending_step(plan)
        state["current_step"] = next_step
        
        # Add metadata
        state["metadata"]["planning_iterations"] = state["metadata"].get("planning_iterations", 0) + 1
        
        return state
    
    async def _researcher_node(self, state: GraphState) -> GraphState:
        """Enhanced researcher with hybrid retrieval."""
        logger.info("Executing researcher node")
        agent = self.agents[AgentRole.RESEARCHER]
        step = state["current_step"]
        
        # Perform hybrid retrieval (lexical + vector + KG)
        results = await agent.hybrid_retrieval(
            query=step.inputs.get("query", state["problem"].question),
            filters=step.inputs.get("filters", {}),
            use_kg=step.inputs.get("use_kg", True),
            k=step.inputs.get("k", 10)
        )
        
        # Extract and normalize citations
        citations = await agent.normalize_citations(results)
        
        # Update state
        step.outputs = {"retrieved_docs": results}
        step.citations = citations
        step.status = "completed"
        state["citations"].extend(citations)
        
        return state
    
    async def _math_symbolic_node(self, state: GraphState) -> GraphState:
        """Math symbolic with Wolfram/SymPy selection."""
        logger.info("Executing math symbolic node")
        agent = self.agents[AgentRole.MATH]
        step = state["current_step"]
        
        # Select compute engine based on problem
        engine = self.compute_selector.select_symbolic_engine(
            expression=step.inputs.get("expression"),
            prefer_closed_form=step.inputs.get("prefer_closed_form", True)
        )
        
        # Execute symbolic computation
        if engine == "wolfram":
            result = await agent.wolfram_solve(
                code=step.inputs.get("wolfram_code"),
                timeout=step.inputs.get("timeout", 30)
            )
        else:  # SymPy fallback
            result = await agent.sympy_solve(
                expression=step.inputs.get("expression"),
                variables=step.inputs.get("variables", {})
            )
        
        # Store results with LaTeX and machine forms
        step.outputs = {
            "result": result,
            "engine": engine,
            "latex": result.get("latex"),
            "machine_form": result.get("machine_form")
        }
        step.status = "completed"
        
        # Add artifacts if any (e.g., Wolfram images)
        if result.get("artifacts"):
            state["artifacts"].extend(result["artifacts"])
        
        return state
    
    async def _numeric_compute_node(self, state: GraphState) -> GraphState:
        """Numeric computation with MATLAB/JAX selection."""
        logger.info("Executing numeric compute node")
        agent = self.agents[AgentRole.NUMERIC]
        step = state["current_step"]
        
        # Select compute engine for numerics
        engine = self.compute_selector.select_numeric_engine(
            problem_type=step.inputs.get("problem_type"),
            requires_ode=step.inputs.get("requires_ode", False),
            requires_optimization=step.inputs.get("requires_optimization", False)
        )
        
        # Execute numeric computation
        if engine == "matlab":
            result = await agent.matlab_compute(
                code=step.inputs.get("matlab_code"),
                timeout=step.inputs.get("timeout", 30)
            )
        else:  # JAX/NumPy fallback
            result = await agent.jax_compute(
                code=step.inputs.get("python_code"),
                use_jit=step.inputs.get("use_jit", True)
            )
        
        # Generate plots if needed
        if step.inputs.get("generate_plot"):
            plot = await agent.generate_plot(
                data=result.get("data"),
                plot_type=step.inputs.get("plot_type", "line")
            )
            state["artifacts"].append(plot)
        
        # Store results with solver settings
        step.outputs = {
            "result": result,
            "engine": engine,
            "solver_settings": result.get("solver_settings"),
            "residuals": result.get("residuals")
        }
        step.status = "completed"
        
        return state
    
    async def _code_runner_node(self, state: GraphState) -> GraphState:
        """Code runner with sandboxed execution."""
        logger.info("Executing code runner node")
        agent = self.agents[AgentRole.CODE]
        step = state["current_step"]
        
        # Prepare sandbox environment
        sandbox_config = {
            "language": step.inputs.get("language", "python"),
            "timeout": step.inputs.get("timeout", 30),
            "memory_mb": step.inputs.get("memory_mb", 512),
            "cpu_shares": step.inputs.get("cpu_shares", 512),
            "network": False,  # No network in sandbox
        }
        
        # Execute code in sandbox
        result = await agent.sandbox_execute(
            code=step.inputs.get("code"),
            test_cases=step.inputs.get("test_cases", []),
            config=sandbox_config
        )
        
        # Store outputs and artifacts
        step.outputs = {
            "stdout": result.get("stdout"),
            "stderr": result.get("stderr"),
            "exit_code": result.get("exit_code"),
            "test_results": result.get("test_results")
        }
        
        # Add generated files as artifacts
        if result.get("files"):
            for file in result["files"]:
                state["artifacts"].append({
                    "type": "file",
                    "name": file["name"],
                    "content": file["content"],
                    "mime_type": file.get("mime_type")
                })
        
        step.status = "completed"
        return state
    
    async def _verifier_node(self, state: GraphState) -> GraphState:
        """Enhanced verifier with multiple checks."""
        logger.info("Executing verifier node")
        agent = self.agents[AgentRole.VERIFIER]
        
        # Perform comprehensive verification
        verification = await agent.comprehensive_verify(
            results=self._collect_results(state),
            problem=state["problem"],
            checks=[
                "dimensional_analysis",
                "unit_consistency",
                "numeric_residuals",
                "conservation_laws",
                "boundary_conditions",
                "sanity_checks"
            ]
        )
        
        state["verification_results"] = verification
        
        # Determine if refinement needed
        if not verification["all_passed"]:
            state["metadata"]["verification_failures"] = verification["failures"]
        
        return state
    
    async def _explainer_node(self, state: GraphState) -> GraphState:
        """Enhanced explainer with structured output."""
        logger.info("Executing explainer node")
        agent = self.agents[AgentRole.EXPLAINER]
        
        # Generate comprehensive answer
        answer = await agent.generate_answer(
            problem=state["problem"],
            plan=state["plan"],
            citations=state["citations"],
            artifacts=state["artifacts"],
            verification=state["verification_results"],
            include_steps=state["problem"].need_steps,
            include_citations=state["problem"].need_citations
        )
        
        state["final_answer"] = answer
        return state
    
    def _route_from_planner(self, state: GraphState) -> str:
        """Enhanced routing from planner based on problem type."""
        if state["current_step"] is None:
            return "end"
        
        step = state["current_step"]
        problem_type = state.get("problem_type", ProblemType.HYBRID)
        
        # Route based on step role and problem type
        if step.role == AgentRole.RESEARCHER:
            return "researcher"
        elif problem_type == ProblemType.SYMBOLIC or step.inputs.get("force_symbolic"):
            return "math_symbolic"
        elif problem_type == ProblemType.NUMERIC or step.inputs.get("force_numeric"):
            return "numeric_compute"
        elif problem_type == ProblemType.CODE or step.inputs.get("requires_code"):
            return "code_runner"
        else:
            # Default to math symbolic for hybrid problems
            return "math_symbolic"
    
    def _route_from_researcher(self, state: GraphState) -> str:
        """Route from researcher based on retrieved information."""
        step = state["current_step"]
        
        if step.outputs.get("found_equations"):
            return "math_symbolic"
        elif step.outputs.get("found_numeric_data"):
            return "numeric_compute"
        elif step.outputs.get("found_code_examples"):
            return "code_runner"
        else:
            return "planner"  # Need new plan
    
    def _route_from_math(self, state: GraphState) -> str:
        """Route from math symbolic."""
        step = state["current_step"]
        
        if step.outputs.get("needs_numeric_verification"):
            return "numeric_compute"
        elif step.outputs.get("needs_more_info"):
            return "researcher"
        elif self._all_steps_complete(state):
            return "verifier"
        else:
            return "planner"
    
    def _route_from_numeric(self, state: GraphState) -> str:
        """Route from numeric compute."""
        step = state["current_step"]
        
        if step.outputs.get("needs_symbolic_derivation"):
            return "math_symbolic"
        elif step.outputs.get("needs_plotting"):
            return "code_runner"
        elif self._all_steps_complete(state):
            return "verifier"
        else:
            return "planner"
    
    def _route_from_code(self, state: GraphState) -> str:
        """Route from code runner."""
        if self._all_steps_complete(state):
            return "verifier"
        else:
            return "planner"
    
    def _route_from_verifier(self, state: GraphState) -> str:
        """Route from verifier based on verification results."""
        verification = state["verification_results"]
        
        if not verification["all_passed"]:
            # Determine which component needs refinement
            if "dimensional_error" in verification["failures"]:
                return "math_symbolic"
            elif "numeric_instability" in verification["failures"]:
                return "numeric_compute"
            else:
                return "planner"  # Replan
        else:
            return "explainer"
    
    def _get_next_pending_step(self, plan: List[PlanStep]) -> Optional[PlanStep]:
        """Get next step respecting dependencies."""
        for step in plan:
            if step.status == "pending":
                # Check if dependencies are satisfied
                deps_satisfied = all(
                    plan[dep_idx].status == "completed"
                    for dep_idx in step.inputs.get("dependencies", [])
                )
                if deps_satisfied:
                    return step
        return None
    
    def _all_steps_complete(self, state: GraphState) -> bool:
        """Check if all planned steps are complete."""
        return all(step.status == "completed" for step in state["plan"])
    
    def _collect_results(self, state: GraphState) -> Dict[str, Any]:
        """Collect all results for verification."""
        results = {}
        for step in state["plan"]:
            if step.status == "completed":
                results[f"{step.role}_{step.id}"] = step.outputs
        return results