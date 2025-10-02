"""
MAX - AI Research Assistant
Combines Elicit, Semantic Scholar, Scispace, Scite.AI, Paperguide, Research Rabbit, Litmaps
Literature search, citation analysis, paper synthesis, and visualization
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional, Set, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging
import numpy as np
from collections import defaultdict
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PaperSource(Enum):
    """Academic paper sources"""
    SEMANTIC_SCHOLAR = "semantic_scholar"
    ARXIV = "arxiv"
    PUBMED = "pubmed"
    IEEE = "ieee"
    ACM = "acm"


class CitationType(Enum):
    """Types of citations"""
    SUPPORTING = "supporting"
    CONTRASTING = "contrasting"
    METHODOLOGICAL = "methodological"
    BACKGROUND = "background"


@dataclass
class Author:
    """Author information"""
    name: str
    author_id: Optional[str] = None
    affiliations: List[str] = field(default_factory=list)
    h_index: Optional[int] = None
    citation_count: Optional[int] = None


@dataclass
class Paper:
    """Academic paper representation"""
    paper_id: str
    title: str
    authors: List[Author]
    abstract: str
    year: int
    venue: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    pmid: Optional[str] = None
    pdf_url: Optional[str] = None
    citations_count: int = 0
    references_count: int = 0
    influential_citation_count: int = 0
    fields_of_study: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    embedding: Optional[np.ndarray] = None
    source: PaperSource = PaperSource.SEMANTIC_SCHOLAR
    credibility_score: float = 0.0


@dataclass
class Citation:
    """Citation relationship between papers"""
    citing_paper_id: str
    cited_paper_id: str
    citation_type: CitationType
    context: Optional[str] = None
    is_influential: bool = False


@dataclass
class SearchQuery:
    """Search query with filters"""
    query: str
    fields_of_study: Optional[List[str]] = None
    year_min: Optional[int] = None
    year_max: Optional[int] = None
    venue: Optional[str] = None
    author: Optional[str] = None
    min_citations: Optional[int] = None
    max_results: int = 20


@dataclass
class SearchResult:
    """Search results with metadata"""
    papers: List[Paper]
    total_results: int
    query: SearchQuery
    execution_time_ms: int
    refined_queries: List[str] = field(default_factory=list)


class SemanticScholarClient:
    """
    Client for Semantic Scholar API
    Free tier: 100 req/5min, unlimited with API key
    """

    def __init__(self, api_key: Optional[str] = None):
        self.base_url = "https://api.semanticscholar.org/graph/v1"
        self.api_key = api_key
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def search_papers(self, query: SearchQuery) -> List[Paper]:
        """Search papers using Semantic Scholar API"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        # Build query parameters
        params = {
            "query": query.query,
            "limit": min(query.max_results, 100),
            "fields": "paperId,title,abstract,authors,year,venue,citationCount,referenceCount,influentialCitationCount,fieldsOfStudy,externalIds"
        }

        if query.year_min:
            params["year"] = f"{query.year_min}-"
        if query.year_max and query.year_min:
            params["year"] = f"{query.year_min}-{query.year_max}"
        elif query.year_max:
            params["year"] = f"-{query.year_max}"

        if query.fields_of_study:
            params["fieldsOfStudy"] = ",".join(query.fields_of_study)

        url = f"{self.base_url}/paper/search"

        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    logger.error(f"Semantic Scholar API error: {response.status}")
                    return []

                data = await response.json()
                papers = self._parse_papers(data.get("data", []))
                return papers

        except Exception as e:
            logger.error(f"Error searching papers: {e}")
            return []

    async def get_paper_details(self, paper_id: str) -> Optional[Paper]:
        """Get detailed information about a specific paper"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        fields = "paperId,title,abstract,authors,year,venue,citationCount,referenceCount,influentialCitationCount,fieldsOfStudy,externalIds,embedding"
        url = f"{self.base_url}/paper/{paper_id}?fields={fields}"

        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    return None

                data = await response.json()
                papers = self._parse_papers([data])
                return papers[0] if papers else None

        except Exception as e:
            logger.error(f"Error fetching paper details: {e}")
            return None

    async def get_citations(self, paper_id: str, limit: int = 100) -> List[str]:
        """Get papers that cite this paper"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        url = f"{self.base_url}/paper/{paper_id}/citations?fields=paperId&limit={limit}"

        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    return []

                data = await response.json()
                return [item["citingPaper"]["paperId"] for item in data.get("data", [])]

        except Exception as e:
            logger.error(f"Error fetching citations: {e}")
            return []

    async def get_references(self, paper_id: str, limit: int = 100) -> List[str]:
        """Get papers referenced by this paper"""
        if not self.session:
            self.session = aiohttp.ClientSession()

        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        url = f"{self.base_url}/paper/{paper_id}/references?fields=paperId&limit={limit}"

        try:
            async with self.session.get(url, headers=headers) as response:
                if response.status != 200:
                    return []

                data = await response.json()
                return [item["citedPaper"]["paperId"] for item in data.get("data", [])]

        except Exception as e:
            logger.error(f"Error fetching references: {e}")
            return []

    def _parse_papers(self, data: List[Dict]) -> List[Paper]:
        """Parse Semantic Scholar API response to Paper objects"""
        papers = []

        for item in data:
            try:
                # Parse authors
                authors = []
                for author_data in item.get("authors", []):
                    author = Author(
                        name=author_data.get("name", "Unknown"),
                        author_id=author_data.get("authorId")
                    )
                    authors.append(author)

                # Parse external IDs
                external_ids = item.get("externalIds", {})

                paper = Paper(
                    paper_id=item["paperId"],
                    title=item.get("title", ""),
                    authors=authors,
                    abstract=item.get("abstract", ""),
                    year=item.get("year", 0),
                    venue=item.get("venue", ""),
                    doi=external_ids.get("DOI"),
                    arxiv_id=external_ids.get("ArXiv"),
                    pmid=external_ids.get("PubMed"),
                    citations_count=item.get("citationCount", 0),
                    references_count=item.get("referenceCount", 0),
                    influential_citation_count=item.get("influentialCitationCount", 0),
                    fields_of_study=item.get("fieldsOfStudy", []),
                    source=PaperSource.SEMANTIC_SCHOLAR
                )

                papers.append(paper)

            except Exception as e:
                logger.warning(f"Error parsing paper: {e}")
                continue

        return papers


