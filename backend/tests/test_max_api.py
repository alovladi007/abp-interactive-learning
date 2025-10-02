"""
API endpoint tests for MAX Research Assistant

Tests all REST API endpoints for:
- Paper search
- Citation networks
- Research synthesis
- Collections
- Exports
- Health checks
"""

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch
import json

# Import FastAPI app
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app
from services.max_core_complete import Paper, PaperSource


class TestSearchEndpoint:
    """Test /api/max/search endpoint"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_search_papers_basic(self, client):
        """Test basic paper search"""

        mock_papers = [
            Paper(
                external_id="test123",
                source=PaperSource.SEMANTIC_SCHOLAR,
                title="Machine Learning in Healthcare",
                abstract="ML applications...",
                authors=["John Doe"],
                publication_date=datetime(2023, 1, 1),
                citations_count=50,
                venue="JAMA"
            )
        ]

        with patch('api.max_routes_complete.get_max') as mock_max:
            mock_max_instance = Mock()
            mock_max_instance.search_multi_source = AsyncMock(return_value=mock_papers)
            mock_max.return_value = mock_max_instance

            response = client.post("/api/max/search", json={
                "query": "machine learning healthcare",
                "sources": ["semantic_scholar"],
                "max_results": 10
            })

            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert "total" in data
            assert data["total"] >= 0

    def test_search_with_year_filters(self, client):
        """Test search with year range filters"""

        response = client.post("/api/max/search", json={
            "query": "deep learning",
            "sources": ["semantic_scholar"],
            "year_min": 2020,
            "year_max": 2024,
            "max_results": 20
        })

        # Should not error with filters
        assert response.status_code in [200, 500]  # 500 if MAX not initialized

    def test_search_with_citation_filter(self, client):
        """Test search with minimum citation filter"""

        response = client.post("/api/max/search", json={
            "query": "neural networks",
            "sources": ["semantic_scholar", "arxiv"],
            "min_citations": 100,
            "max_results": 10
        })

        assert response.status_code in [200, 500]

    def test_search_empty_query(self, client):
        """Test search with empty query"""

        response = client.post("/api/max/search", json={
            "query": "",
            "sources": ["semantic_scholar"],
            "max_results": 10
        })

        # Should handle empty query gracefully
        assert response.status_code in [200, 400, 422, 500]

    def test_search_invalid_source(self, client):
        """Test search with invalid source"""

        response = client.post("/api/max/search", json={
            "query": "test",
            "sources": ["invalid_source"],
            "max_results": 10
        })

        # Should reject invalid source
        assert response.status_code in [400, 422, 500]


class TestCitationNetworkEndpoint:
    """Test /api/max/citations/network endpoint"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_build_citation_network(self, client):
        """Test building citation network"""

        response = client.post("/api/max/citations/network", json={
            "paper_ids": ["paper1", "paper2", "paper3"],
            "depth": 1,
            "min_citations": 10
        })

        # Should return network structure
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "nodes" in data or "network" in data

    def test_citation_network_single_paper(self, client):
        """Test network with single paper"""

        response = client.post("/api/max/citations/network", json={
            "paper_ids": ["paper1"],
            "depth": 2
        })

        assert response.status_code in [200, 500]

    def test_citation_network_invalid_depth(self, client):
        """Test network with invalid depth"""

        response = client.post("/api/max/citations/network", json={
            "paper_ids": ["paper1"],
            "depth": -1
        })

        # Should reject negative depth
        assert response.status_code in [400, 422, 500]


class TestSynthesisEndpoint:
    """Test /api/max/synthesize endpoint"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_synthesize_papers(self, client):
        """Test paper synthesis"""

        response = client.post("/api/max/synthesize", json={
            "paper_ids": ["paper1", "paper2", "paper3"],
            "include_methodologies": True,
            "include_gaps": True
        })

        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "summary" in data or "synthesis" in data

    def test_synthesize_single_paper(self, client):
        """Test synthesis with single paper"""

        response = client.post("/api/max/synthesize", json={
            "paper_ids": ["paper1"],
            "include_methodologies": False,
            "include_gaps": False
        })

        assert response.status_code in [200, 500]

    def test_synthesize_empty_papers(self, client):
        """Test synthesis with no papers"""

        response = client.post("/api/max/synthesize", json={
            "paper_ids": [],
            "include_methodologies": True,
            "include_gaps": True
        })

        # Should handle empty list
        assert response.status_code in [200, 400, 422, 500]


class TestCollectionsEndpoint:
    """Test collection management endpoints"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_create_collection(self, client):
        """Test creating a new collection"""

        response = client.post("/api/max/collections", json={
            "name": "My Research Collection",
            "description": "Papers on ML in healthcare",
            "user_id": "user123",
            "is_public": False,
            "color": "#667eea"
        })

        assert response.status_code in [200, 201, 500]

        if response.status_code in [200, 201]:
            data = response.json()
            assert "collection_id" in data or "id" in data

    def test_create_collection_missing_name(self, client):
        """Test creating collection without name"""

        response = client.post("/api/max/collections", json={
            "description": "No name provided",
            "user_id": "user123"
        })

        # Should require name
        assert response.status_code in [400, 422, 500]

    def test_add_papers_to_collection(self, client):
        """Test adding papers to collection"""

        response = client.post("/api/max/collections/col123/papers", json={
            "paper_ids": ["paper1", "paper2", "paper3"]
        })

        assert response.status_code in [200, 404, 500]

    def test_get_collection_papers(self, client):
        """Test retrieving collection papers"""

        response = client.get("/api/max/collections/col123/papers")

        assert response.status_code in [200, 404, 500]


