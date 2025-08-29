"""
Expert Orchestration with LangGraph
"""

from typing import Any, Dict, List
from langgraph.graph import StateGraph, END
from langchain.schema import BaseMessage

from .agents import (
    PlannerAgent, ResearcherAgent, MathematicianAgent,
    VerifierAgent, ExplainerAgent, VisualizerAgent,
    EducatorAgent, AssessorAgent
)

class ExpertOrchestrator:
    """Multi-agent orchestration for expert problem-solving."""
    
    def __init__(self):
        self.agents = {
            "planner": PlannerAgent(),
            "researcher": ResearcherAgent(),
            "mathematician": MathematicianAgent(),
            "verifier": VerifierAgent(),
            "explainer": ExplainerAgent(),
            "visualizer": VisualizerAgent(),
            "educator": EducatorAgent(),
            "assessor": AssessorAgent()
        }
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the expert orchestration graph."""
        workflow = StateGraph(Dict)
        
        # Add all agent nodes
        for name, agent in self.agents.items():
            workflow.add_node(name, agent.process)
        
        # Complex routing logic
        workflow.set_entry_point("planner")
        
        # Planner routes to appropriate specialist
        workflow.add_conditional_edges(
            "planner",
            self._route_from_planner,
            {
                "researcher": "researcher",
                "mathematician": "mathematician",
                "educator": "educator",
                "end": END
            }
        )
        
        # Researcher can invoke mathematician
        workflow.add_conditional_edges(
            "researcher",
            lambda x: "mathematician" if x["needs_computation"] else "explainer",
            {"mathematician": "mathematician", "explainer": "explainer"}
        )
        
        # Mathematician always goes to verifier
        workflow.add_edge("mathematician", "verifier")
        
        # Verifier can loop back or proceed
        workflow.add_conditional_edges(
            "verifier",
            lambda x: "mathematician" if not x["verified"] else "visualizer",
            {"mathematician": "mathematician", "visualizer": "visualizer"}
        )
        
        # Visualizer to explainer
        workflow.add_edge("visualizer", "explainer")
        
        # Educator path
        workflow.add_edge("educator", "assessor")
        workflow.add_edge("assessor", "explainer")
        
        # Explainer is terminal
        workflow.add_edge("explainer", END)
        
        return workflow.compile()
    
    def _route_from_planner(self, state: Dict) -> str:
        """Intelligent routing based on problem type."""
        problem_type = state.get("problem_type", "general")
        
        if problem_type == "research":
            return "researcher"
        elif problem_type in ["computation", "proof"]:
            return "mathematician"
        elif problem_type == "learning":
            return "educator"
        else:
            return "researcher"
    
    async def solve(self, problem: Dict, mode: str, level: str) -> Dict:
        """Orchestrate the solution process."""
        initial_state = {
            "problem": problem,
            "mode": mode,
            "level": level,
            "messages": [],
            "steps": [],
            "solution": None
        }
        
        result = await self.graph.ainvoke(initial_state)
        return result
    
    def health(self) -> str:
        """Check orchestrator health."""
        return "healthy"
