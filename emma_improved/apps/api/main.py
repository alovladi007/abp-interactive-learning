from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import sympy as sp

app = FastAPI(title="EMMA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolveRequest(BaseModel):
    question: str
    mode: str = "auto"

class SolveResponse(BaseModel):
    answer: str
    steps: List[Dict[str, Any]]

@app.get("/v1/health")
def health():
    return {"status": "healthy"}

@app.post("/v1/chat/solve")
async def solve(req: SolveRequest):
    # Simple symbolic solver
    try:
        if "integrate" in req.question.lower():
            x = sp.Symbol('x')
            expr = sp.sin(x)  # Example
            result = sp.integrate(expr, x)
            answer = f"∫sin(x)dx = {result}"
        else:
            answer = "Processing: " + req.question
        
        return SolveResponse(
            answer=answer,
            steps=[{"role": "solver", "action": "compute"}]
        )
    except Exception as e:
        return SolveResponse(answer=str(e), steps=[])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
