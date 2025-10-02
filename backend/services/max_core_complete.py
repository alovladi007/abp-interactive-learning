"""
MAX - AI Research Assistant (Complete Implementation)
Combines: Semantic Scholar, Elicit, Scispace, Scite.AI, Paperguide, Research Rabbit, Litmaps
Full-stack research management with citation analysis, synthesis, and collaboration
Version: 2.0.0
"""

import aiohttp
import asyncio
import networkx as nx
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from enum import Enum
import logging
import json
import hashlib
from collections import defaultdict, Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import asyncpg
from neo4j import AsyncGraphDatabase
import redis.asyncio as redis
from sentence_transformers import SentenceTransformer
import xml.etree.ElementTree as ET
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS & DATA CLASSES
# ============================================================================

class PaperSource(Enum):
    """Sources for academic papers"""
    SEMANTIC_SCHOLAR = "semantic_scholar"
    ARXIV = "arxiv"
    PUBMED = "pubmed"
    CROSSREF = "crossref"
    SCISPACE = "scispace"
    OPEN_ALEX = "openalex"
    GOOGLE_SCHOLAR = "google_scholar"


class CitationIntent(Enum):
    """Types of citation intents"""
    BACKGROUND = "background"
    METHOD = "method"
    RESULT_COMPARISON = "result_comparison"
    EXTENSION = "extension"
    CRITICISM = "criticism"
    FUTURE_WORK = "future_work"


@dataclass
class Author:
    """Academic author information"""
    name: str
    author_id: Optional[str] = None
    affiliation: Optional[str] = None
    orcid: Optional[str] = None
    google_scholar_id: Optional[str] = None
    h_index: Optional[int] = None
    total_citations: Optional[int] = None
    email: Optional[str] = None


