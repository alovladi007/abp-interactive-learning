"""Tool registry and base implementations for EMMA."""

import asyncio
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, Field
import httpx
import sympy as sp
import numpy as np

from .schemas import ToolCall
from .utils import get_logger, timing_context

logger = get_logger(__name__)


class ToolSchema(BaseModel):
    """Schema for tool specification."""
    
    name: str
    description: str
    parameters: Dict[str, Any]
    returns: Dict[str, Any]


class BaseTool(ABC):
    """Base class for all tools."""
    
    name: str
    description: str
    
    @abstractmethod
    async def run(self, **kwargs) -> Any:
        """Execute the tool."""
        pass
    
    @abstractmethod
    def get_schema(self) -> ToolSchema:
        """Get the tool's schema for function calling."""
        pass


class SearchWebTool(BaseTool):
    """Tool for web search."""
    
    name = "search_web"
    description = "Search the web for information"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    async def run(self, query: str, k: int = 5, recency_days: Optional[int] = None) -> List[Dict]:
        """Search the web and return results."""
        async with httpx.AsyncClient() as client:
            # This would call a real search API (Google, Bing, etc.)
            # For demo, return mock results
            return [
                {
                    "title": f"Result {i+1} for: {query}",
                    "snippet": f"This is a snippet about {query}...",
                    "url": f"https://example.com/{i}",
                    "score": 0.95 - i * 0.1,
                }
                for i in range(k)
            ]
    
    def get_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "k": {"type": "integer", "description": "Number of results", "default": 5},
                    "recency_days": {"type": "integer", "description": "Filter by recency"},
                },
                "required": ["query"],
            },
            returns={"type": "array", "items": {"type": "object"}},
        )


class WolframEvalTool(BaseTool):
    """Tool for Wolfram Language evaluation."""
    
    name = "wolfram_eval"
    description = "Evaluate expressions using Wolfram Language"
    
    def __init__(self, app_id: Optional[str] = None):
        self.app_id = app_id
    
    async def run(self, code: str, timeout_s: int = 30) -> Dict[str, Any]:
        """Evaluate Wolfram Language code."""
        if not self.app_id:
            # Fallback to SymPy
            return await self._sympy_fallback(code)
        
        async with httpx.AsyncClient(timeout=timeout_s) as client:
            # This would call Wolfram Cloud API
            # For demo, use SymPy fallback
            return await self._sympy_fallback(code)
    
    async def _sympy_fallback(self, code: str) -> Dict[str, Any]:
        """Fallback to SymPy for symbolic computation."""
        try:
            # Parse and evaluate with SymPy
            result = sp.sympify(code)
            return {
                "success": True,
                "result": str(result),
                "latex": sp.latex(result),
                "numeric": float(result.evalf()) if result.is_number else None,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "Wolfram Language code"},
                    "timeout_s": {"type": "integer", "description": "Timeout in seconds", "default": 30},
                },
                "required": ["code"],
            },
            returns={"type": "object"},
        )


class PythonSympyTool(BaseTool):
    """Tool for SymPy symbolic computation."""
    
    name = "python_sympy"
    description = "Perform symbolic mathematics using SymPy"
    
    async def run(self, code: str, timeout_s: int = 30) -> Dict[str, Any]:
        """Execute SymPy code."""
        try:
            # Create safe namespace
            namespace = {
                "sp": sp,
                "symbols": sp.symbols,
                "solve": sp.solve,
                "diff": sp.diff,
                "integrate": sp.integrate,
                "limit": sp.limit,
                "series": sp.series,
                "simplify": sp.simplify,
                "expand": sp.expand,
                "factor": sp.factor,
            }
            
            # Execute code
            exec(code, namespace)
            
            # Get result (assume last line assigns to 'result')
            result = namespace.get("result", "No result variable found")
            
            return {
                "success": True,
                "result": str(result),
                "latex": sp.latex(result) if hasattr(result, "__class__") else None,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "SymPy Python code"},
                    "timeout_s": {"type": "integer", "description": "Timeout in seconds", "default": 30},
                },
                "required": ["code"],
            },
            returns={"type": "object"},
        )


