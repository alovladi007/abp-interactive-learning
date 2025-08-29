"""
Sandbox Runner for safe code execution
"""
from fastapi import FastAPI
from pydantic import BaseModel
import tempfile
import subprocess
import os
import resource
import signal

app = FastAPI(title="EMMA Sandbox Runner")

class RunRequest(BaseModel):
    language: str = "python"
    code: str

def limit_resources():
    """Set resource limits for safety."""
    # CPU limit: 2 seconds
    resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
    # Memory limit: 128MB
    mem = 128 * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem, mem))

@app.post("/run")
def run_code(req: RunRequest):
    if req.language != "python":
        return {"error": "Only python supported in dev sandbox"}
    
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "main.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(req.code)
        
        try:
            proc = subprocess.run(
                ["python", "-S", "-B", path],
                capture_output=True,
                text=True,
                timeout=3,
                preexec_fn=limit_resources
            )
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "returncode": proc.returncode
            }
        except subprocess.TimeoutExpired:
            return {"error": "timeout"}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