@dataclass
class Paper:
    """Complete paper metadata"""
    paper_id: str
    title: str
    abstract: str
    authors: List[Author]
    publication_year: int
    venue: str
    source: PaperSource
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    pubmed_id: Optional[str] = None
    url: Optional[str] = None
    pdf_url: Optional[str] = None
    citations_count: int = 0
    references_count: int = 0
    influential_citation_count: int = 0
    fields_of_study: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    credibility_score: float = 0.0
    tldr: Optional[str] = None
    is_open_access: bool = False
    embedding: Optional[List[float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Citation:
    """Citation relationship between papers"""
    citing_paper_id: str
    cited_paper_id: str
    context: Optional[str] = None
    intent: Optional[CitationIntent] = None
    is_influential: bool = False


@dataclass
class ResearchTrend:
    """Research trend analysis"""
    topic: str
    field_of_study: str
    paper_count: int
    citation_velocity: float
    top_papers: List[str]
    top_authors: List[str]
    emerging_keywords: List[str]
    trend_score: float
    time_period: str


# ============================================================================
# API CLIENTS
# ============================================================================

class SemanticScholarClient:
    """
    Enhanced Semantic Scholar API client
    Handles rate limiting, caching, and batch requests
    """

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None
        self.rate_limit_delay = 0.1  # 10 requests per second
        self.last_request_time = 0

    async def __aenter__(self):
        headers = {}
        if self.api_key:
            headers['x-api-key'] = self.api_key
        self.session = aiohttp.ClientSession(headers=headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _rate_limit(self):
        """Enforce rate limiting"""
        now = asyncio.get_event_loop().time()
        time_since_last = now - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            await asyncio.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = asyncio.get_event_loop().time()

    async def search_papers(
        self,
        query: str,
        fields_of_study: Optional[List[str]] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None,
        venue: Optional[str] = None,
        min_citations: Optional[int] = None,
        limit: int = 100
    ) -> List[Paper]:
        """
        Search for papers with advanced filters
        """
        await self._rate_limit()

        # Build query string
        query_parts = [query]
        if year_min:
            query_parts.append(f"year:{year_min}-")
        if year_max:
            query_parts.append(f"year:-{year_max}")
        if venue:
            query_parts.append(f"venue:{venue}")
        if min_citations:
            query_parts.append(f"citations:{min_citations}-")

        full_query = " ".join(query_parts)

        params = {
            'query': full_query,
            'limit': min(limit, 100),
            'fields': 'paperId,title,abstract,authors,year,venue,citationCount,referenceCount,influentialCitationCount,fieldsOfStudy,openAccessPdf,citationStyles,tldr'
        }

        if fields_of_study:
            params['fieldsOfStudy'] = ','.join(fields_of_study)

        try:
            async with self.session.get(f"{self.BASE_URL}/paper/search", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [self._parse_paper(item) for item in data.get('data', [])]
                elif response.status == 429:
                    logger.warning("Rate limit exceeded, waiting...")
                    await asyncio.sleep(60)
                    return await self.search_papers(query, fields_of_study, year_min, year_max, venue, min_citations, limit)
                else:
                    logger.error(f"Search failed: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []

    async def get_paper_details(self, paper_id: str) -> Optional[Paper]:
        """Get detailed information about a specific paper"""
        await self._rate_limit()

        params = {
            'fields': 'paperId,title,abstract,authors,year,venue,citationCount,referenceCount,influentialCitationCount,fieldsOfStudy,openAccessPdf,embedding,tldr'
        }

        try:
            async with self.session.get(f"{self.BASE_URL}/paper/{paper_id}", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_paper(data)
                return None
        except Exception as e:
            logger.error(f"Get paper error: {e}")
            return None

    async def get_citations(self, paper_id: str, limit: int = 1000) -> List[Citation]:
        """Get all papers that cite this paper"""
        await self._rate_limit()

        params = {
            'fields': 'paperId,title,contexts,intents,isInfluential',
            'limit': min(limit, 1000)
        }

        citations = []
        try:
            async with self.session.get(f"{self.BASE_URL}/paper/{paper_id}/citations", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    for item in data.get('data', []):
                        citing_paper = item.get('citingPaper', {})
                        citations.append(Citation(
                            citing_paper_id=citing_paper.get('paperId'),
                            cited_paper_id=paper_id,
                            context=item.get('contexts', [None])[0],
                            intent=CitationIntent(item['intents'][0]) if item.get('intents') else None,
                            is_influential=item.get('isInfluential', False)
                        ))
            return citations
        except Exception as e:
            logger.error(f"Get citations error: {e}")
            return []

    async def get_references(self, paper_id: str, limit: int = 1000) -> List[Citation]:
        """Get all papers that this paper cites"""
        await self._rate_limit()

        params = {
            'fields': 'paperId,title,contexts,intents,isInfluential',
            'limit': min(limit, 1000)
        }

        references = []
        try:
            async with self.session.get(f"{self.BASE_URL}/paper/{paper_id}/references", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    for item in data.get('data', []):
                        cited_paper = item.get('citedPaper', {})
                        references.append(Citation(
                            citing_paper_id=paper_id,
                            cited_paper_id=cited_paper.get('paperId'),
                            context=item.get('contexts', [None])[0],
                            intent=CitationIntent(item['intents'][0]) if item.get('intents') else None,
                            is_influential=item.get('isInfluential', False)
                        ))
            return references
        except Exception as e:
            logger.error(f"Get references error: {e}")
            return []

    async def get_recommendations(self, paper_id: str, limit: int = 10) -> List[Paper]:
        """Get recommended papers based on content similarity"""
        await self._rate_limit()

        params = {
            'fields': 'paperId,title,abstract,authors,year,venue,citationCount',
            'limit': limit
        }

        try:
            async with self.session.get(f"{self.BASE_URL}/recommendations/v1/papers/forpaper/{paper_id}", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [self._parse_paper(item) for item in data.get('recommendedPapers', [])]
                return []
        except Exception as e:
            logger.error(f"Get recommendations error: {e}")
            return []

    def _parse_paper(self, data: Dict) -> Paper:
        """Parse Semantic Scholar API response into Paper object"""
        authors = [
            Author(
                name=a.get('name', ''),
                author_id=a.get('authorId'),
                affiliation=a.get('affiliations', [None])[0] if a.get('affiliations') else None
            )
            for a in data.get('authors', [])
        ]

        pdf_url = None
        if data.get('openAccessPdf'):
            pdf_url = data['openAccessPdf'].get('url')

        return Paper(
            paper_id=data.get('paperId', ''),
            title=data.get('title', ''),
            abstract=data.get('abstract', ''),
            authors=authors,
            publication_year=data.get('year', 0),
            venue=data.get('venue', ''),
            source=PaperSource.SEMANTIC_SCHOLAR,
            doi=data.get('externalIds', {}).get('DOI'),
            arxiv_id=data.get('externalIds', {}).get('ArXiv'),
            pubmed_id=data.get('externalIds', {}).get('PubMed'),
            url=f"https://www.semanticscholar.org/paper/{data.get('paperId')}",
            pdf_url=pdf_url,
            citations_count=data.get('citationCount', 0),
            references_count=data.get('referenceCount', 0),
            influential_citation_count=data.get('influentialCitationCount', 0),
            fields_of_study=data.get('fieldsOfStudy', []),
            is_open_access=bool(pdf_url),
            tldr=data.get('tldr', {}).get('text') if data.get('tldr') else None,
            embedding=data.get('embedding', {}).get('vector') if data.get('embedding') else None
        )


class ArXivClient:
    """
    ArXiv API client for preprints
    """

    BASE_URL = "http://export.arxiv.org/api/query"

    async def search_papers(
        self,
        query: str,
        category: Optional[str] = None,
        max_results: int = 100
    ) -> List[Paper]:
        """Search ArXiv for papers"""
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }

        if category:
            params['search_query'] += f' AND cat:{category}'

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(self.BASE_URL, params=params) as response:
                    if response.status == 200:
                        xml_data = await response.text()
                        return self._parse_arxiv_response(xml_data)
                    return []
            except Exception as e:
                logger.error(f"ArXiv search error: {e}")
                return []

    def _parse_arxiv_response(self, xml_data: str) -> List[Paper]:
        """Parse ArXiv XML response"""
        papers = []
        root = ET.fromstring(xml_data)

        for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
            title = entry.find('{http://www.w3.org/2005/Atom}title').text
            summary = entry.find('{http://www.w3.org/2005/Atom}summary').text
            arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text.split('/abs/')[-1]
            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            year = int(published.split('-')[0])

            authors = [
                Author(name=a.find('{http://www.w3.org/2005/Atom}name').text)
                for a in entry.findall('{http://www.w3.org/2005/Atom}author')
            ]

            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

            papers.append(Paper(
                paper_id=arxiv_id,
                title=title.strip(),
                abstract=summary.strip(),
                authors=authors,
                publication_year=year,
                venue="arXiv",
                source=PaperSource.ARXIV,
                arxiv_id=arxiv_id,
                url=f"https://arxiv.org/abs/{arxiv_id}",
                pdf_url=pdf_url,
                is_open_access=True
            ))

        return papers


# ============================================================================
# CITATION ANALYSIS ENGINE
# ============================================================================

class CitationNetworkAnalyzer:
    """
    Advanced citation network analysis using NetworkX and graph algorithms
    Identifies influential papers, communities, and research trends
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self.embedding_model = SentenceTransformer('allenai-specter')

    def build_network(self, papers: List[Paper], citations: List[Citation]):
        """Build citation network from papers and citations"""
        # Add nodes
        for paper in papers:
            self.graph.add_node(
                paper.paper_id,
                title=paper.title,
                year=paper.publication_year,
                citations=paper.citations_count,
                venue=paper.venue
            )

        # Add edges
        for citation in citations:
            if citation.citing_paper_id in self.graph and citation.cited_paper_id in self.graph:
                self.graph.add_edge(
                    citation.citing_paper_id,
                    citation.cited_paper_id,
                    influential=citation.is_influential
                )

    def compute_pagerank(self) -> Dict[str, float]:
        """Compute PageRank scores for all papers"""
        return nx.pagerank(self.graph, alpha=0.85)

    def compute_betweenness_centrality(self) -> Dict[str, float]:
        """Find papers that bridge different research areas"""
        return nx.betweenness_centrality(self.graph)

    def detect_communities(self, algorithm: str = 'louvain') -> Dict[str, int]:
        """
        Detect research communities
        Returns mapping of paper_id to community_id
        """
        # Convert to undirected for community detection
        undirected = self.graph.to_undirected()

        if algorithm == 'louvain':
            import community as community_louvain
            return community_louvain.best_partition(undirected)
        elif algorithm == 'label_propagation':
            communities = nx.algorithms.community.label_propagation_communities(undirected)
            result = {}
            for idx, community in enumerate(communities):
                for node in community:
                    result[node] = idx
            return result
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def find_influential_papers(self, top_n: int = 20) -> List[Tuple[str, float]]:
        """Find most influential papers using multiple metrics"""
        pagerank = self.compute_pagerank()
        betweenness = self.compute_betweenness_centrality()

        # Combine scores
        combined_scores = {}
        for paper_id in self.graph.nodes():
            pr_score = pagerank.get(paper_id, 0)
            bt_score = betweenness.get(paper_id, 0)
            citations = self.graph.nodes[paper_id].get('citations', 0)

            # Weighted combination
            combined_scores[paper_id] = (
                0.4 * pr_score +
                0.3 * bt_score +
                0.3 * (citations / max(citations, 1))
            )

        return sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    def find_citation_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        """Find shortest citation path between two papers"""
        try:
            return nx.shortest_path(self.graph, source_id, target_id)
        except nx.NetworkXNoPath:
            return None

    def get_co_citation_clusters(self, min_co_citations: int = 3) -> List[Set[str]]:
        """
        Find papers that are frequently cited together
        Useful for identifying related work
        """
        co_citation_graph = nx.Graph()

        # Build co-citation graph
        for node in self.graph.nodes():
            citing_papers = list(self.graph.predecessors(node))

            for i, p1 in enumerate(citing_papers):
                for p2 in citing_papers[i+1:]:
                    if co_citation_graph.has_edge(p1, p2):
                        co_citation_graph[p1][p2]['weight'] += 1
                    else:
                        co_citation_graph.add_edge(p1, p2, weight=1)

        # Filter by minimum co-citations
        edges_to_remove = [
            (u, v) for u, v, d in co_citation_graph.edges(data=True)
            if d['weight'] < min_co_citations
        ]
        co_citation_graph.remove_edges_from(edges_to_remove)

        # Find connected components (clusters)
        return list(nx.connected_components(co_citation_graph))


# ============================================================================
# RESEARCH SYNTHESIS ENGINE
# ============================================================================

class PaperSynthesizer:
    """
    Synthesize information from multiple papers
    Extract key findings, methodologies, and identify research gaps
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )

    def extract_key_findings(
        self,
        papers: List[Paper],
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Extract most important findings across papers using TF-IDF
        """
        if not papers:
            return []

        # Combine abstracts
        texts = [f"{p.title}. {p.abstract}" for p in papers if p.abstract]

        if not texts:
            return []

        # Compute TF-IDF
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        feature_names = self.vectorizer.get_feature_names_out()

        # Get top terms for each paper
        findings = []
        for idx, paper in enumerate(papers):
            if idx >= len(texts):
                continue

            tfidf_scores = tfidf_matrix[idx].toarray()[0]
            top_indices = tfidf_scores.argsort()[-top_k:][::-1]
            top_terms = [feature_names[i] for i in top_indices if tfidf_scores[i] > 0]

            if top_terms:
                findings.append({
                    'paper_id': paper.paper_id,
                    'title': paper.title,
                    'key_terms': top_terms,
                    'year': paper.publication_year,
                    'citations': paper.citations_count
                })

        return findings

    def identify_methodologies(self, papers: List[Paper]) -> Dict[str, List[str]]:
        """
        Identify common methodologies used across papers
        """
        method_keywords = [
            'method', 'approach', 'technique', 'algorithm', 'model',
            'framework', 'system', 'experiment', 'analysis', 'evaluation'
        ]

        methodologies = defaultdict(list)

        for paper in papers:
            if not paper.abstract:
                continue

            text = paper.abstract.lower()

            for keyword in method_keywords:
                if keyword in text:
                    # Extract sentence containing the keyword
                    sentences = text.split('.')
                    for sentence in sentences:
                        if keyword in sentence:
                            methodologies[keyword].append({
                                'paper_id': paper.paper_id,
                                'title': paper.title,
                                'snippet': sentence.strip()
                            })
                            break

        return dict(methodologies)

    def identify_research_gaps(
        self,
        papers: List[Paper],
        future_work_keywords: List[str] = None
    ) -> List[str]:
        """
        Identify potential research gaps mentioned in papers
        """
        if future_work_keywords is None:
            future_work_keywords = [
                'future work', 'future research', 'limitation', 'challenge',
                'open problem', 'remains unclear', 'further investigation',
                'yet to be', 'unexplored'
            ]

        gaps = []

        for paper in papers:
            if not paper.abstract:
                continue

            text = paper.abstract.lower()
            sentences = text.split('.')

            for sentence in sentences:
                for keyword in future_work_keywords:
                    if keyword in sentence:
                        gaps.append(sentence.strip())
                        break

        return list(set(gaps))  # Remove duplicates

    def compute_paper_similarity(self, papers: List[Paper]) -> np.ndarray:
        """
        Compute pairwise similarity between papers
        Returns similarity matrix
        """
        if len(papers) < 2:
            return np.array([[]])

        texts = [f"{p.title}. {p.abstract}" for p in papers if p.abstract]

        if len(texts) < 2:
            return np.array([[]])

        tfidf_matrix = self.vectorizer.fit_transform(texts)
        return cosine_similarity(tfidf_matrix)

    def generate_synthesis_summary(
        self,
        papers: List[Paper],
        max_length: int = 500
    ) -> str:
        """
        Generate a synthesis summary from multiple papers
        """
        if not papers:
            return ""

        # Extract key information
        findings = self.extract_key_findings(papers, top_k=5)
        methodologies = self.identify_methodologies(papers)
        gaps = self.identify_research_gaps(papers)

        # Build summary
        summary_parts = []

        # Overview
        summary_parts.append(
            f"This synthesis covers {len(papers)} papers "
            f"published between {min(p.publication_year for p in papers)} "
            f"and {max(p.publication_year for p in papers)}. "
        )

        # Key findings
        if findings:
            top_terms = set()
            for f in findings[:5]:
                top_terms.update(f['key_terms'][:3])
            summary_parts.append(
                f"Key topics include: {', '.join(list(top_terms)[:10])}. "
            )

        # Methodologies
        if methodologies:
            common_methods = sorted(methodologies.items(), key=lambda x: len(x[1]), reverse=True)
            summary_parts.append(
                f"Common methodologies: {', '.join(m[0] for m in common_methods[:5])}. "
            )

        # Research gaps
        if gaps:
            summary_parts.append(
                f"Identified research gaps include: {gaps[0][:100]}... "
            )

        summary = ' '.join(summary_parts)

        # Truncate if too long
        if len(summary) > max_length:
            summary = summary[:max_length] + "..."

        return summary


# ============================================================================
# MAIN MAX CORE CLASS
# ============================================================================

class MAXCore:
    """
    Complete MAX AI Research Assistant
    Orchestrates all components: search, analysis, synthesis, collaboration
    """

    def __init__(
        self,
        semantic_scholar_api_key: Optional[str] = None,
        postgres_config: Optional[Dict] = None,
        neo4j_config: Optional[Dict] = None,
        redis_config: Optional[Dict] = None
    ):
        self.s2_client = SemanticScholarClient(semantic_scholar_api_key)
        self.arxiv_client = ArXivClient()
        self.citation_analyzer = CitationNetworkAnalyzer()
        self.synthesizer = PaperSynthesizer()

        # Database connections
        self.postgres_config = postgres_config
        self.neo4j_config = neo4j_config
        self.redis_config = redis_config

        self.db_pool: Optional[asyncpg.Pool] = None
        self.neo4j_driver = None
        self.redis_client: Optional[redis.Redis] = None

    async def initialize(self):
        """Initialize database connections"""
        # PostgreSQL
        if self.postgres_config:
            self.db_pool = await asyncpg.create_pool(**self.postgres_config)

        # Neo4j
        if self.neo4j_config:
            self.neo4j_driver = AsyncGraphDatabase.driver(
                self.neo4j_config['uri'],
                auth=(self.neo4j_config['user'], self.neo4j_config['password'])
            )

        # Redis
        if self.redis_config:
            self.redis_client = await redis.from_url(
                self.redis_config['url'],
                encoding="utf-8",
                decode_responses=True
            )

    async def close(self):
        """Close all connections"""
        if self.db_pool:
            await self.db_pool.close()
        if self.neo4j_driver:
            await self.neo4j_driver.close()
        if self.redis_client:
            await self.redis_client.close()

    async def search_multi_source(
        self,
        query: str,
        sources: List[PaperSource] = None,
        **filters
    ) -> List[Paper]:
        """
        Search across multiple sources and merge results
        """
        if sources is None:
            sources = [PaperSource.SEMANTIC_SCHOLAR, PaperSource.ARXIV]

        tasks = []

        if PaperSource.SEMANTIC_SCHOLAR in sources:
            async with self.s2_client as client:
                tasks.append(client.search_papers(query, **filters))

        if PaperSource.ARXIV in sources:
            tasks.append(self.arxiv_client.search_papers(query, max_results=filters.get('limit', 100)))

        results = await asyncio.gather(*tasks)

        # Merge and deduplicate
        all_papers = []
        seen_titles = set()

        for paper_list in results:
            for paper in paper_list:
                title_normalized = paper.title.lower().strip()
                if title_normalized not in seen_titles:
                    seen_titles.add(title_normalized)
                    all_papers.append(paper)

        return all_papers

    async def build_citation_network(
        self,
        paper_ids: List[str],
        depth: int = 1
    ) -> Dict[str, Any]:
        """
        Build citation network for given papers
        Returns network data and analysis
        """
        papers = []
        citations = []

        async with self.s2_client as client:
            # Get paper details
            for paper_id in paper_ids:
                paper = await client.get_paper_details(paper_id)
                if paper:
                    papers.append(paper)

            # Get citations and references
            for paper_id in paper_ids:
                paper_citations = await client.get_citations(paper_id, limit=100)
                paper_references = await client.get_references(paper_id, limit=100)
                citations.extend(paper_citations)
                citations.extend(paper_references)

        # Build network
        self.citation_analyzer.build_network(papers, citations)

        # Analyze
        influential_papers = self.citation_analyzer.find_influential_papers(top_n=20)
        communities = self.citation_analyzer.detect_communities()

        return {
            'papers': [asdict(p) for p in papers],
            'citations': len(citations),
            'influential_papers': influential_papers,
            'communities': communities,
            'network_stats': {
                'nodes': self.citation_analyzer.graph.number_of_nodes(),
                'edges': self.citation_analyzer.graph.number_of_edges(),
                'density': nx.density(self.citation_analyzer.graph)
            }
        }

    async def synthesize_research(
        self,
        paper_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Synthesize information from multiple papers
        """
        papers = []

        async with self.s2_client as client:
            for paper_id in paper_ids:
                paper = await client.get_paper_details(paper_id)
                if paper:
                    papers.append(paper)

        if not papers:
            return {'error': 'No papers found'}

        # Perform synthesis
        key_findings = self.synthesizer.extract_key_findings(papers, top_k=10)
        methodologies = self.synthesizer.identify_methodologies(papers)
        gaps = self.synthesizer.identify_research_gaps(papers)
        summary = self.synthesizer.generate_synthesis_summary(papers)
        similarity_matrix = self.synthesizer.compute_paper_similarity(papers)

        return {
            'summary': summary,
            'key_findings': key_findings,
            'methodologies': methodologies,
            'research_gaps': gaps[:10],  # Top 10 gaps
            'similarity_matrix': similarity_matrix.tolist() if similarity_matrix.size > 0 else [],
            'paper_count': len(papers),
            'year_range': f"{min(p.publication_year for p in papers)}-{max(p.publication_year for p in papers)}"
        }


# ============================================================================
# EXPORT & UTILITY FUNCTIONS
# ============================================================================

def format_citation(paper: Paper, style: str = 'apa') -> str:
    """
    Format paper citation in various styles
    """
    authors = paper.authors[:3]
    author_str = ', '.join([a.name for a in authors])
    if len(paper.authors) > 3:
        author_str += ', et al.'

    if style == 'apa':
        return f"{author_str} ({paper.publication_year}). {paper.title}. {paper.venue}."
    elif style == 'mla':
        return f"{author_str}. \"{paper.title}.\" {paper.venue}, {paper.publication_year}."
    elif style == 'chicago':
        return f"{author_str}. \"{paper.title}.\" {paper.venue} ({paper.publication_year})."
    else:
        return f"{author_str} ({paper.publication_year}). {paper.title}. {paper.venue}."


# Example usage
if __name__ == "__main__":
    async def main():
        max_core = MAXCore(
            semantic_scholar_api_key="YOUR_API_KEY",
            postgres_config={
                'host': 'localhost',
                'port': 5432,
                'database': 'max_db',
                'user': 'max_user',
                'password': 'password'
            }
        )

        await max_core.initialize()

        # Search papers
        papers = await max_core.search_multi_source(
            "machine learning healthcare",
            sources=[PaperSource.SEMANTIC_SCHOLAR, PaperSource.ARXIV],
            year_min=2020,
            limit=50
        )

        print(f"Found {len(papers)} papers")

        # Synthesize research
        if len(papers) >= 5:
            paper_ids = [p.paper_id for p in papers[:5]]
            synthesis = await max_core.synthesize_research(paper_ids)
            print(f"Synthesis: {synthesis['summary']}")

        await max_core.close()

    asyncio.run(main())
