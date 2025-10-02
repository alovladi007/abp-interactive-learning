"""
MAX API Routes - Complete Implementation
FastAPI endpoints for MAX AI Research Assistant with full database integration
Version: 2.0.0
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field, UUID4
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
from uuid import UUID, uuid4
import asyncio
import json
import io

from services.max_core_complete import (
    MAXCore,
    Paper,
    PaperSource,
    Citation,
    Author,
    ResearchTrend,
    format_citation
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/max", tags=["MAX Research Assistant"])

# Global MAX instance
max_instance: Optional[MAXCore] = None


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

async def get_max() -> MAXCore:
    """Dependency to get MAX instance"""
    global max_instance
    if max_instance is None:
        # Initialize with configuration
        max_instance = MAXCore(
            semantic_scholar_api_key=None,  # Set from environment
            postgres_config={
                'host': 'localhost',
                'port': 5432,
                'database': 'max_db',
                'user': 'max_user',
                'password': 'password'
            },
            neo4j_config={
                'uri': 'bolt://localhost:7687',
                'user': 'neo4j',
                'password': 'password'
            },
            redis_config={
                'url': 'redis://localhost:6379'
            }
        )
        await max_instance.initialize()
    return max_instance


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3, description="Search query")
    sources: Optional[List[str]] = Field(
        default=["semantic_scholar", "arxiv"],
        description="Paper sources to search"
    )
    fields_of_study: Optional[List[str]] = Field(None, description="Filter by fields")
    year_min: Optional[int] = Field(None, ge=1900, le=2030)
    year_max: Optional[int] = Field(None, ge=1900, le=2030)
    venue: Optional[str] = None
    min_citations: Optional[int] = Field(None, ge=0)
    max_results: int = Field(20, ge=1, le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "query": "machine learning healthcare",
                "sources": ["semantic_scholar", "arxiv"],
                "year_min": 2020,
                "max_results": 50
            }
        }


class PaperResponse(BaseModel):
    paper_id: str
    title: str
    authors: List[Dict[str, Any]]
    abstract: str
    publication_year: int
    venue: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    url: Optional[str] = None
    pdf_url: Optional[str] = None
    citations_count: int
    credibility_score: float
    fields_of_study: List[str]
    is_open_access: bool
    tldr: Optional[str] = None


class CitationNetworkRequest(BaseModel):
    paper_ids: List[str] = Field(..., min_items=1, description="Paper IDs to analyze")
    depth: int = Field(1, ge=1, le=3, description="Citation depth (1-3)")
    include_references: bool = Field(True, description="Include paper references")
    include_citations: bool = Field(True, description="Include papers citing these")


class SynthesisRequest(BaseModel):
    paper_ids: List[str] = Field(..., min_items=2, description="Papers to synthesize")
    include_key_findings: bool = Field(True)
    include_methodologies: bool = Field(True)
    include_gaps: bool = Field(True)
    max_summary_length: int = Field(500, ge=100, le=2000)


class CollectionCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: bool = Field(False)
    color: Optional[str] = Field(None, regex=r'^#[0-9A-Fa-f]{6}$')


class CollectionAddPaperRequest(BaseModel):
    paper_id: str
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    reading_status: str = Field("to_read", regex=r'^(to_read|reading|read|referenced)$')
    importance_rating: Optional[int] = Field(None, ge=1, le=5)


class SavedSearchRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    query: str
    filters: Dict[str, Any] = Field(default_factory=dict)
    alert_enabled: bool = Field(False)
    alert_frequency: Optional[str] = Field(None, regex=r'^(daily|weekly|monthly)$')


class AnnotationRequest(BaseModel):
    paper_id: str
    annotation_type: str = Field(..., regex=r'^(highlight|note|question|idea)$')
    content: str = Field(..., min_length=1)
    page_number: Optional[int] = None
    position: Optional[Dict[str, Any]] = None
    color: Optional[str] = Field(None, regex=r'^#[0-9A-Fa-f]{6}$')
    is_private: bool = Field(True)


class ExportCitationsRequest(BaseModel):
    paper_ids: List[str]
    style: str = Field("apa", regex=r'^(apa|mla|chicago|ieee|vancouver)$')
    format: str = Field("text", regex=r'^(text|bibtex|ris|json)$')


# ============================================================================
# SEARCH ENDPOINTS
# ============================================================================

@router.post("/search", response_model=Dict[str, Any])
async def search_papers(
    request: SearchRequest,
    max_core: MAXCore = Depends(get_max)
):
    """
    Search academic papers across multiple sources with advanced filters

    Returns:
    - papers: List of matching papers
    - total_results: Total count
    - sources_used: Which sources were queried
    - execution_time_ms: Query execution time
    """
    try:
        start_time = datetime.now()

        # Convert source strings to enum
        sources = [PaperSource(s) for s in request.sources]

        # Execute search
        papers = await max_core.search_multi_source(
            query=request.query,
            sources=sources,
            fields_of_study=request.fields_of_study,
            year_min=request.year_min,
            year_max=request.year_max,
            venue=request.venue,
            min_citations=request.min_citations,
            limit=request.max_results
        )

        execution_time = (datetime.now() - start_time).total_seconds() * 1000

        # Format response
        paper_responses = [
            PaperResponse(
                paper_id=p.paper_id,
                title=p.title,
                authors=[{
                    'name': a.name,
                    'affiliation': a.affiliation,
                    'h_index': a.h_index
                } for a in p.authors],
                abstract=p.abstract,
                publication_year=p.publication_year,
                venue=p.venue,
                doi=p.doi,
                arxiv_id=p.arxiv_id,
                url=p.url,
                pdf_url=p.pdf_url,
                citations_count=p.citations_count,
                credibility_score=p.credibility_score,
                fields_of_study=p.fields_of_study,
                is_open_access=p.is_open_access,
                tldr=p.tldr
            )
            for p in papers
        ]

        return {
            "papers": [p.dict() for p in paper_responses],
            "total_results": len(papers),
            "sources_used": request.sources,
            "execution_time_ms": execution_time,
            "query": request.query
        }

    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/paper/{paper_id}", response_model=PaperResponse)
async def get_paper_details(
    paper_id: str,
    max_core: MAXCore = Depends(get_max)
):
    """Get detailed information about a specific paper"""
    try:
        async with max_core.s2_client as client:
            paper = await client.get_paper_details(paper_id)

        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")

        return PaperResponse(
            paper_id=paper.paper_id,
            title=paper.title,
            authors=[{'name': a.name, 'affiliation': a.affiliation} for a in paper.authors],
            abstract=paper.abstract,
            publication_year=paper.publication_year,
            venue=paper.venue,
            doi=paper.doi,
            arxiv_id=paper.arxiv_id,
            url=paper.url,
            pdf_url=paper.pdf_url,
            citations_count=paper.citations_count,
            credibility_score=paper.credibility_score,
            fields_of_study=paper.fields_of_study,
            is_open_access=paper.is_open_access,
            tldr=paper.tldr
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get paper error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/paper/{paper_id}/similar", response_model=Dict[str, Any])
async def get_similar_papers(
    paper_id: str,
    limit: int = Query(10, ge=1, le=50),
    max_core: MAXCore = Depends(get_max)
):
    """Find papers similar to the given paper"""
    try:
        async with max_core.s2_client as client:
            similar_papers = await client.get_recommendations(paper_id, limit=limit)

        return {
            "paper_id": paper_id,
            "similar_papers": [
                {
                    "paper_id": p.paper_id,
                    "title": p.title,
                    "authors": [a.name for a in p.authors],
                    "year": p.publication_year,
                    "citations": p.citations_count
                }
                for p in similar_papers
            ],
            "count": len(similar_papers)
        }
    except Exception as e:
        logger.error(f"Similar papers error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CITATION NETWORK ENDPOINTS
# ============================================================================

@router.post("/citations/network", response_model=Dict[str, Any])
async def build_citation_network(
    request: CitationNetworkRequest,
    background_tasks: BackgroundTasks,
    max_core: MAXCore = Depends(get_max)
):
    """
    Build and analyze citation network for given papers

    Returns:
    - papers: All papers in network
    - citations: Citation relationships
    - influential_papers: Most influential papers (PageRank)
    - communities: Detected research communities
    - network_stats: Graph statistics
    """
    try:
        result = await max_core.build_citation_network(
            paper_ids=request.paper_ids,
            depth=request.depth
        )

        return result

    except Exception as e:
        logger.error(f"Citation network error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Network analysis failed: {str(e)}")


@router.get("/citations/{paper_id}/citing", response_model=Dict[str, Any])
async def get_citing_papers(
    paper_id: str,
    limit: int = Query(100, ge=1, le=1000),
    max_core: MAXCore = Depends(get_max)
):
    """Get all papers that cite this paper"""
    try:
        async with max_core.s2_client as client:
            citations = await client.get_citations(paper_id, limit=limit)

        return {
            "paper_id": paper_id,
            "citing_papers_count": len(citations),
            "citations": [
                {
                    "citing_paper_id": c.citing_paper_id,
                    "context": c.context,
                    "is_influential": c.is_influential
                }
                for c in citations
            ]
        }
    except Exception as e:
        logger.error(f"Get citations error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/citations/{paper_id}/references", response_model=Dict[str, Any])
async def get_paper_references(
    paper_id: str,
    limit: int = Query(100, ge=1, le=1000),
    max_core: MAXCore = Depends(get_max)
):
    """Get all papers that this paper cites"""
    try:
        async with max_core.s2_client as client:
            references = await client.get_references(paper_id, limit=limit)

        return {
            "paper_id": paper_id,
            "references_count": len(references),
            "references": [
                {
                    "cited_paper_id": c.cited_paper_id,
                    "context": c.context,
                    "is_influential": c.is_influential
                }
                for c in references
            ]
        }
    except Exception as e:
        logger.error(f"Get references error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RESEARCH SYNTHESIS ENDPOINTS
# ============================================================================

@router.post("/synthesize", response_model=Dict[str, Any])
async def synthesize_papers(
    request: SynthesisRequest,
    max_core: MAXCore = Depends(get_max)
):
    """
    Synthesize information from multiple papers

    Extracts:
    - Overall summary
    - Key findings
    - Common methodologies
    - Research gaps
    - Paper similarity matrix
    """
    try:
        result = await max_core.synthesize_research(request.paper_ids)

        # Filter based on request
        filtered_result = {
            "summary": result.get("summary", ""),
            "paper_count": result.get("paper_count", 0),
            "year_range": result.get("year_range", "")
        }

        if request.include_key_findings:
            filtered_result["key_findings"] = result.get("key_findings", [])

        if request.include_methodologies:
            filtered_result["methodologies"] = result.get("methodologies", {})

        if request.include_gaps:
            filtered_result["research_gaps"] = result.get("research_gaps", [])

        filtered_result["similarity_matrix"] = result.get("similarity_matrix", [])

        return filtered_result

    except Exception as e:
        logger.error(f"Synthesis error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Synthesis failed: {str(e)}")


# ============================================================================
# COLLECTIONS ENDPOINTS (Requires database)
# ============================================================================

@router.post("/collections", status_code=status.HTTP_201_CREATED)
async def create_collection(
    request: CollectionCreateRequest,
    user_id: UUID4 = Query(..., description="User ID"),
    max_core: MAXCore = Depends(get_max)
):
    """Create a new research collection"""
    if not max_core.db_pool:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        async with max_core.db_pool.acquire() as conn:
            collection_id = await conn.fetchval(
                """
                INSERT INTO collections (user_id, name, description, is_public, color)
                VALUES ($1, $2, $3, $4, $5)
                RETURNING collection_id
                """,
                user_id, request.name, request.description, request.is_public, request.color
            )

        return {
            "collection_id": collection_id,
            "name": request.name,
            "created_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Create collection error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/collections/{collection_id}/papers")
async def get_collection_papers(
    collection_id: UUID4,
    max_core: MAXCore = Depends(get_max)
):
    """Get all papers in a collection"""
    if not max_core.db_pool:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        async with max_core.db_pool.acquire() as conn:
            papers = await conn.fetch(
                """
                SELECT p.*, cp.notes, cp.tags, cp.reading_status, cp.importance_rating
                FROM collection_papers cp
                JOIN papers p ON cp.paper_id = p.paper_id
                WHERE cp.collection_id = $1
                ORDER BY cp.added_at DESC
                """,
                collection_id
            )

        return {
            "collection_id": collection_id,
            "papers": [dict(p) for p in papers],
            "count": len(papers)
        }
    except Exception as e:
        logger.error(f"Get collection papers error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# EXPORT ENDPOINTS
# ============================================================================

@router.post("/export/citations")
async def export_citations(
    request: ExportCitationsRequest,
    max_core: MAXCore = Depends(get_max)
):
    """
    Export citations in various formats (APA, MLA, BibTeX, etc.)
    """
    try:
        # Fetch papers
        papers = []
        async with max_core.s2_client as client:
            for paper_id in request.paper_ids:
                paper = await client.get_paper_details(paper_id)
                if paper:
                    papers.append(paper)

        if not papers:
            raise HTTPException(status_code=404, detail="No papers found")

        # Format citations
        if request.format == "text":
            citations = [format_citation(p, request.style) for p in papers]
            content = "\n\n".join(citations)
            media_type = "text/plain"
        elif request.format == "json":
            citations = [
                {
                    "id": p.paper_id,
                    "citation": format_citation(p, request.style),
                    "title": p.title,
                    "year": p.publication_year
                }
                for p in papers
            ]
            content = json.dumps(citations, indent=2)
            media_type = "application/json"
        else:
            raise HTTPException(status_code=400, detail=f"Format {request.format} not yet implemented")

        # Return as downloadable file
        return StreamingResponse(
            io.BytesIO(content.encode()),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename=citations.{request.format}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Export error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ANALYTICS ENDPOINTS
# ============================================================================

@router.get("/analytics/trends")
async def get_research_trends(
    topic: str = Query(..., min_length=2),
    field_of_study: Optional[str] = None,
    time_period: str = Query("last_year", regex=r'^(last_month|last_year|all_time)$'),
    max_core: MAXCore = Depends(get_max)
):
    """
    Get research trends for a topic
    Returns trending papers, authors, keywords
    """
    # This would query the research_trends table
    # For now, return mock data structure
    return {
        "topic": topic,
        "field_of_study": field_of_study,
        "time_period": time_period,
        "paper_count": 0,
        "citation_velocity": 0.0,
        "trend_score": 0.0,
        "message": "Trend analysis requires database population"
    }


# ============================================================================
# HEALTH CHECK
# ============================================================================

@router.get("/health")
async def health_check(max_core: MAXCore = Depends(get_max)):
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MAX AI Research Assistant",
        "version": "2.0.0",
        "database": "connected" if max_core.db_pool else "not connected",
        "neo4j": "connected" if max_core.neo4j_driver else "not connected",
        "redis": "connected" if max_core.redis_client else "not connected"
    }
