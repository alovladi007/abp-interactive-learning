"""Sandbox Runner Service - Secure code execution in Docker containers."""

import asyncio
import os
import tempfile
import tarfile
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

import docker
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import aiofiles

app = FastAPI(title="EMMA Sandbox Runner", version="1.0.0")

# Docker client
docker_client = docker.from_env()

# Configuration
SANDBOX_IMAGE = os.getenv("SANDBOX_IMAGE", "emma-sandbox-runtime")
MAX_TIMEOUT = int(os.getenv("MAX_SANDBOX_TIMEOUT", "60"))
MAX_MEMORY = os.getenv("MAX_SANDBOX_MEMORY", "512m")
MAX_CPU_SHARES = int(os.getenv("MAX_CPU_SHARES", "512"))


class SandboxRequest(BaseModel):
    """Request for sandbox execution."""
    
    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="Code to execute")
    files: Optional[List[Dict[str, str]]] = Field(
        default=None, description="Additional files"
    )
    stdin: Optional[str] = Field(None, description="Standard input")
    timeout: int = Field(30, ge=1, le=MAX_TIMEOUT)
    memory_mb: int = Field(512, ge=128, le=2048)
    cpu_shares: int = Field(512, ge=128, le=1024)
    env_vars: Optional[Dict[str, str]] = Field(
        default=None, description="Environment variables"
    )


class SandboxResponse(BaseModel):
    """Response from sandbox execution."""
    
    id: str
    status: str
    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: int
    files: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None