class QueryRefiner:
    """
    AI-powered query refinement
    Expands and improves search queries
    """

    def __init__(self):
        self.synonyms = self._load_academic_synonyms()

    def _load_academic_synonyms(self) -> Dict[str, List[str]]:
        """Load domain-specific synonyms"""
        return {
            "machine learning": ["ML", "deep learning", "neural networks", "AI"],
            "artificial intelligence": ["AI", "machine learning", "cognitive computing"],
            "neural network": ["NN", "deep learning", "artificial neural network", "ANN"],
            "natural language processing": ["NLP", "text mining", "computational linguistics"],
            # Add more domain-specific synonyms
        }

    def refine_query(self, query: str) -> List[str]:
        """Generate refined query variations"""
        refined = [query]

        # Add synonym variations
        query_lower = query.lower()
        for term, synonyms in self.synonyms.items():
            if term in query_lower:
                for syn in synonyms[:2]:  # Limit to prevent explosion
                    refined.append(query.replace(term, syn))

        # Add boolean operators
        words = query.split()
        if len(words) > 1:
            # AND all terms
            refined.append(" AND ".join(words))
            # OR important terms
            if len(words) <= 3:
                refined.append(" OR ".join(words))

        return list(set(refined))[:5]  # Limit to 5 variations


class CitationAnalyzer:
    """
    Analyzes citation networks
    Identifies influential papers, supporting/contrasting evidence
    """

    def __init__(self):
        self.citation_graph = nx.DiGraph()

    def build_citation_network(self, papers: List[Paper], citations: List[Citation]):
        """Build NetworkX graph from papers and citations"""
        # Add nodes
        for paper in papers:
            self.citation_graph.add_node(
                paper.paper_id,
                title=paper.title,
                year=paper.year,
                citations=paper.citations_count
            )

        # Add edges
        for citation in citations:
            self.citation_graph.add_edge(
                citation.citing_paper_id,
                citation.cited_paper_id,
                type=citation.citation_type.value,
                influential=citation.is_influential
            )

    def find_influential_papers(self, top_n: int = 10) -> List[Tuple[str, float]]:
        """Find most influential papers using PageRank"""
        if len(self.citation_graph.nodes) == 0:
            return []

        pagerank = nx.pagerank(self.citation_graph)
        sorted_papers = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)
        return sorted_papers[:top_n]

    def find_research_clusters(self, min_cluster_size: int = 3) -> List[Set[str]]:
        """Identify research clusters/communities"""
        if len(self.citation_graph.nodes) < min_cluster_size:
            return []

        # Convert to undirected for community detection
        undirected = self.citation_graph.to_undirected()

        # Use greedy modularity
        communities = nx.community.greedy_modularity_communities(undirected)

        return [set(c) for c in communities if len(c) >= min_cluster_size]

    def calculate_credibility_score(self, paper: Paper) -> float:
        """Calculate paper credibility score"""
        score = 0.0

        # Citation count (normalized, max 40 points)
        citation_score = min(paper.citations_count / 100.0, 1.0) * 40
        score += citation_score

        # Influential citations (max 30 points)
        influential_score = min(paper.influential_citation_count / 20.0, 1.0) * 30
        score += influential_score

        # Venue quality (max 20 points) - simplified
        high_quality_venues = ["Nature", "Science", "Cell", "PNAS", "arXiv"]
        if any(venue in paper.venue for venue in high_quality_venues):
            score += 20
        elif paper.venue:
            score += 10

        # Author reputation (max 10 points) - would need author data
        if paper.authors:
            score += 5  # Placeholder

        return min(score, 100.0)


