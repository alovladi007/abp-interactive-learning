# AI Path Advisor Starter Kit

A complete learning roadmap generator with FastAPI backend and Next.js frontend.

## Quick Start

### 1. Backend (Terminal 1)
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Frontend (Terminal 2)
```bash
cd frontend
npm install
npm run dev
```

### 3. Access
- Frontend: http://localhost:3001
- API Docs: http://localhost:8000/docs

## Features

### Backend
- FastAPI with automatic API documentation
- 50+ skills across CS, EE, Physics, Data Science
- 15+ learning modules with assessments
- 60+ curated resources (books, courses, videos)
- Intelligent path planning algorithm
- Career path templates
- Resource quality scoring

### Frontend
- Modern React/Next.js interface
- Interactive goal wizard
- Visual roadmap display
- Resource recommendations
- Progress tracking

## Data Structure

### Skills
- Prerequisite graph
- Difficulty levels
- Tags for categorization

### Modules
- Skill groupings
- Learning outcomes
- Assessment types
- Project ideas

### Resources
- Quality scores
- Time estimates
- Cost information
- Format types

## Customization

### Add New Major
1. Add skills to `backend/data/skills.json`
2. Add modules to `backend/data/modules.json`
3. Add resources to `backend/data/resources.json`
4. Update `MAJOR_TARGETS` in `backend/main.py`

### Add Career Path
Update `CAREER_PATHS` in `backend/main.py`

## API Endpoints

- `POST /plan` - Generate roadmap
- `GET /skills` - List all skills
- `GET /resources` - List all resources
- `GET /modules` - List all modules
- `GET /careers` - List career paths

## License
MIT
