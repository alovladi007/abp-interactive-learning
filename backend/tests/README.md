# MAX Research Assistant - Testing Suite

Comprehensive test suite for the MAX AI Research Assistant.

## Test Coverage

### Core Functionality Tests (`test_max.py`)

- **SemanticScholarClient**: API client for Semantic Scholar
  - Paper search with pagination
  - Rate limiting and retry logic
  - Citation retrieval
  - Error handling

- **ArXivClient**: API client for ArXiv
  - XML response parsing
  - Date parsing and formatting
  - Category extraction

- **MAXCore**: Main service orchestration
  - Multi-source paper search
  - Result deduplication
  - Filter application (year, citations, venue)
  - Database integration

- **CitationNetworkAnalyzer**: Network analysis
  - Graph construction
  - PageRank influence scoring
  - Community detection
  - Betweenness centrality
  - Co-citation analysis

- **PaperSynthesizer**: Research synthesis
  - Key findings extraction (TF-IDF)
  - Methodology identification
  - Research gap detection
  - Paper similarity computation

- **Collections Management**
  - Collection creation
  - Adding papers to collections
  - Public/private collections

- **Export Functionality**
  - APA citation formatting
  - MLA, Chicago, IEEE formats
  - BibTeX export
  - RIS format

### API Endpoint Tests (`test_max_api.py`)

- **Search Endpoint** (`/api/max/search`)
  - Basic search
  - Multi-source search
  - Year range filters
  - Citation count filters
  - Venue filters
  - Input validation

- **Citation Network** (`/api/max/citations/network`)
  - Network construction
  - Depth control
  - Minimum citation filtering

- **Synthesis** (`/api/max/synthesize`)
  - Multi-paper synthesis
  - Methodology extraction toggle
  - Research gaps toggle

- **Collections** (`/api/max/collections/*`)
  - Create collection
  - Add papers to collection
  - Retrieve collection papers
  - Delete collections

- **Export** (`/api/max/export/citations`)
  - Multiple citation formats
  - Format validation
  - File download

- **Paper Details** (`/api/max/papers/{id}`)
  - Get paper metadata
  - Get citations
  - Get references

- **Trends** (`/api/max/trends/*`)
  - Trending papers
  - Trending topics
  - Field statistics

- **Recommendations** (`/api/max/recommend/*`)
  - Similar papers
  - Collection-based recommendations

- **Health Checks** (`/api/max/health`)
  - Basic health
  - Detailed service status

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-asyncio httpx
```

### Run All Tests

```bash
cd backend
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_max.py -v
pytest tests/test_max_api.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_max.py::TestSemanticScholarClient -v
```

### Run Specific Test

```bash
pytest tests/test_max.py::TestSemanticScholarClient::test_search_papers_success -v
```

### Run with Coverage

```bash
pip install pytest-cov
pytest tests/ --cov=services --cov=api --cov-report=html
```

View coverage report: `open htmlcov/index.html`

### Run Tests in Parallel

```bash
pip install pytest-xdist
pytest tests/ -n auto
```

## Test Configuration

### Environment Variables

Create `.env.test` file:

```env
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=max_test_db
POSTGRES_USER=test_user
POSTGRES_PASSWORD=test_password

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=test_password

# API Keys (optional for mocked tests)
SEMANTIC_SCHOLAR_API_KEY=test_key
```

### Test Database Setup

For integration tests with real database:

```bash
# PostgreSQL
createdb max_test_db
psql max_test_db < database/max_schema.sql

# Neo4j
# Start test Neo4j instance on different port
docker run -d \
  --name neo4j-test \
  -p 7688:7687 \
  -e NEO4J_AUTH=neo4j/test_password \
  neo4j:5.14-community
```

## Test Organization

```
tests/
├── conftest.py              # Shared fixtures
├── test_max.py              # Core service tests
├── test_max_api.py          # API endpoint tests
└── README.md                # This file
```

## Mocking Strategy

Tests use mocking to avoid external API calls:

- **API Clients**: Mock HTTP responses
- **Database**: Mock database connections
- **Neo4j**: Mock graph operations

This ensures:
- Fast test execution
- No external dependencies
- Deterministic results
- No API rate limits

## Integration Tests

For end-to-end testing with real services:

```bash
# Set environment variable
export MAX_INTEGRATION_TESTS=true

# Run integration tests
pytest tests/ -v -m integration
```

## Continuous Integration

GitHub Actions workflow (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx pytest-cov
      - name: Run tests
        run: pytest tests/ -v --cov=services --cov=api
```

## Test Metrics

Target coverage: **85%+**

Current test count: **60+ tests**

Areas covered:
- ✅ API clients (Semantic Scholar, ArXiv)
- ✅ Core search functionality
- ✅ Citation network analysis
- ✅ Research synthesis
- ✅ Collections management
- ✅ Export functionality
- ✅ Error handling
- ✅ Input validation
- ✅ API endpoints

## Writing New Tests

### Test Template

```python
import pytest
from unittest.mock import Mock, AsyncMock, patch

class TestNewFeature:
    """Test description"""

    @pytest.mark.asyncio
    async def test_feature_success(self):
        """Test successful operation"""
        # Arrange
        mock_data = {...}

        # Act
        result = await function_under_test(mock_data)

        # Assert
        assert result == expected_value

    @pytest.mark.asyncio
    async def test_feature_error(self):
        """Test error handling"""
        with patch('module.function', side_effect=Exception("Error")):
            result = await function_under_test(invalid_data)
            assert result == []  # Graceful failure
```

### Best Practices

1. **Use descriptive test names**: `test_search_papers_with_year_filter`
2. **One assertion per test**: Focus on single behavior
3. **Mock external dependencies**: No real API calls
4. **Test edge cases**: Empty inputs, errors, limits
5. **Use fixtures**: Share test data via conftest.py
6. **Async tests**: Use `@pytest.mark.asyncio` for async functions

## Troubleshooting

### Import Errors

```bash
# Add backend to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
pytest tests/
```

### Async Warnings

If you see warnings about event loops:

```python
# In conftest.py (already configured)
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

### Database Connection Errors

For mocked tests, ensure proper mocking:

```python
with patch('services.max_core_complete.asyncpg.connect'):
    # Test code
    pass
```

## Future Enhancements

- [ ] Performance benchmarking tests
- [ ] Load testing with locust
- [ ] Security testing (SQL injection, XSS)
- [ ] API contract testing
- [ ] Snapshot testing for complex outputs
