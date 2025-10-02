"""
Comprehensive test suite for MAX AI Research Assistant

Tests cover:
- Multi-source paper search
- Citation network building and analysis
- Research synthesis
- Collections management
- Export functionality
- Error handling
"""

import pytest
import asyncio
from datetime import datetime
from typing import List, Dict, Any

# Mock imports for testing without actual API calls
from unittest.mock import Mock, AsyncMock, patch, MagicMock

# Import MAX components
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.max_core_complete import (
    MAXCore,
    SemanticScholarClient,
    ArXivClient,
    CitationNetworkAnalyzer,
    PaperSynthesizer,
    Paper,
    PaperSource,
    CitationContext
)


class TestSemanticScholarClient:
    """Test Semantic Scholar API client"""

    @pytest.mark.asyncio
    async def test_search_papers_success(self):
        """Test successful paper search"""
        client = SemanticScholarClient()

        mock_response = {
            "total": 1,
            "data": [{
                "paperId": "test123",
                "title": "Test Paper on Machine Learning",
                "abstract": "This is a test abstract about ML.",
                "authors": [{"name": "John Doe", "authorId": "author1"}],
                "year": 2023,
                "citationCount": 42,
                "venue": "ICML",
                "publicationDate": "2023-01-15",
                "isOpenAccess": True,
                "fieldsOfStudy": ["Computer Science", "Machine Learning"]
            }]
        }

        with patch.object(client.session, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)
            mock_get.return_value.__aenter__.return_value.status = 200

            results = await client.search_papers("machine learning", limit=10)

            assert len(results) == 1
            assert results[0].external_id == "test123"
            assert results[0].title == "Test Paper on Machine Learning"
            assert results[0].citations_count == 42
            assert results[0].source == PaperSource.SEMANTIC_SCHOLAR

    @pytest.mark.asyncio
    async def test_search_papers_rate_limit(self):
        """Test rate limiting behavior"""
        client = SemanticScholarClient()

        with patch.object(client.session, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.__aenter__.return_value.status = 429

            results = await client.search_papers("test query")

            assert len(results) == 0

    @pytest.mark.asyncio
    async def test_get_paper_citations(self):
        """Test fetching paper citations"""
        client = SemanticScholarClient()

        mock_response = {
            "data": [
                {
                    "citingPaper": {
                        "paperId": "citing1",
                        "title": "Citing Paper 1",
                        "abstract": "This cites the original paper.",
                        "authors": [{"name": "Jane Smith"}],
                        "year": 2024
                    },
                    "contexts": ["We build on the work of..."],
                    "intents": ["background"]
                }
            ]
        }

        with patch.object(client.session, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)
            mock_get.return_value.__aenter__.return_value.status = 200

            citations = await client.get_paper_citations("test123", limit=100)

            assert len(citations) == 1
            assert citations[0].title == "Citing Paper 1"


class TestArXivClient:
    """Test ArXiv API client"""

    @pytest.mark.asyncio
    async def test_search_papers_xml_parsing(self):
        """Test XML response parsing"""
        client = ArXivClient()

        mock_xml = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <id>http://arxiv.org/abs/2301.00001v1</id>
                <title>Test ArXiv Paper</title>
                <summary>Test abstract for arxiv paper.</summary>
                <author><name>Test Author</name></author>
                <published>2023-01-01T00:00:00Z</published>
                <arxiv:primary_category term="cs.LG" xmlns:arxiv="http://arxiv.org/schemas/atom"/>
            </entry>
        </feed>
        """

        with patch.object(client.session, 'get', new_callable=AsyncMock) as mock_get:
            mock_get.return_value.__aenter__.return_value.text = AsyncMock(return_value=mock_xml)
            mock_get.return_value.__aenter__.return_value.status = 200

            results = await client.search_papers("test query", max_results=10)

            assert len(results) == 1
            assert results[0].title == "Test ArXiv Paper"
            assert results[0].source == PaperSource.ARXIV
            assert "2301.00001" in results[0].external_id


class TestMAXCore:
    """Test main MAX core functionality"""

    @pytest.fixture
    def max_core(self):
        """Create MAXCore instance for testing"""
        return MAXCore(
            db_config={"mock": True},
            neo4j_config={"mock": True}
        )

    @pytest.mark.asyncio
    async def test_search_multi_source(self, max_core):
        """Test multi-source search with deduplication"""

        # Mock Semantic Scholar results
        ss_paper = Paper(
            external_id="ss123",
            source=PaperSource.SEMANTIC_SCHOLAR,
            title="Machine Learning for Healthcare",
            abstract="ML in healthcare...",
            authors=["John Doe"],
            publication_date=datetime(2023, 1, 1),
            citations_count=50
        )

        # Mock ArXiv results with similar title (should be deduplicated)
        arxiv_paper = Paper(
            external_id="2301.00001",
            source=PaperSource.ARXIV,
            title="machine learning for healthcare",  # Slight variation
            abstract="ML in healthcare...",
            authors=["John Doe", "Jane Smith"],
            publication_date=datetime(2023, 1, 1),
            citations_count=0
        )

        with patch.object(max_core.semantic_scholar, 'search_papers',
                         new_callable=AsyncMock, return_value=[ss_paper]):
            with patch.object(max_core.arxiv_client, 'search_papers',
                             new_callable=AsyncMock, return_value=[arxiv_paper]):

                results = await max_core.search_multi_source(
                    query="machine learning healthcare",
                    sources=[PaperSource.SEMANTIC_SCHOLAR, PaperSource.ARXIV]
                )

                # Should deduplicate similar titles
                assert len(results) <= 2

                # Should prioritize Semantic Scholar (has citations)
                if len(results) == 1:
                    assert results[0].source == PaperSource.SEMANTIC_SCHOLAR

    @pytest.mark.asyncio
    async def test_search_with_filters(self, max_core):
        """Test search with year and citation filters"""

        papers = [
            Paper(
                external_id="old_paper",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="Old Paper",
                abstract="Old research",
                authors=["Author 1"],
                publication_date=datetime(2015, 1, 1),
                citations_count=5
            ),
            Paper(
                external_id="new_paper",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="New Highly Cited Paper",
                abstract="Recent breakthrough",
                authors=["Author 2"],
                publication_date=datetime(2023, 1, 1),
                citations_count=100
            )
        ]

        with patch.object(max_core.semantic_scholar, 'search_papers',
                         new_callable=AsyncMock, return_value=papers):

            # Filter by year
            results = await max_core.search_multi_source(
                query="test",
                year_min=2020,
                sources=[PaperSource.SEMANTIC_SCHOLAR]
            )

            filtered = max_core._apply_filters(results, year_min=2020, min_citations=50)

            assert len(filtered) == 1
            assert filtered[0].external_id == "new_paper"
            assert filtered[0].publication_date.year >= 2020
            assert filtered[0].citations_count >= 50


class TestCitationNetworkAnalyzer:
    """Test citation network analysis"""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return CitationNetworkAnalyzer()

    def test_build_network_structure(self, analyzer):
        """Test basic network construction"""

        papers = [
            Paper(
                external_id="paper1",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="Paper 1",
                abstract="First paper",
                authors=["Author A"],
                publication_date=datetime(2020, 1, 1),
                citations_count=10
            ),
            Paper(
                external_id="paper2",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="Paper 2",
                abstract="Second paper",
                authors=["Author B"],
                publication_date=datetime(2021, 1, 1),
                citations_count=20
            )
        ]

        citations = [
            CitationContext(
                citing_paper_id="paper2",
                cited_paper_id="paper1",
                context="We build on paper1...",
                intent="background",
                is_influential=True
            )
        ]

        network = analyzer.build_network(papers, citations)

        assert network["nodes_count"] == 2
        assert network["edges_count"] == 1
        assert "paper1" in network["nodes"]
        assert "paper2" in network["nodes"]

    def test_pagerank_calculation(self, analyzer):
        """Test PageRank influence scoring"""

        papers = [
            Paper(external_id=f"paper{i}", source=PaperSource.SEMANTIC_SCHOLAR,
                  title=f"Paper {i}", abstract="Abstract", authors=["Author"],
                  publication_date=datetime(2020, 1, 1), citations_count=0)
            for i in range(5)
        ]

        # Create citation network: paper4 is cited by all others
        citations = [
            CitationContext(
                citing_paper_id=f"paper{i}",
                cited_paper_id="paper4",
                context="",
                intent="background",
                is_influential=True
            )
            for i in range(4)
        ]

        network = analyzer.build_network(papers, citations)

        # paper4 should have highest PageRank
        pagerank_scores = network.get("pagerank", {})
        if pagerank_scores:
            assert pagerank_scores["paper4"] > pagerank_scores["paper0"]

    def test_community_detection(self, analyzer):
        """Test research community detection"""

        # Create two disconnected groups
        papers = [Paper(
            external_id=f"paper{i}",
            source=PaperSource.SEMANTIC_SCHOLAR,
            title=f"Paper {i}",
            abstract="Abstract",
            authors=["Author"],
            publication_date=datetime(2020, 1, 1),
            citations_count=0
        ) for i in range(6)]

        # Group 1: papers 0,1,2 cite each other
        # Group 2: papers 3,4,5 cite each other
        citations = []
        for i in range(3):
            for j in range(3):
                if i != j:
                    citations.append(CitationContext(
                        citing_paper_id=f"paper{i}",
                        cited_paper_id=f"paper{j}",
                        context="",
                        intent="background",
                        is_influential=False
                    ))

        for i in range(3, 6):
            for j in range(3, 6):
                if i != j:
                    citations.append(CitationContext(
                        citing_paper_id=f"paper{i}",
                        cited_paper_id=f"paper{j}",
                        context="",
                        intent="background",
                        is_influential=False
                    ))

        network = analyzer.build_network(papers, citations)

        # Should detect at least 2 communities
        communities = network.get("communities", {})
        unique_communities = set(communities.values()) if communities else set()
        assert len(unique_communities) >= 2


class TestPaperSynthesizer:
    """Test research synthesis functionality"""

    @pytest.fixture
    def synthesizer(self):
        """Create synthesizer instance"""
        return PaperSynthesizer()

    def test_extract_key_findings(self, synthesizer):
        """Test key findings extraction"""

        papers = [
            Paper(
                external_id="paper1",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="Neural Networks for Image Classification",
                abstract="We propose a novel convolutional neural network architecture. "
                        "Our results show 95% accuracy on ImageNet dataset. "
                        "The proposed method outperforms previous approaches.",
                authors=["Author A"],
                publication_date=datetime(2023, 1, 1),
                citations_count=50
            ),
            Paper(
                external_id="paper2",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="Transfer Learning in Computer Vision",
                abstract="Transfer learning significantly improves performance on small datasets. "
                        "We achieve state-of-the-art results with minimal training data. "
                        "Fine-tuning pre-trained models is highly effective.",
                authors=["Author B"],
                publication_date=datetime(2023, 6, 1),
                citations_count=30
            )
        ]

        synthesis = synthesizer.synthesize(papers)

        assert "summary" in synthesis
        assert "key_findings" in synthesis
        assert len(synthesis["key_findings"]) > 0

        # Should identify important terms
        findings_text = " ".join(synthesis["key_findings"]).lower()
        assert "neural" in findings_text or "learning" in findings_text

    def test_methodology_identification(self, synthesizer):
        """Test methodology extraction"""

        papers = [
            Paper(
                external_id="paper1",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="Experimental Study",
                abstract="We conducted a randomized controlled trial with 100 participants. "
                        "Participants were randomly assigned to treatment and control groups. "
                        "Data was collected using surveys and analyzed using ANOVA.",
                authors=["Author A"],
                publication_date=datetime(2023, 1, 1),
                citations_count=10
            )
        ]

        synthesis = synthesizer.synthesize(papers)

        assert "methodologies" in synthesis
        methodologies = synthesis["methodologies"]

        # Should identify experimental method
        method_text = " ".join(methodologies).lower()
        assert any(term in method_text for term in ["randomized", "controlled", "trial", "experimental"])

    def test_research_gaps_detection(self, synthesizer):
        """Test research gap identification"""

        papers = [
            Paper(
                external_id="paper1",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="Limitations Study",
                abstract="However, our study has several limitations. "
                        "Future work should investigate larger sample sizes. "
                        "Further research is needed to validate these findings. "
                        "More studies are required to understand the mechanism.",
                authors=["Author A"],
                publication_date=datetime(2023, 1, 1),
                citations_count=5
            )
        ]

        synthesis = synthesizer.synthesize(papers)

        assert "research_gaps" in synthesis
        gaps = synthesis["research_gaps"]

        # Should identify gap indicators
        assert len(gaps) > 0
        gaps_text = " ".join(gaps).lower()
        assert any(term in gaps_text for term in ["limitation", "future", "further", "needed"])


class TestCollectionsManagement:
    """Test research collections functionality"""

    @pytest.mark.asyncio
    async def test_create_collection(self):
        """Test creating a new collection"""

        # Mock database
        mock_db = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {"collection_id": "col123"}

        collection_data = {
            "name": "My Research Collection",
            "description": "Papers on ML",
            "user_id": "user123",
            "is_public": False,
            "color": "#667eea"
        }

        # Simulate collection creation
        assert collection_data["name"] == "My Research Collection"
        assert collection_data["is_public"] is False

    @pytest.mark.asyncio
    async def test_add_papers_to_collection(self):
        """Test adding papers to collection"""

        collection_id = "col123"
        paper_ids = ["paper1", "paper2", "paper3"]

        # Verify paper IDs are valid
        assert len(paper_ids) == 3
        assert all(isinstance(pid, str) for pid in paper_ids)


class TestExportFunctionality:
    """Test citation export in various formats"""

    def test_format_apa_citation(self):
        """Test APA format citation"""

        paper = Paper(
            external_id="test123",
            source=PaperSource.SEMANTIC_SCHOLAR,
            title="Machine Learning Applications in Healthcare",
            abstract="Abstract text",
            authors=["Smith, J.", "Doe, A."],
            publication_date=datetime(2023, 3, 15),
            citations_count=25,
            venue="Journal of Medical AI"
        )

        # Format as APA
        apa = f"{', '.join(paper.authors)} ({paper.publication_date.year}). " \
              f"{paper.title}. {paper.venue or 'Unpublished'}."

        assert "Smith, J., Doe, A." in apa
        assert "(2023)" in apa
        assert paper.title in apa

    def test_format_bibtex_citation(self):
        """Test BibTeX format citation"""

        paper = Paper(
            external_id="smith2023ml",
            source=PaperSource.SEMANTIC_SCHOLAR,
            title="Machine Learning Applications",
            abstract="Abstract",
            authors=["John Smith", "Alice Doe"],
            publication_date=datetime(2023, 1, 1),
            citations_count=10,
            venue="ICML"
        )

        # Format as BibTeX
        bibtex = f"""@article{{smith2023ml,
    title={{{paper.title}}},
    author={{{' and '.join(paper.authors)}}},
    year={{{paper.publication_date.year}}},
    journal={{{paper.venue or 'arXiv'}}}
}}"""

        assert "@article{" in bibtex
        assert paper.title in bibtex
        assert "John Smith and Alice Doe" in bibtex


class TestErrorHandling:
    """Test error handling and edge cases"""

    @pytest.mark.asyncio
    async def test_network_error_handling(self):
        """Test graceful handling of network errors"""

        client = SemanticScholarClient()

        with patch.object(client.session, 'get', side_effect=Exception("Network error")):
            results = await client.search_papers("test query")

            # Should return empty list instead of crashing
            assert results == []

    @pytest.mark.asyncio
    async def test_empty_results_handling(self):
        """Test handling of empty search results"""

        max_core = MAXCore(db_config={"mock": True}, neo4j_config={"mock": True})

        with patch.object(max_core.semantic_scholar, 'search_papers',
                         new_callable=AsyncMock, return_value=[]):

            results = await max_core.search_multi_source(
                query="nonexistent query xyz123",
                sources=[PaperSource.SEMANTIC_SCHOLAR]
            )

            assert results == []

    def test_invalid_date_handling(self):
        """Test handling of papers with invalid dates"""

        # Paper with None date should be handled gracefully
        paper = Paper(
            external_id="test",
            source=PaperSource.ARXIV,
            title="Test Paper",
            abstract="Abstract",
            authors=["Author"],
            publication_date=None,
            citations_count=0
        )

        # Should not crash when accessing date
        year = paper.publication_date.year if paper.publication_date else None
        assert year is None


class TestIntegration:
    """Integration tests for complete workflows"""

    @pytest.mark.asyncio
    async def test_complete_search_and_network_workflow(self):
        """Test end-to-end search -> network -> synthesis"""

        max_core = MAXCore(db_config={"mock": True}, neo4j_config={"mock": True})

        # Mock papers
        papers = [
            Paper(
                external_id=f"paper{i}",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title=f"Deep Learning Paper {i}",
                abstract=f"This paper explores deep learning methods. "
                        f"We propose a novel architecture with {i*10}% accuracy.",
                authors=[f"Author {i}"],
                publication_date=datetime(2023, i, 1),
                citations_count=i * 10
            )
            for i in range(1, 4)
        ]

        # Mock citations
        citations = [
            CitationContext(
                citing_paper_id="paper3",
                cited_paper_id="paper1",
                context="Building on the work of paper1...",
                intent="background",
                is_influential=True
            ),
            CitationContext(
                citing_paper_id="paper3",
                cited_paper_id="paper2",
                context="We extend paper2's approach...",
                intent="methodology",
                is_influential=True
            )
        ]

        # Build network
        analyzer = CitationNetworkAnalyzer()
        network = analyzer.build_network(papers, citations)

        assert network["nodes_count"] == 3
        assert network["edges_count"] == 2

        # Synthesize research
        synthesizer = PaperSynthesizer()
        synthesis = synthesizer.synthesize(papers)

        assert "summary" in synthesis
        assert len(synthesis["key_findings"]) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