class UnitCheckTool(BaseTool):
    """Tool for dimensional analysis and unit checking."""
    
    name = "unit_check"
    description = "Check dimensional consistency and unit conversions"
    
    async def run(self, expression: str, expected_unit: Optional[str] = None) -> Dict[str, Any]:
        """Check units and dimensions."""
        try:
            import pint
            ureg = pint.UnitRegistry()
            
            # Parse expression
            quantity = ureg(expression)
            
            # Check against expected
            if expected_unit:
                expected = ureg(expected_unit)
                is_compatible = quantity.dimensionality == expected.dimensionality
                
                if is_compatible:
                    converted = quantity.to(expected_unit)
                    return {
                        "success": True,
                        "dimensional_ok": True,
                        "original": str(quantity),
                        "converted": str(converted),
                        "magnitude": converted.magnitude,
                    }
                else:
                    return {
                        "success": False,
                        "dimensional_ok": False,
                        "error": f"Incompatible dimensions: {quantity.dimensionality} vs {expected.dimensionality}",
                    }
            else:
                return {
                    "success": True,
                    "value": str(quantity),
                    "magnitude": quantity.magnitude,
                    "units": str(quantity.units),
                    "dimensionality": str(quantity.dimensionality),
                }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Expression with units"},
                    "expected_unit": {"type": "string", "description": "Expected unit"},
                },
                "required": ["expression"],
            },
            returns={"type": "object"},
        )


class PlotTool(BaseTool):
    """Tool for generating plots."""
    
    name = "plot"
    description = "Generate plots and visualizations"
    
    async def run(self, script_py: str) -> Dict[str, Any]:
        """Execute plotting script and return image."""
        try:
            import matplotlib
            matplotlib.use('Agg')  # Non-interactive backend
            import matplotlib.pyplot as plt
            import io
            import base64
            
            # Create namespace with common imports
            namespace = {
                "plt": plt,
                "np": np,
                "sp": sp,
            }
            
            # Execute plotting code
            exec(script_py, namespace)
            
            # Save plot to base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close('all')
            
            return {
                "success": True,
                "image": f"data:image/png;base64,{image_base64}",
                "format": "png",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_schema(self) -> ToolSchema:
        return ToolSchema(
            name=self.name,
            description=self.description,
            parameters={
                "type": "object",
                "properties": {
                    "script_py": {"type": "string", "description": "Python plotting script"},
                },
                "required": ["script_py"],
            },
            returns={"type": "object"},
        )


class ToolRegistry:
    """Registry for all available tools."""
    
    def __init__(self):
        self.tools: Dict[str, BaseTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default tools."""
        self.register(SearchWebTool())
        self.register(WolframEvalTool())
        self.register(PythonSympyTool())
        self.register(UnitCheckTool())
        self.register(PlotTool())
    
    def register(self, tool: BaseTool):
        """Register a tool."""
        self.tools[tool.name] = tool
        logger.info(f"Registered tool: {tool.name}")
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name."""
        return self.tools.get(name)
    
    def get_all_tools(self) -> List[BaseTool]:
        """Get all registered tools."""
        return list(self.tools.values())
    
    def get_schemas(self) -> List[ToolSchema]:
        """Get schemas for all tools."""
        return [tool.get_schema() for tool in self.tools.values()]
    
    async def run_tool(self, name: str, **kwargs) -> ToolCall:
        """Run a tool and return a ToolCall record."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool {name} not found")
        
        with timing_context() as timer:
            try:
                result = await tool.run(**kwargs)
                return ToolCall(
                    name=name,
                    args=kwargs,
                    result=result,
                    latency_ms=timer.elapsed_ms,
                )
            except Exception as e:
                return ToolCall(
                    name=name,
                    args=kwargs,
                    result={},
                    latency_ms=timer.elapsed_ms,
                    error=str(e),
                )
    
    async def initialize(self):
        """Initialize all tools."""
        logger.info("Initializing tool registry")
    
    async def cleanup(self):
        """Cleanup all tools."""
        logger.info("Cleaning up tool registry")