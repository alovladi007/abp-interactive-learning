"""
Minimal LangGraph planner for EMMA
"""
from typing import Dict, Any
from langgraph.graph import StateGraph, END

def _detect_intent(question: str) -> str:
    """Detect the intent from question."""
    q = question.lower()
    if "integrate" in q or "∫" in q:
        return "integrate"
    if "=" in q:
        return "solve_equation"
    if "code" in q or "python" in q:
        return "code"
    return "explain"

def make_planner_graph():
    """Create the planner graph."""
    sg = StateGraph(dict)
    
    def planner_node(state: Dict[str, Any]) -> Dict[str, Any]:
        intent = _detect_intent(state.get("question", ""))
        state["intent"] = intent
        state.setdefault("trace", []).append({"node": "planner", "intent": intent})
        return state
    
    def researcher_node(state: Dict[str, Any]) -> Dict[str, Any]:
        state.setdefault("trace", []).append({"node": "researcher", "status": "retrieved"})
        return state
    
    def math_node(state: Dict[str, Any]) -> Dict[str, Any]:
        state.setdefault("trace", []).append({"node": "math", "status": "computed"})
        return state
    
    def done_node(state: Dict[str, Any]) -> Dict[str, Any]:
        state["status"] = "completed"
        return state
    
    # Add nodes
    sg.add_node("planner", planner_node)
    sg.add_node("researcher", researcher_node)
    sg.add_node("math", math_node)
    sg.add_node("done", done_node)
    
    # Add routing
    def route_from_planner(state: Dict[str, Any]) -> str:
        intent = state.get("intent", "explain")
        if intent in ["integrate", "solve_equation"]:
            return "math"
        return "researcher"
    
    # Add edges
    sg.set_entry_point("planner")
    sg.add_conditional_edges("planner", route_from_planner, {
        "math": "math",
        "researcher": "researcher"
    })
    sg.add_edge("researcher", "done")
    sg.add_edge("math", "done")
    sg.set_finish_point("done")
    
    return sg.compile()