class SandboxRunner:
    """Manages secure code execution in Docker containers."""
    
    def __init__(self):
        self.docker = docker_client
        self._ensure_sandbox_image()
    
    def _ensure_sandbox_image(self):
        """Ensure sandbox image exists or build it."""
        try:
            self.docker.images.get(SANDBOX_IMAGE)
        except docker.errors.ImageNotFound:
            self._build_sandbox_image()
    
    def _build_sandbox_image(self):
        """Build the sandbox Docker image."""
        dockerfile = """
FROM python:3.11-slim

# Install additional runtimes
RUN apt-get update && apt-get install -y \
    gcc g++ make \
    nodejs npm \
    octave \
    firejail \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    numpy scipy matplotlib sympy pandas \
    networkx scikit-learn

# Install Node packages
RUN npm install -g \
    mathjs lodash axios

# Create sandbox user
RUN useradd -m -u 1000 -s /bin/bash sandbox && \
    mkdir -p /sandbox/work && \
    chown -R sandbox:sandbox /sandbox

# Security settings
USER sandbox
WORKDIR /sandbox/work

# Set resource limits
CMD ["/bin/bash"]
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.dockerfile') as f:
            f.write(dockerfile)
            f.flush()
            
            self.docker.images.build(
                path=os.path.dirname(f.name),
                dockerfile=os.path.basename(f.name),
                tag=SANDBOX_IMAGE,
                rm=True
            )
    
    async def execute(self, request: SandboxRequest) -> SandboxResponse:
        """Execute code in a sandboxed container."""
        run_id = str(uuid4())
        
        try:
            # Prepare execution environment
            work_dir = await self._prepare_workspace(run_id, request)
            
            # Configure container
            container_config = self._get_container_config(
                work_dir, request
            )
            
            # Run container
            start_time = asyncio.get_event_loop().time()
            container = self.docker.containers.run(
                **container_config,
                detach=True
            )
            
            # Wait for completion or timeout
            try:
                result = container.wait(timeout=request.timeout)
                execution_time = int(
                    (asyncio.get_event_loop().time() - start_time) * 1000
                )
            except Exception:
                container.kill()
                raise TimeoutError(f"Execution exceeded {request.timeout}s timeout")
            
            # Collect outputs
            stdout = container.logs(stdout=True, stderr=False).decode('utf-8')
            stderr = container.logs(stdout=False, stderr=True).decode('utf-8')
            exit_code = result['StatusCode']
            
            # Extract generated files
            files = await self._extract_files(container, work_dir)
            
            # Cleanup
            container.remove()
            
            return SandboxResponse(
                id=run_id,
                status="completed",
                stdout=stdout,
                stderr=stderr,
                exit_code=exit_code,
                execution_time_ms=execution_time,
                files=files
            )
            
        except Exception as e:
            return SandboxResponse(
                id=run_id,
                status="failed",
                stdout="",
                stderr=str(e),
                exit_code=-1,
                execution_time_ms=0,
                error=str(e)
            )
    
    async def _prepare_workspace(
        self, run_id: str, request: SandboxRequest
    ) -> Path:
        """Prepare workspace with code and files."""
        work_dir = Path(f"/tmp/sandbox_{run_id}")
        work_dir.mkdir(parents=True, exist_ok=True)
        
        # Determine file extension based on language
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "octave": "m",
            "cpp": "cpp",
            "java": "java",
        }
        ext = extensions.get(request.language, "txt")
        
        # Write main code file
        main_file = work_dir / f"main.{ext}"
        async with aiofiles.open(main_file, 'w') as f:
            await f.write(request.code)
        
        # Write additional files
        if request.files:
            for file_info in request.files:
                file_path = work_dir / file_info['name']
                file_path.parent.mkdir(parents=True, exist_ok=True)
                async with aiofiles.open(file_path, 'w') as f:
                    await f.write(file_info['content'])
        
        # Write stdin if provided
        if request.stdin:
            stdin_file = work_dir / "stdin.txt"
            async with aiofiles.open(stdin_file, 'w') as f:
                await f.write(request.stdin)
        
        return work_dir
    
    def _get_container_config(
        self, work_dir: Path, request: SandboxRequest
    ) -> Dict[str, Any]:
        """Get Docker container configuration."""
        # Select command based on language
        commands = {
            "python": ["python", "main.py"],
            "javascript": ["node", "main.js"],
            "typescript": ["npx", "ts-node", "main.ts"],
            "octave": ["octave", "--no-gui", "main.m"],
            "cpp": ["sh", "-c", "g++ -o main main.cpp && ./main"],
            "java": ["sh", "-c", "javac Main.java && java Main"],
        }
        
        command = commands.get(request.language, ["cat", "main.txt"])
        
        # Add stdin redirection if provided
        if request.stdin:
            command = ["sh", "-c", f"{' '.join(command)} < stdin.txt"]
        
        # Container configuration
        config = {
            "image": SANDBOX_IMAGE,
            "command": command,
            "volumes": {
                str(work_dir): {
                    "bind": "/sandbox/work",
                    "mode": "rw"
                }
            },
            "working_dir": "/sandbox/work",
            "mem_limit": f"{request.memory_mb}m",
            "memswap_limit": f"{request.memory_mb}m",
            "cpu_shares": request.cpu_shares,
            "network_mode": "none",  # No network access
            "read_only": False,  # Need write for output files
            "security_opt": ["no-new-privileges"],
            "cap_drop": ["ALL"],  # Drop all capabilities
            "environment": request.env_vars or {},
            "user": "sandbox",
        }
        
        return config
    
    async def _extract_files(
        self, container: docker.models.containers.Container,
        work_dir: Path
    ) -> List[Dict[str, Any]]:
        """Extract generated files from container."""
        files = []
        
        try:
            # Get tar archive from container
            tar_stream, _ = container.get_archive("/sandbox/work")
            
            # Extract to temp directory
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in tar_stream:
                    tmp.write(chunk)
                tmp_path = tmp.name
            
            # Process tar file
            with tarfile.open(tmp_path, 'r') as tar:
                for member in tar.getmembers():
                    if member.isfile():
                        # Skip input files
                        if member.name in ['work/main.py', 'work/stdin.txt']:
                            continue
                        
                        # Extract file content
                        f = tar.extractfile(member)
                        if f:
                            content = f.read()
                            
                            # Determine if binary or text
                            try:
                                text_content = content.decode('utf-8')
                                files.append({
                                    "name": os.path.basename(member.name),
                                    "content": text_content,
                                    "size": member.size,
                                    "type": "text"
                                })
                            except UnicodeDecodeError:
                                # Binary file - encode as base64
                                import base64
                                b64_content = base64.b64encode(content).decode('utf-8')
                                files.append({
                                    "name": os.path.basename(member.name),
                                    "content": b64_content,
                                    "size": member.size,
                                    "type": "binary",
                                    "encoding": "base64"
                                })
            
            # Cleanup
            os.unlink(tmp_path)
            
        except Exception as e:
            print(f"Error extracting files: {e}")
        
        return files


# Global runner instance
runner = SandboxRunner()


@app.post("/execute", response_model=SandboxResponse)
async def execute_code(request: SandboxRequest) -> SandboxResponse:
    """Execute code in sandbox."""
    return await runner.execute(request)


@app.post("/execute/files", response_model=SandboxResponse)
async def execute_with_files(
    code: str,
    language: str,
    files: List[UploadFile] = File(None),
    timeout: int = 30,
) -> SandboxResponse:
    """Execute code with uploaded files."""
    # Process uploaded files
    file_contents = []
    if files:
        for file in files:
            content = await file.read()
            file_contents.append({
                "name": file.filename,
                "content": content.decode('utf-8')
            })
    
    request = SandboxRequest(
        language=language,
        code=code,
        files=file_contents,
        timeout=timeout
    )
    
    return await runner.execute(request)


@app.get("/languages")
async def get_supported_languages() -> Dict[str, List[str]]:
    """Get list of supported languages."""
    return {
        "languages": [
            "python",
            "javascript",
            "typescript",
            "octave",
            "cpp",
            "java"
        ]
    }


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    try:
        # Check Docker connection
        docker_client.ping()
        return {"status": "healthy", "service": "sandbox"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)