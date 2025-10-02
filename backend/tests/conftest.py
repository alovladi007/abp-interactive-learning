"""
Pytest configuration and shared fixtures for MAX tests
"""

import pytest
import asyncio
from typing import Generator


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_db_config():
    """Mock database configuration"""
    return {
        "host": "localhost",
        "port": 5432,
        "database": "max_test_db",
        "user": "test_user",
        "password": "test_password"
    }


@pytest.fixture
def mock_neo4j_config():
    """Mock Neo4j configuration"""
    return {
        "uri": "bolt://localhost:7687",
        "user": "neo4j",
        "password": "test_password"
    }


@pytest.fixture
def sample_papers():
    """Sample papers for testing"""
    from datetime import datetime
    from services.max_core_complete import Paper, PaperSource

    return [
        Paper(
            external_id="paper1",
            source=PaperSource.SEMANTIC_SCHOLAR,
            title="Deep Learning for Computer Vision",
            abstract="This paper presents a comprehensive survey of deep learning methods for computer vision tasks.",
            authors=["Alice Johnson", "Bob Smith"],
            publication_date=datetime(2023, 1, 15),
            citations_count=125,
            venue="CVPR",
            url="https://example.com/paper1",
            pdf_url="https://example.com/paper1.pdf"
        ),
        Paper(
            external_id="paper2",
            source=PaperSource.ARXIV,
            title="Attention Mechanisms in Neural Networks",
            abstract="We explore various attention mechanisms and their applications in sequence modeling.",
            authors=["Charlie Davis"],
            publication_date=datetime(2023, 3, 20),
            citations_count=87,
            venue="arXiv",
            url="https://arxiv.org/abs/2303.00002",
            pdf_url="https://arxiv.org/pdf/2303.00002.pdf"
        ),
        Paper(
            external_id="paper3",
            source=PaperSource.SEMANTIC_SCHOLAR,
            title="Transfer Learning in NLP",
            abstract="Transfer learning has revolutionized natural language processing through pre-trained models.",
            authors=["Eve Wilson", "Frank Miller"],
            publication_date=datetime(2022, 11, 10),
            citations_count=243,
            venue="ACL",
            url="https://example.com/paper3"
        )
    ]


@pytest.fixture
def sample_citations():
    """Sample citations for testing"""
    from services.max_core_complete import CitationContext

    return [
        CitationContext(
            citing_paper_id="paper2",
            cited_paper_id="paper1",
            context="Building on the work of Johnson and Smith, we extend their approach...",
            intent="methodology",
            is_influential=True
        ),
        CitationContext(
            citing_paper_id="paper2",
            cited_paper_id="paper3",
            context="As demonstrated by Wilson and Miller, pre-trained models...",
            intent="background",
            is_influential=True
        )
    ]
