# Advanced QBank System with IRT Adaptive Testing

## Overview

This is an advanced Question Bank (QBank) system implementing Item Response Theory (IRT) for adaptive testing with Sympson-Hetter exposure control algorithms. The system provides psychometric analysis, calibration, and supports 5000+ practice questions with real-time adaptation.

## Features

- **IRT-based Adaptive Testing**: Uses 3-parameter logistic model for precise ability estimation
- **Sympson-Hetter Exposure Control**: Prevents item overexposure while maintaining test quality
- **Psychometric Analysis**: Real-time calibration and item parameter estimation
- **5000+ Questions Database**: Comprehensive question bank with metadata and tagging
- **Analytics Dashboard**: Visual representation of student performance and item statistics
- **Docker Deployment**: Complete containerized deployment solution
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Real-time Adaptation**: Dynamic question selection based on student ability

## Architecture

### Backend (FastAPI)
- **Core**: Configuration and database connectivity
- **Models**: SQLAlchemy models for questions, responses, and sessions
- **Services**: 
  - Adaptive testing engine with IRT implementation
  - Sympson-Hetter calibration service
- **API**: RESTful endpoints for question delivery and response processing

### Database (PostgreSQL)
- Optimized schema for high-performance question retrieval
- Indexed for adaptive algorithm queries
- Support for concurrent testing sessions

### Frontend
- Analytics dashboard for administrators
- Real-time performance visualization
- Item analysis tools

## IRT Implementation

The system uses a 3-parameter logistic (3PL) model:

```
P(θ) = c + (1-c) / (1 + exp(-a(θ-b)))
```

Where:
- θ: Student ability parameter
- a: Item discrimination
- b: Item difficulty
- c: Pseudo-guessing parameter

## Sympson-Hetter Exposure Control

Implements the Sympson-Hetter method to:
- Control maximum exposure rates
- Maintain content balance
- Ensure test security
- Optimize item usage

## Quick Start

### Using Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- FastAPI backend on port 8000
- Nginx proxy on port 80

### Manual Installation

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up database:
```bash
psql -U postgres -f sql/01_init_schema.sql
psql -U postgres -f sql/02_seed_data.sql
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Core Endpoints

- `POST /api/v1/sessions/start` - Start new adaptive testing session
- `GET /api/v1/questions/next` - Get next adaptive question
- `POST /api/v1/responses/submit` - Submit answer and get feedback
- `GET /api/v1/analytics/performance` - Get performance analytics
- `GET /api/v1/calibration/status` - Check calibration status

### Admin Endpoints

- `GET /api/v1/admin/items/analysis` - Item analysis report
- `POST /api/v1/admin/calibration/run` - Trigger recalibration
- `GET /api/v1/admin/exposure/report` - Exposure rate analysis

## Configuration

Environment variables (`.env`):

```env
DATABASE_URL=postgresql://user:password@localhost/qbank
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key
IRT_MODEL=3PL
EXPOSURE_RATE_MAX=0.25
MIN_RESPONSES_FOR_CALIBRATION=30
```

## Performance

- Supports 10,000+ concurrent users
- Sub-100ms question selection
- Real-time ability estimation
- Automatic scaling with Docker Swarm/Kubernetes

## Testing

Run the test suite:

```bash
pytest tests/ --cov=app
```

## Documentation

- API Documentation: http://localhost:8000/docs
- Analytics Dashboard: http://localhost/analytics
- Admin Panel: http://localhost/admin

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.