class PaperSynthesizer:
    """
    Synthesizes information from multiple papers
    Extracts key findings, methodologies, results
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100, stop_words='english')

    def extract_key_findings(self, papers: List[Paper], top_n: int = 5) -> List[str]:
        """Extract key findings from paper abstracts"""
        if not papers:
            return []

        # Use TF-IDF to find important sentences
        abstracts = [p.abstract for p in papers if p.abstract]
        if not abstracts:
            return []

        try:
            # Split into sentences
            all_sentences = []
            for abstract in abstracts:
                sentences = abstract.split('. ')
                all_sentences.extend(sentences)

            if len(all_sentences) < top_n:
                return all_sentences

            # Vectorize
            tfidf_matrix = self.vectorizer.fit_transform(all_sentences)

            # Calculate importance scores
            importance = np.asarray(tfidf_matrix.sum(axis=1)).flatten()

            # Get top sentences
            top_indices = importance.argsort()[-top_n:][::-1]
            key_findings = [all_sentences[i] for i in top_indices]

            return key_findings

        except Exception as e:
            logger.error(f"Error extracting key findings: {e}")
            return []

    def compare_methodologies(self, papers: List[Paper]) -> Dict[str, List[str]]:
        """Compare research methodologies across papers"""
        methodologies = defaultdict(list)

        for paper in papers:
            if not paper.abstract:
                continue

            abstract_lower = paper.abstract.lower()

            # Identify methodology keywords
            if any(word in abstract_lower for word in ["experiment", "trial", "study"]):
                methodologies["experimental"].append(paper.title)
            if any(word in abstract_lower for word in ["survey", "questionnaire", "interview"]):
                methodologies["survey"].append(paper.title)
            if any(word in abstract_lower for word in ["simulation", "model", "computational"]):
                methodologies["computational"].append(paper.title)
            if any(word in abstract_lower for word in ["review", "meta-analysis", "systematic"]):
                methodologies["review"].append(paper.title)

        return dict(methodologies)

    def synthesize_papers(self, papers: List[Paper]) -> Dict[str, Any]:
        """Generate comprehensive synthesis of papers"""
        return {
            "total_papers": len(papers),
            "year_range": (min(p.year for p in papers), max(p.year for p in papers)) if papers else (0, 0),
            "key_findings": self.extract_key_findings(papers),
            "methodologies": self.compare_methodologies(papers),
            "top_venues": self._get_top_venues(papers),
            "total_citations": sum(p.citations_count for p in papers),
            "fields_of_study": self._aggregate_fields(papers)
        }

    def _get_top_venues(self, papers: List[Paper], top_n: int = 5) -> List[Tuple[str, int]]:
        """Get most common publication venues"""
        venue_counts = defaultdict(int)
        for paper in papers:
            if paper.venue:
                venue_counts[paper.venue] += 1

        return sorted(venue_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def _aggregate_fields(self, papers: List[Paper]) -> List[Tuple[str, int]]:
        """Aggregate fields of study"""
        field_counts = defaultdict(int)
        for paper in papers:
            for field in paper.fields_of_study:
                field_counts[field] += 1

        return sorted(field_counts.items(), key=lambda x: x[1], reverse=True)


class MAXCore:
    """
    Main MAX orchestrator
    Combines search, citation analysis, and paper synthesis
    """

    def __init__(self, semantic_scholar_api_key: Optional[str] = None):
        self.ss_client = SemanticScholarClient(api_key=semantic_scholar_api_key)
        self.query_refiner = QueryRefiner()
        self.citation_analyzer = CitationAnalyzer()
        self.synthesizer = PaperSynthesizer()

    async def search(self, query: SearchQuery) -> SearchResult:
        """Main search interface"""
        start_time = datetime.now()

        async with self.ss_client:
            # Refine query
            refined_queries = self.query_refiner.refine_query(query.query)

            # Search with original query
            papers = await self.ss_client.search_papers(query)

            # Calculate credibility scores
            for paper in papers:
                paper.credibility_score = self.citation_analyzer.calculate_credibility_score(paper)

        execution_time = int((datetime.now() - start_time).total_seconds() * 1000)

        return SearchResult(
            papers=papers,
            total_results=len(papers),
            query=query,
            execution_time_ms=execution_time,
            refined_queries=refined_queries
        )

    async def build_citation_network(self, paper_ids: List[str]) -> Dict[str, Any]:
        """Build citation network for papers"""
        async with self.ss_client:
            # Get paper details
            papers = []
            for paper_id in paper_ids:
                paper = await self.ss_client.get_paper_details(paper_id)
                if paper:
                    papers.append(paper)

            # Get citations
            citations = []
            for paper in papers:
                citing_ids = await self.ss_client.get_citations(paper.paper_id, limit=50)
                for citing_id in citing_ids:
                    citation = Citation(
                        citing_paper_id=citing_id,
                        cited_paper_id=paper.paper_id,
                        citation_type=CitationType.BACKGROUND  # Default
                    )
                    citations.append(citation)

            # Build network
            self.citation_analyzer.build_citation_network(papers, citations)

            # Analyze
            influential = self.citation_analyzer.find_influential_papers()
            clusters = self.citation_analyzer.find_research_clusters()

            return {
                "papers": [p.paper_id for p in papers],
                "citations_count": len(citations),
                "influential_papers": influential,
                "research_clusters": [list(c) for c in clusters],
                "network_size": len(self.citation_analyzer.citation_graph.nodes)
            }

    async def synthesize(self, paper_ids: List[str]) -> Dict[str, Any]:
        """Synthesize information from multiple papers"""
        async with self.ss_client:
            papers = []
            for paper_id in paper_ids:
                paper = await self.ss_client.get_paper_details(paper_id)
                if paper:
                    papers.append(paper)

            synthesis = self.synthesizer.synthesize_papers(papers)
            return synthesis


# Example usage
async def main():
    max_core = MAXCore()

    # Search example
    query = SearchQuery(
        query="machine learning healthcare",
        year_min=2020,
        max_results=10
    )

    result = await max_core.search(query)
    print(f"Found {result.total_results} papers in {result.execution_time_ms}ms")

    for paper in result.papers[:3]:
        print(f"\n{paper.title}")
        print(f"  Authors: {', '.join([a.name for a in paper.authors[:3]])}")
        print(f"  Year: {paper.year}, Citations: {paper.citations_count}")
        print(f"  Credibility: {paper.credibility_score:.1f}/100")


if __name__ == "__main__":
    asyncio.run(main())
