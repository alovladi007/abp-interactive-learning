# AI Path Advisor - Complete Feature List

## IMPORTANT: Use the IMPROVED version!
**URL: `ai-path-advisor-improved.html`** (NOT the old `ai-path-advisor.html`)

## All 6 Majors Available (in ai-path-advisor-improved.html)

### 1. Computer Science
- Full Computer Science Degree (24-36 months)
- Machine Learning Engineer (12-18 months)
- Full Stack Developer (6-10 months)
- Data Engineer (8-12 months)
- Security Engineer (10-14 months)
- DevOps Engineer (8-12 months)

### 2. Electrical Engineering
- Full Electrical Engineering (24-36 months)
- Embedded Systems Engineer (10-14 months)
- Power Systems Engineer (12-18 months)
- Control Systems Engineer (12-16 months)
- RF/Communications Engineer (14-18 months)

### 3. Physics
- Full Physics Curriculum (24-36 months)
- Quantum Physics Focus (18-24 months)
- Computational Physics (12-18 months)
- Applied Physics (12-18 months)

### 4. Data Science
- Full Data Science Path (18-24 months)
- Data Analyst (6-9 months)
- Machine Learning Engineer (12-18 months)
- Data Engineer (8-12 months)
- Business Intelligence Analyst (6-9 months)

### 5. Public Health
- Full Public Health Curriculum (24-30 months)
- **Epidemiologist** (12-18 months) ✅
- Health Policy Analyst (10-14 months)
- Global Health Specialist (12-16 months)
- Biostatistician (10-14 months)

### 6. Materials Science
- Full Materials Science (24-36 months)
- **Polymer Engineer** (10-14 months) ✅
- Semiconductor Specialist (12-18 months)
- Nanomaterials Researcher (14-18 months)
- Biomaterials Engineer (12-16 months)

## Quiz System Features (in backend)

### Location: `ai-path-advisor-starter/backend/main.py`

#### Quiz Questions Per Major (5 questions each):
- **Computer Science**: Algorithms, OS, Databases, Networks, Software Engineering
- **Electrical Engineering**: Circuits, Digital Logic, Signals, Control, Power
- **Physics**: Mechanics, E&M, Quantum, Thermodynamics, Optics
- **Data Science**: Statistics, ML, Data Engineering, Visualization, Big Data
- **Public Health**: Epidemiology, Biostatistics, Health Policy, Environmental Health, Global Health
- **Materials Science**: Crystallography, Polymers, Electronic Materials, Mechanical Properties, Phase Diagrams

#### API Endpoints:
- `POST /quiz/start` - Start a baseline quiz
- `POST /quiz/grade` - Grade quiz and infer mastered skills

## How to Access the Features

### From Academic Setup:
1. Go to Academic Setup page
2. Find Louis AI Advisor card
3. Click "Create Path" button
4. This now links to `ai-path-advisor-improved.html` ✅

### Direct Access:
- Navigate to: `/ai-path-advisor-improved.html`

### What You See:
1. **Step 1**: Choose from 6 major cards (CS, EE, Physics, Data Science, Public Health, Materials)
2. **Step 2**: Select specific career path (5-6 options per major)
3. **Step 3**: Set preferences (hours/week, budget, learning style)
4. **Step 4**: Take baseline quiz (optional)
5. **Step 5**: Generate personalized roadmap

## File Locations

### Frontend:
- `ai-path-advisor-improved.html` - Main UI with all 6 majors (lines 806-849 contain career paths)
- `path-advisor.js` - JavaScript logic

### Backend:
- `ai-path-advisor-starter/backend/main.py` - FastAPI server (lines 408-600 contain quiz system)
- `ai-path-advisor-starter/backend/data/skills.json` - 90+ skills
- `ai-path-advisor-starter/backend/data/modules.json` - Learning modules
- `ai-path-advisor-starter/backend/data/resources.json` - 80+ resources

### Scripts:
- `create-ai-path-advisor-kit.py` - Creates initial system
- `extend-ai-path-advisor.py` - Added Public Health & Materials Science

## Verification Commands

To see all majors in the improved file:
```bash
grep -E "Computer Science|Electrical Engineering|Physics|Data Science|Public Health|Materials Science" ai-path-advisor-improved.html
```

To see career paths including Epidemiologist and Polymer Engineer:
```bash
grep -E "Epidemiologist|Polymer Engineer" ai-path-advisor-improved.html
```

To see quiz system:
```bash
grep -E "QUIZ_BANK|quiz/start|quiz/grade" ai-path-advisor-starter/backend/main.py
```

## GitHub Location
Repository: https://github.com/alovladi007/abp-interactive-learning
Branch: main
Path: /ai-path-advisor-improved.html (NOT the old ai-path-advisor.html)