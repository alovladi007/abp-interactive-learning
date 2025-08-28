# E.U.R.E.K.A Interactive Learning Platform - Repository Contents

## Branch Structure
✅ **Single Branch: main** - All content consolidated here

## Major Components

### 1. AI Path Advisor System (NEW)
Complete personalized learning roadmap generator with:

#### Files:
- `ai-path-advisor.html` - Original UI
- `ai-path-advisor-improved.html` - **Enhanced UI with better navigation**
- `path-advisor.js` - Frontend JavaScript
- `create-ai-path-advisor-kit.py` - System generator script
- `extend-ai-path-advisor.py` - Extension script for new majors

#### Full Stack Implementation:
- `ai-path-advisor-starter/` - Complete backend and frontend
  - `backend/` - FastAPI server with quiz system
    - `main.py` - API endpoints for path planning and quizzes
    - `data/skills.json` - 90+ skills across 6 majors
    - `data/modules.json` - 20+ learning modules
    - `data/resources.json` - 80+ curated resources
  - `frontend/` - Next.js application
    - `app/page.tsx` - Interactive UI with quiz integration

#### Features:
- **6 Academic Majors**: CS, EE, Physics, Data Science, Public Health, Materials Science
- **10+ Career Paths per Major**
- **Quiz System** for baseline assessment
- **Personalized Roadmap Generation**
- **Resource Recommendations** (books, courses, videos)

### 2. QBank System
Advanced question bank with adaptive testing:

#### Files:
- `qbank-platform.html` - Main QBank interface
- `qbank-admin.html` - Admin dashboard
- `qbank-advanced.html` - Advanced features
- `qbank-integrated.html` - Integrated version
- `qbank-working.html` - Working implementation
- `qbank-v10/` - Latest version with IRT engine
- `qbank-backend/` - Backend implementation

#### Features:
- 5000+ questions across multiple subjects
- IRT (Item Response Theory) adaptive testing
- PostgreSQL database integration
- Admin dashboard for question management
- Docker Compose deployment

### 3. Core Platform
- `index.html` - Main landing page
- `dashboard.html` - Student dashboard
- `dashboard.css` - Dashboard styles
- `dashboard.js` - Dashboard functionality
- `academic-setup.html` - Academic profile setup with Louis AI Advisor

### 4. Learning Resources
- `library.html` - Digital library
- `marketplace.html` - Course marketplace
- `prep-courses.html` - Test prep courses
- `tutoring-videos.html` - Video tutorials
- `certifications.html` - Certification programs

### 5. Additional Features
- `ai-generator.html` - AI content generator
- `quizzes.html` - Quiz system
- `partners.html` - Partner institutions
- `corporate.html` - Corporate training hub
- `pricing.html` - Subscription plans

### 6. Infrastructure
- `docker-compose.yml` - Container orchestration
- `Dockerfile` - Container configuration
- `nginx.conf` - Web server configuration
- `Makefile` - Build automation
- `backend/` - Backend services
- Various deployment guides and documentation

## Recent Updates
1. ✅ Added AI Path Advisor with 6 majors and personalized roadmaps
2. ✅ Integrated Public Health and Materials Science majors
3. ✅ Implemented quiz system for skill assessment
4. ✅ Enhanced UI with better navigation (majors upfront)
5. ✅ Consolidated all branches into main
6. ✅ Preserved all existing QBank and platform features

## Total Statistics
- **158 files** in repository
- **6 academic majors** supported
- **90+ skills** in knowledge graph
- **80+ learning resources** curated
- **5000+ quiz questions** in QBank
- **10+ career paths** available

## Access
Repository: https://github.com/alovladi007/abp-interactive-learning
Branch: main (single branch)

All content is preserved and accessible from the main branch.