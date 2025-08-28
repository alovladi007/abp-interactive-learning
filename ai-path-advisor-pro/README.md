# 🚀 AI Path Advisor Pro

A comprehensive, production-ready learning path planner with advanced optimization and tracking features.

## ✨ Features

### Core Capabilities
- **20 Academic Majors**: CS, EE, Physics, Medicine, Law, Economics, and more
- **240+ Courses**: Top 12 courses per major with complete syllabi
- **15+ Career Roles**: Software Engineer, ML Engineer, Data Scientist, etc.
- **ILP Resource Optimization**: Uses PuLP for optimal resource selection
- **Adaptive Quiz System**: Baseline assessment with skill inference
- **Progress Tracking**: Burndown charts, milestones, and persistence
- **Calendar Export**: ICS format for integration with calendar apps
- **Capstone Generation**: Automated project specifications
- **Course Management**: Full syllabus, weekly topics, assessments, textbooks

### Advanced Features
- **Multi-objective Optimization**: Balance time, cost, quality, and difficulty
- **Format Preferences**: Prioritize video, text, labs, or projects
- **Plan Comparison**: Compare up to 3 different roadmaps
- **Real-time Progress**: Track actual vs planned progress
- **Skill Prerequisites**: Automatic dependency resolution
- **Budget Constraints**: Stay within financial limits

## 🛠️ Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **PuLP**: Linear programming optimization
- **Pydantic**: Data validation and serialization
- **CORS**: Cross-origin resource sharing enabled

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **React Hooks**: Modern state management
- **SVG Charts**: Custom burndown visualizations

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
# or
yarn install
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

## 📚 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /majors` - List available majors
- `GET /roles` - List career roles
- `POST /plan` - Generate optimized roadmap

### Quiz System
- `POST /quiz/start` - Start baseline assessment
- `POST /quiz/grade` - Grade quiz and infer skills

### Progress Management
- `POST /progress/save` - Save progress data
- `GET /progress/load` - Load saved progress

### Export & Utilities
- `GET /export/ics` - Export calendar file
- `POST /capstone` - Generate capstone project

## 🎯 Usage Examples

### Generate a Roadmap

```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{
    "role": "ml_engineer",
    "weekly_hours": 15,
    "budget": 200,
    "prefer_formats": ["video", "projects"],
    "variant": "balanced"
  }'
```

### Start a Quiz

```bash
curl -X POST http://localhost:8000/quiz/start \
  -H "Content-Type: application/json" \
  -d '{
    "major": "cs",
    "num_items": 5
  }'
```

## 📊 Data Structure

### Skills
- 120+ skills across all majors
- Prerequisites and dependencies
- Difficulty levels (1-5)
- Tags for categorization

### Modules
- 32 learning modules
- Skill groupings
- Target hours
- Assessment methods
- Project ideas

### Resources
- Books, courses, videos
- Quality scores
- Time estimates
- Cost information
- Format types

### Roles
- Career-specific skill sets
- Industry-aligned paths
- Optimized sequences

## 🔧 Configuration

### Optimization Weights
- **Time Weight**: Prioritize shorter paths
- **Cost Weight**: Minimize expenses
- **Quality Weight**: Maximize resource quality
- **Difficulty Weight**: Control complexity

### Variants
- **Balanced**: Equal consideration of all factors
- **Fastest**: Minimize time to completion
- **Cheapest**: Minimize financial cost

## 📈 Progress Tracking

### Burndown Chart
- Visual representation of remaining work
- Planned vs actual progress
- Week-by-week tracking

### Milestones
- Automatic diagnostic points
- Skill completion markers
- Capstone project

### Persistence
- Save/load progress
- JSON-based storage
- Resume from any point

## 🎨 Frontend Features

### Tabbed Interface
- Configuration
- Quiz Assessment
- Roadmap View
- Progress Dashboard

### Interactive Elements
- Real-time updates
- Form validation
- Dynamic charts
- Responsive design

### Plan Comparison
- Side-by-side analysis
- Multiple variants
- Export options

## 🚢 Deployment

### Production Build

Backend:
```bash
cd backend
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

Frontend:
```bash
cd frontend
npm run build
npm start
```

### Docker Support

Create a `docker-compose.yml`:
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

## 📝 License

MIT License - Feel free to use for educational and commercial purposes.

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 🐛 Known Issues

- Quiz system currently limited to 5 questions per major
- Progress persistence uses local JSON (consider database for production)
- ICS export basic implementation (can be enhanced)

## 🔮 Future Enhancements

- [ ] User authentication system
- [ ] PostgreSQL database integration
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] AI-powered recommendations
- [ ] Social features (share roadmaps)
- [ ] Certificate generation
- [ ] Integration with learning platforms

## 📧 Support

For issues and questions, please open an issue on GitHub or contact the development team.

---

Built with ❤️ for lifelong learners