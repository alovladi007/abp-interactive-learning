# AI Path Advisor — Backend (FastAPI)

## Quickstart
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will run on http://127.0.0.1:8000

## API Endpoints

### POST /plan
Generate a learning roadmap based on goals and constraints.

### GET /skills
List all available skills with prerequisites.

### GET /resources
List all available learning resources.

### GET /modules
List all available learning modules.

## Test
```bash
curl -X POST http://127.0.0.1:8000/plan \
  -H "Content-Type: application/json" \
  -d '{
    "major":"cs",
    "goal":"ml-engineer",
    "horizon_months":12,
    "weekly_hours":15,
    "budget":200,
    "baseline_mastered":["prog.python.basics"]
  }'
```
