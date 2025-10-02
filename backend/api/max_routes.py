"""
MAX API Routes
FastAPI endpoints for MAX AI Research Assistant
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from services.max_core import (
    MAXCore,
    SearchQuery,
    Paper,
    PaperSource
)

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/max", tags=["MAX"])

# Initialize MAX
max_instance = None


def get_max():
    """Dependency to get MAX instance"""
    global max_instance
    if max_instance is None:
        max_instance = MAXCore()
    return max_instance


# Pydantic models
class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    fields_of_study: Optional[List[str]] = Field(None, description="Filter by fields")
    year_min: Optional[int] = Field(None, ge=1900, le=2030)
    year_max: Optional[int] = Field(None, ge=1900, le=2030)
    venue: Optional[str] = None
    author: Optional[str] = None
    min_citations: Optional[int] = Field(None, ge=0)
    max_results: int = Field(20, ge=1, le=100)

    class Config:
        schema_extra = {
            "example": {
                "query": "machine learning healthcare",
                "year_min": 2020,
                "max_results": 20
            }
        }


class PaperResponse(BaseModel):
    paper_id: str
    title: str
    authors: List[str]
    abstract: str
    year: int
    venue: str
    citations_count: int
    credibility_score: float
    fields_of_study: List[str]
    doi: Optional[str]
    arxiv_id: Optional[str]
    pdf_url: Optional[str]


class CitationNetworkRequest(BaseModel):
    paper_ids: List[str] = Field(..., description="Paper IDs to analyze")
    max_depth: int = Field(1, ge=1, le=3, description="Citation depth")


class SynthesisRequest(BaseModel):
    paper_ids: List[str] = Field(..., description="Papers to synthesize")


class QueryRefineRequest(BaseModel):
    query: str = Field(..., description="Original query to refine")


# Endpoints
@router.post("/search")
async def search_papers(
    request: SearchRequest,
    max_core: MAXCore = Depends(get_max)
):
    """
    Search academic papers with advanced filters

    Returns papers matching the search criteria with credibility scores
    """
    try:
        # Create search query
        query = SearchQuery(
            query=request.query,
            fields_of_study=request.fields_of_study,
            year_min=request.year_min,
            year_max=request.year_max,
            venue=request.venue,
            author=request.author,
            min_citations=request.min_citations,
            max_results=request.max_results
        )

        # Execute search
        logger.info(f"Searching papers: {request.query}")
        result = await max_core.search(query)

        # Format response
        papers = []
        for paper in result.papers:
            papers.append(PaperResponse(
                paper_id=paper.paper_id,
                title=paper.title,
                authors=[a.name for a in paper.authors],
                abstract=paper.abstract,
                year=paper.year,
                venue=paper.venue,
                citations_count=paper.citations_count,
                credibility_score=paper.credibility_score,
                fields_of_study=paper.fields_of_study,
                doi=paper.doi,
                arxiv_id=paper.arxiv_id,
                pdf_url=paper.pdf_url
            ))

        return {
            "papers": papers,
            "total_results": result.total_results,
            "execution_time_ms": result.execution_time_ms,
            "refined_queries": result.refined_queries,
            "query": request.query
        }

    except Exception as e:
        logger.error(f"Search error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/paper/{paper_id}")
async def get_paper_details(
    paper_id: str,
    max_core: MAXCore = Depends(get_max)
):
    """Get detailed information about a specific paper"""
    try:
        async with max_core.ss_client:
            paper = await max_core.ss_client.get_paper_details(paper_id)

        if not paper:
            raise HTTPException(status_code=404, detail="Paper not found")

        return PaperResponse(
            paper_id=paper.paper_id,
            title=paper.title,
            authors=[a.name for a in paper.authors],
            abstract=paper.abstract,
            year=paper.year,
            venue=paper.venue,
            citations_count=paper.citations_count,
            credibility_score=max_core.citation_analyzer.calculate_credibility_score(paper),
            fields_of_study=paper.fields_of_study,
            doi=paper.doi,
            arxiv_id=paper.arxiv_id,
            pdf_url=paper.pdf_url
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching paper: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch paper details")


@router.post("/citations")
async def get_citation_network(
    request: CitationNetworkRequest,
    max_core: MAXCore = Depends(get_max)
):
    """
    Build and analyze citation network for papers

    Returns network statistics, influential papers, and research clusters
    """
    try:
        logger.info(f"Building citation network for {len(request.paper_ids)} papers")
        network = await max_core.build_citation_network(request.paper_ids)

        return {
            "paper_ids": network["papers"],
            "citations_count": network["citations_count"],
            "influential_papers": network["influential_papers"],
            "research_clusters": network["research_clusters"],
            "network_size": network["network_size"]
        }

    except Exception as e:
        logger.error(f"Citation network error: {e}")
        raise HTTPException(status_code=500, detail="Failed to build citation network")


@router.get("/citations/{paper_id}")
async def get_paper_citations(
    paper_id: str,
    limit: int = Query(50, ge=1, le=100),
    max_core: MAXCore = Depends(get_max)
):
    """Get papers that cite this paper"""
    try:
        async with max_core.ss_client:
            citing_ids = await max_core.ss_client.get_citations(paper_id, limit)

        return {
            "paper_id": paper_id,
            "citing_papers": citing_ids,
            "count": len(citing_ids)
        }

    except Exception as e:
        logger.error(f"Error fetching citations: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch citations")


@router.get("/references/{paper_id}")
async def get_paper_references(
    paper_id: str,
    limit: int = Query(50, ge=1, le=100),
    max_core: MAXCore = Depends(get_max)
):
    """Get papers referenced by this paper"""
    try:
        async with max_core.ss_client:
            reference_ids = await max_core.ss_client.get_references(paper_id, limit)

        return {
            "paper_id": paper_id,
            "references": reference_ids,
            "count": len(reference_ids)
        }

    except Exception as e:
        logger.error(f"Error fetching references: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch references")


@router.get("/similar/{paper_id}")
async def find_similar_papers(
    paper_id: str,
    limit: int = Query(10, ge=1, le=50),
    max_core: MAXCore = Depends(get_max)
):
    """Find papers similar to the given paper"""
    try:
        async with max_core.ss_client:
            # Get the paper details
            paper = await max_core.ss_client.get_paper_details(paper_id)

            if not paper:
                raise HTTPException(status_code=404, detail="Paper not found")

            # Search using paper title and keywords
            query = SearchQuery(
                query=paper.title,
                fields_of_study=paper.fields_of_study[:2] if paper.fields_of_study else None,
                max_results=limit + 1  # +1 to exclude original
            )

            result = await max_core.search(query)

            # Remove the original paper from results
            similar = [p for p in result.papers if p.paper_id != paper_id][:limit]

            return {
                "paper_id": paper_id,
                "similar_papers": [
                    PaperResponse(
                        paper_id=p.paper_id,
                        title=p.title,
                        authors=[a.name for a in p.authors],
                        abstract=p.abstract,
                        year=p.year,
                        venue=p.venue,
                        citations_count=p.citations_count,
                        credibility_score=p.credibility_score,
                        fields_of_study=p.fields_of_study,
                        doi=p.doi,
                        arxiv_id=p.arxiv_id,
                        pdf_url=p.pdf_url
                    )
                    for p in similar
                ],
                "count": len(similar)
            }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finding similar papers: {e}")
        raise HTTPException(status_code=500, detail="Failed to find similar papers")


@router.post("/synthesize")
async def synthesize_papers(
    request: SynthesisRequest,
    max_core: MAXCore = Depends(get_max)
):
    """
    Synthesize information from multiple papers

    Returns key findings, methodologies, and aggregated insights
    """
    try:
        logger.info(f"Synthesizing {len(request.paper_ids)} papers")
        synthesis = await max_core.synthesize(request.paper_ids)

        return {
            "total_papers": synthesis["total_papers"],
            "year_range": synthesis["year_range"],
            "key_findings": synthesis["key_findings"],
            "methodologies": synthesis["methodologies"],
            "top_venues": synthesis["top_venues"],
            "total_citations": synthesis["total_citations"],
            "fields_of_study": synthesis["fields_of_study"]
        }

    except Exception as e:
        logger.error(f"Synthesis error: {e}")
        raise HTTPException(status_code=500, detail="Failed to synthesize papers")


@router.post("/refine-query")
async def refine_query(
    request: QueryRefineRequest,
    max_core: MAXCore = Depends(get_max)
):
    """
    Get AI-powered query refinements

    Returns alternative query formulations with synonyms and operators
    """
    try:
        refined = max_core.query_refiner.refine_query(request.query)

        return {
            "original_query": request.query,
            "refined_queries": refined,
            "count": len(refined)
        }

    except Exception as e:
        logger.error(f"Query refinement error: {e}")
        raise HTTPException(status_code=500, detail="Failed to refine query")


@router.get("/trends/{topic}")
async def analyze_trends(
    topic: str,
    year_start: int = Query(2015, ge=1900, le=2030),
    year_end: int = Query(2024, ge=1900, le=2030),
    max_core: MAXCore = Depends(get_max)
):
    """
    Analyze research trends for a topic over time

    Returns publication counts and citation trends by year
    """
    try:
        # Search papers for each year
        trends = []

        for year in range(year_start, year_end + 1):
            query = SearchQuery(
                query=topic,
                year_min=year,
                year_max=year,
                max_results=100
            )

            result = await max_core.search(query)

            trends.append({
                "year": year,
                "paper_count": result.total_results,
                "total_citations": sum(p.citations_count for p in result.papers),
                "avg_citations": sum(p.citations_count for p in result.papers) / len(result.papers) if result.papers else 0
            })

        return {
            "topic": topic,
            "year_start": year_start,
            "year_end": year_end,
            "trends": trends
        }

    except Exception as e:
        logger.error(f"Trend analysis error: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze trends")


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "MAX",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/stats")
async def get_statistics():
    """Get platform statistics"""
    return {
        "service": "MAX Research Assistant",
        "version": "1.0.0",
        "features": [
            "Paper Search (Semantic Scholar)",
            "Citation Network Analysis",
            "Research Synthesis",
            "Query Refinement",
            "Trend Analysis",
            "Credibility Scoring"
        ],
        "data_sources": [
            "Semantic Scholar",
            "arXiv (via Semantic Scholar)",
            "PubMed (via Semantic Scholar)"
        ]
    }
