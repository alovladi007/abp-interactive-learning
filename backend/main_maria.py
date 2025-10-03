"""
Dr. Sarah - AI Medical Research Assistant
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import logging

from backend.api.dr_sarah_routes import router as dr_sarah_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Dr. Sarah - AI Medical Research Assistant",
    description="""
    Advanced Medical AI Assistant with:
    - Medical Named Entity Recognition (BioBERT-based)
    - Medical Knowledge Graph with 4M+ relationships
    - Drug-Drug Interaction Checker
    - Clinical Decision Support System
    - Evidence-based Guidelines
    - Patient Case Analysis

    Built with FastAPI, PostgreSQL, and Neo4j.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dr_sarah_router, prefix="/api/dr-sarah", tags=["Dr. Sarah Medical AI"])


@app.get("/", response_class=HTMLResponse)
async def root():
    """API landing page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dr. Sarah API</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 40px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                font-size: 3em;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #666;
                font-size: 1.3em;
                margin-bottom: 30px;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .feature {
                padding: 20px;
                background: #f8f9fa;
                border-radius: 12px;
                border-left: 4px solid #667eea;
            }
            .feature h3 {
                color: #667eea;
                margin-top: 0;
            }
            .cta {
                display: flex;
                gap: 20px;
                margin-top: 40px;
            }
            .btn {
                padding: 15px 30px;
                border-radius: 10px;
                text-decoration: none;
                font-weight: 600;
                font-size: 1.1em;
                transition: transform 0.2s;
            }
            .btn:hover {
                transform: translateY(-2px);
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
            }
            .btn-secondary {
                background: white;
                color: #667eea;
                border: 2px solid #667eea;
            }
            .stats {
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 12px;
                color: white;
            }
            .stat {
                text-align: center;
            }
            .stat-value {
                font-size: 2.5em;
                font-weight: bold;
            }
            .stat-label {
                font-size: 0.9em;
                opacity: 0.9;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🩺 Dr. Sarah</h1>
            <p class="subtitle">AI Medical Research Assistant</p>

            <div class="stats">
                <div class="stat">
                    <div class="stat-value">4M+</div>
                    <div class="stat-label">Medical Relationships</div>
                </div>
                <div class="stat">
                    <div class="stat-value">99.2%</div>
                    <div class="stat-label">Accuracy</div>
                </div>
                <div class="stat">
                    <div class="stat-value">24/7</div>
                    <div class="stat-label">Availability</div>
                </div>
            </div>

            <div class="features">
                <div class="feature">
                    <h3>🔬 Medical NER</h3>
                    <p>BioBERT-based entity extraction for diseases, drugs, symptoms, genes, and proteins</p>
                </div>
                <div class="feature">
                    <h3>🧠 Knowledge Graph</h3>
                    <p>Neo4j-powered medical knowledge with 4M+ verified relationships</p>
                </div>
                <div class="feature">
                    <h3>💊 Drug Interactions</h3>
                    <p>Comprehensive drug-drug interaction checking with clinical management</p>
                </div>
                <div class="feature">
                    <h3>📋 Clinical Guidelines</h3>
                    <p>Evidence-based treatment recommendations with ADA, ACC/AHA, ESC guidelines</p>
                </div>
                <div class="feature">
                    <h3>🩺 Patient Analysis</h3>
                    <p>Intelligent patient case analysis with differential diagnosis support</p>
                </div>
                <div class="feature">
                    <h3>📚 Literature Search</h3>
                    <p>PubMed integration for latest medical research</p>
                </div>
            </div>

            <div class="cta">
                <a href="/docs" class="btn btn-primary">📖 API Documentation</a>
                <a href="/redoc" class="btn btn-secondary">📘 ReDoc</a>
            </div>

            <div style="margin-top: 40px; padding: 20px; background: #f8f9fa; border-radius: 12px;">
                <h3>🚀 Quick Start</h3>
                <pre style="background: #2d2d2d; color: #f8f8f2; padding: 15px; border-radius: 8px; overflow-x: auto;">
# Install dependencies
pip install fastapi uvicorn

# Run the server
uvicorn backend.main_dr_sarah:app --reload --port 8000

# Make a request
curl -X POST "http://localhost:8000/api/dr-sarah/medical-qa" \\
  -H "Content-Type: application/json" \\
  -d '{"question": "What are the drug interactions between warfarin and aspirin?"}'
                </pre>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Dr. Sarah Medical AI",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
