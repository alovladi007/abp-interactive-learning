"""LangGraph-based orchestration for EMMA."""

import asyncio
from typing import Any, Dict, List, Optional, TypedDict
from uuid import UUID, uuid4

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
    MathAgent,
    NumericAgent,
    CodeAgent,
    ExplainerAgent,
    VerifierAgent,
)
from .tools import ToolRegistry

logger = get_logger(__name__)


class GraphState(TypedDict):
    """State for the LangGraph execution."""
    
    problem: ProblemInput
    messages: List[BaseMessage]
    plan: List[PlanStep]
    current_step: Optional[PlanStep]
    citations: List[Citation]
    final_answer: Optional[FinalAnswer]
    error: Optional[str]


class EMMAOrchestrator:
    """Main orchestrator using LangGraph for multi-agent coordination."""
    
    def __init__(self):
        self.graph = self._build_graph()
        self.memory = MemorySaver()
        self.tool_registry = ToolRegistry()
        self.agents = self._initialize_agents()
        self.active_runs: Dict[UUID, RunTrace] = {}
    
    def _initialize_agents(self) -> Dict[AgentRole, Any]:
        """Initialize all agents."""
        return {
            AgentRole.PLANNER: PlannerAgent(self.tool_registry),
            AgentRole.RESEARCHER: ResearcherAgent(self.tool_registry),
            AgentRole.MATH: MathAgent(self.tool_registry),
            AgentRole.NUMERIC: NumericAgent(self.tool_registry),
            AgentRole.CODE: CodeAgent(self.tool_registry),
            AgentRole.EXPLAINER: ExplainerAgent(self.tool_registry),
            AgentRole.VERIFIER: VerifierAgent(self.tool_registry),
        }
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph execution graph."""
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("math", self._math_node)
        workflow.add_node("numeric", self._numeric_node)
        workflow.add_node("code", self._code_node)
        workflow.add_node("explainer", self._explainer_node)
        workflow.add_node("verifier", self._verifier_node)
        
        # Add edges
        workflow.set_entry_point("planner")
        
        # Conditional routing based on plan
        workflow.add_conditional_edges(
            "planner",
            self._route_from_planner,
            {
                "researcher": "researcher",
                "math": "math",
                "numeric": "numeric",
                "code": "code",
                "explainer": "explainer",
                "end": END,
            },
        )
        
        # All agents can route back to planner or to explainer
        for node in ["researcher", "math", "numeric", "code"]:
            workflow.add_conditional_edges(
                node,
                self._route_from_agent,
                {
                    "planner": "planner",
                    "explainer": "explainer",
                    "verifier": "verifier",
                },
            )
        
        # Verifier routes to explainer or back to planner
        workflow.add_conditional_edges(
            "verifier",
            self._route_from_verifier,
            {
                "planner": "planner",
                "explainer": "explainer",
            },
        )
        
        # Explainer is terminal
        workflow.add_edge("explainer", END)
        
        return workflow.compile(checkpointer=self.memory)
    
    async def _planner_node(self, state: GraphState) -> GraphState:
        """Planner agent node."""
        logger.info("Executing planner node")
        agent = self.agents[AgentRole.PLANNER]
        
        # Generate or update plan
        plan = await agent.create_plan(state["problem"], state.get("plan", []))
        state["plan"] = plan
        
        # Select next step
        next_step = self._get_next_pending_step(plan)
        state["current_step"] = next_step
        
        return state
    
    async def _researcher_node(self, state: GraphState) -> GraphState:
        """Researcher agent node."""
        logger.info("Executing researcher node")
        agent = self.agents[AgentRole.RESEARCHER]
        step = state["current_step"]
        
        # Perform research
        results, citations = await agent.research(
            query=step.inputs.get("query", state["problem"].question),
            filters=step.inputs.get("filters", {}),
        )
        
        # Update state
        step.outputs = results
        step.citations = citations
        step.status = "completed"
        state["citations"].extend(citations)
        
        return state
    
    async def _math_node(self, state: GraphState) -> GraphState:
        """Math symbolic agent node."""
        logger.info("Executing math node")
        agent = self.agents[AgentRole.MATH]
        step = state["current_step"]
        
        # Perform symbolic computation
        result = await agent.solve_symbolic(
            expression=step.inputs.get("expression"),
            variables=step.inputs.get("variables", {}),
        )
        
        step.outputs = {"result": result}
        step.status = "completed"
        
        return state
    
    async def _numeric_node(self, state: GraphState) -> GraphState:
        """Numeric computation agent node."""
        logger.info("Executing numeric node")
        agent = self.agents[AgentRole.NUMERIC]
        step = state["current_step"]
        
        # Perform numeric computation
        result = await agent.compute_numeric(
            problem=step.inputs.get("problem"),
            method=step.inputs.get("method"),
        )
        
        step.outputs = {"result": result}
        step.status = "completed"
        
        return state
    
    async def _code_node(self, state: GraphState) -> GraphState:
        """Code execution agent node."""
        logger.info("Executing code node")
        agent = self.agents[AgentRole.CODE]
        step = state["current_step"]
        
        # Execute code
        result = await agent.execute_code(
            code=step.inputs.get("code"),
            language=step.inputs.get("language", "python"),
        )
        
        step.outputs = result
        step.status = "completed"
        
        return state
    
    async def _explainer_node(self, state: GraphState) -> GraphState:
        """Explainer agent node."""
        logger.info("Executing explainer node")
        agent = self.agents[AgentRole.EXPLAINER]
        
        # Generate final answer
        answer = await agent.explain_solution(
            problem=state["problem"],
            plan=state["plan"],
            citations=state["citations"],
        )
        
        state["final_answer"] = answer
        
        return state
    
    async def _verifier_node(self, state: GraphState) -> GraphState:
        """Verifier agent node."""
        logger.info("Executing verifier node")
        agent = self.agents[AgentRole.VERIFIER]
        step = state["current_step"]
        
        # Perform verification
        checks = await agent.verify(
            expression=step.outputs.get("result"),
            expected_units=state["problem"].preferred_units,
        )
        
        step.outputs["verification"] = checks
        
        return state
    
    def _route_from_planner(self, state: GraphState) -> str:
        """Route from planner based on next step."""
        if state["current_step"] is None:
            return "end"
        return state["current_step"].role.value
    
    def _route_from_agent(self, state: GraphState) -> str:
        """Route from agent nodes."""
        # Check if all steps are complete
        pending_steps = [s for s in state["plan"] if s.status == "pending"]
        
        if not pending_steps:
            # All done, go to explainer
            return "explainer"
        elif state["current_step"].outputs.get("needs_verification"):
            # Needs verification
            return "verifier"
        else:
            # Back to planner for next step
            return "planner"
    
    def _route_from_verifier(self, state: GraphState) -> str:
        """Route from verifier."""
        verification = state["current_step"].outputs.get("verification", {})
        
        if verification.get("dimensional_ok") and verification.get("unit_consistency"):
            # Verification passed, continue
            return "planner"
        else:
            # Verification failed, go to explainer with error
            return "explainer"
    
    def _get_next_pending_step(self, plan: List[PlanStep]) -> Optional[PlanStep]:
        """Get the next pending step from the plan."""
        for step in plan:
            if step.status == "pending":
                return step
        return None
    
    async def initialize(self):
        """Initialize the orchestrator."""
        logger.info("Initializing EMMA Orchestrator")
        await self.tool_registry.initialize()
        for agent in self.agents.values():
            await agent.initialize()
    
    async def cleanup(self):
        """Cleanup resources."""
        logger.info("Cleaning up EMMA Orchestrator")
        await self.tool_registry.cleanup()
        for agent in self.agents.values():
            await agent.cleanup()
    
    async def start_solve(self, problem: ProblemInput, background_tasks) -> UUID:
        """Start solving a problem."""
        run_id = uuid4()
        
        # Create initial state
        initial_state: GraphState = {
            "problem": problem,
            "messages": [HumanMessage(content=problem.question)],
            "plan": [],
            "current_step": None,
            "citations": [],
            "final_answer": None,
            "error": None,
        }
        
        # Create run trace
        trace = RunTrace(
            id=run_id,
            problem=problem,
            plan=[],
            status="running",
        )
        self.active_runs[run_id] = trace
        
        # Start async execution
        background_tasks.add_task(self._execute_graph, run_id, initial_state)
        
        return run_id
    
    async def _execute_graph(self, run_id: UUID, initial_state: GraphState):
        """Execute the graph asynchronously."""
        try:
            # Run the graph
            config = {"configurable": {"thread_id": str(run_id)}}
            final_state = await self.graph.ainvoke(initial_state, config)
            
            # Update trace
            trace = self.active_runs[run_id]
            trace.plan = final_state["plan"]
            trace.answer = final_state["final_answer"]
            trace.status = "completed"
            
        except Exception as e:
            logger.error(f"Error executing graph for run {run_id}: {e}")
            trace = self.active_runs[run_id]
            trace.status = "failed"
            trace.metadata["error"] = str(e)
    
    async def get_trace(self, run_id: str, user_id: str) -> Optional[RunTrace]:
        """Get trace for a run."""
        run_uuid = UUID(run_id)
        trace = self.active_runs.get(run_uuid)
        
        if trace and trace.problem.user_id == user_id:
            return trace
        return None
    
    async def get_citations(self, run_id: str, user_id: str) -> List[Citation]:
        """Get citations for a run."""
        trace = await self.get_trace(run_id, user_id)
        if trace and trace.answer:
            return trace.answer.citations
        return []
    
    async def run_tool(self, tool_name: str, args: Dict[str, Any]) -> Any:
        """Run a tool directly."""
        tool = self.tool_registry.get_tool(tool_name)
        if not tool:
            raise ValueError(f"Tool {tool_name} not found")
        return await tool.run(**args)
    
    async def ingest_document(self, filename: str, content: bytes, user_id: str) -> str:
        """Ingest a document."""
        # This would call the retriever service
        # For now, return a mock ID
        return f"doc_{uuid4()}"
    
    async def get_health(self) -> Dict[str, Any]:
        """Get health status of all services."""
        return {
            "all_healthy": True,
            "api": "healthy",
            "database": "healthy",
            "redis": "healthy",
            "neo4j": "healthy",
            "minio": "healthy",
        }