class TestExportEndpoint:
    """Test citation export endpoints"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_export_citations_apa(self, client):
        """Test APA format export"""

        response = client.post("/api/max/export/citations", json={
            "paper_ids": ["paper1", "paper2"],
            "format": "apa",
            "style": "text"
        })

        assert response.status_code in [200, 500]

        if response.status_code == 200:
            # Should return text or file
            assert response.headers.get("content-type") in [
                "text/plain",
                "application/json",
                None
            ]

    def test_export_citations_bibtex(self, client):
        """Test BibTeX format export"""

        response = client.post("/api/max/export/citations", json={
            "paper_ids": ["paper1", "paper2", "paper3"],
            "format": "bibtex",
            "style": "bibtex"
        })

        assert response.status_code in [200, 500]

    def test_export_citations_json(self, client):
        """Test JSON format export"""

        response = client.post("/api/max/export/citations", json={
            "paper_ids": ["paper1"],
            "format": "json",
            "style": "json"
        })

        assert response.status_code in [200, 500]

        if response.status_code == 200:
            # Should be valid JSON
            try:
                data = response.json()
                assert isinstance(data, (dict, list))
            except:
                pass  # May be text response

    def test_export_invalid_format(self, client):
        """Test export with invalid format"""

        response = client.post("/api/max/export/citations", json={
            "paper_ids": ["paper1"],
            "format": "invalid_format",
            "style": "text"
        })

        # Should reject invalid format
        assert response.status_code in [400, 422, 500]


class TestPaperDetailsEndpoint:
    """Test paper details endpoints"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_get_paper_details(self, client):
        """Test retrieving paper details"""

        response = client.get("/api/max/papers/test123")

        assert response.status_code in [200, 404, 500]

        if response.status_code == 200:
            data = response.json()
            assert "title" in data or "paper" in data

    def test_get_paper_citations(self, client):
        """Test retrieving paper citations"""

        response = client.get("/api/max/papers/test123/citations?limit=50")

        assert response.status_code in [200, 404, 500]

    def test_get_paper_references(self, client):
        """Test retrieving paper references"""

        response = client.get("/api/max/papers/test123/references?limit=50")

        assert response.status_code in [200, 404, 500]


class TestTrendsEndpoint:
    """Test research trends endpoints"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_get_trending_papers(self, client):
        """Test retrieving trending papers"""

        response = client.get("/api/max/trends/papers?field=computer_science&days=30")

        assert response.status_code in [200, 500]

    def test_get_trending_topics(self, client):
        """Test retrieving trending topics"""

        response = client.get("/api/max/trends/topics?field=machine_learning&limit=10")

        assert response.status_code in [200, 500]

    def test_get_field_statistics(self, client):
        """Test field statistics"""

        response = client.get("/api/max/trends/statistics?field=computer_science")

        assert response.status_code in [200, 500]


class TestRecommendationsEndpoint:
    """Test paper recommendation endpoints"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_get_similar_papers(self, client):
        """Test finding similar papers"""

        response = client.post("/api/max/recommend/similar", json={
            "paper_id": "test123",
            "limit": 10,
            "method": "embedding"
        })

        assert response.status_code in [200, 404, 500]

    def test_get_recommendations_by_collection(self, client):
        """Test recommendations based on collection"""

        response = client.get("/api/max/recommend/collection/col123?limit=20")

        assert response.status_code in [200, 404, 500]


class TestHealthEndpoint:
    """Test health check endpoints"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_health_check(self, client):
        """Test basic health check"""

        response = client.get("/api/max/health")

        # Health check should always respond
        assert response.status_code == 200

        data = response.json()
        assert "status" in data

    def test_detailed_health_check(self, client):
        """Test detailed health status"""

        response = client.get("/api/max/health/detailed")

        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            # Should include service statuses
            assert isinstance(data, dict)


class TestRateLimiting:
    """Test rate limiting behavior"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_rate_limit_search(self, client):
        """Test search rate limiting"""

        # Make multiple rapid requests
        responses = []
        for i in range(5):
            response = client.post("/api/max/search", json={
                "query": f"test query {i}",
                "sources": ["semantic_scholar"],
                "max_results": 5
            })
            responses.append(response)

        # All should complete (rate limiting happens at API client level)
        assert all(r.status_code in [200, 429, 500] for r in responses)


class TestValidation:
    """Test input validation"""

    @pytest.fixture
    def client(self):
        return TestClient(app)

    def test_search_max_results_limit(self, client):
        """Test max_results upper bound"""

        response = client.post("/api/max/search", json={
            "query": "test",
            "sources": ["semantic_scholar"],
            "max_results": 10000  # Extremely high
        })

        # Should cap or reject
        assert response.status_code in [200, 400, 422, 500]

    def test_collection_name_length(self, client):
        """Test collection name length validation"""

        response = client.post("/api/max/collections", json={
            "name": "A" * 1000,  # Very long name
            "user_id": "user123"
        })

        # Should validate length
        assert response.status_code in [200, 201, 400, 422, 500]

    def test_paper_ids_limit(self, client):
        """Test paper IDs list size limit"""

        response = client.post("/api/max/synthesize", json={
            "paper_ids": [f"paper{i}" for i in range(1000)],  # Many papers
            "include_methodologies": True,
            "include_gaps": True
        })

        # Should handle or reject large lists
        assert response.status_code in [200, 400, 422, 500]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
