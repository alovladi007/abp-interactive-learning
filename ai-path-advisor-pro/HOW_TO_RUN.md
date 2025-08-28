# 🚀 How to Run AI Path Advisor Pro

## ✅ Quick Start (Two Terminal Windows)

### Terminal 1: Backend Server
```bash
cd /workspace/ai-path-advisor-pro
./run_backend.sh
```

Or manually:
```bash
cd /workspace/ai-path-advisor-pro/backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/workspace/ai-path-advisor-pro/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [####] using WatchFiles
INFO:     Started server process [####]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Terminal 2: Frontend Server
```bash
cd /workspace/ai-path-advisor-pro
./run_frontend.sh
```

Or manually:
```bash
cd /workspace/ai-path-advisor-pro/frontend
npm run dev
```

**Expected output:**
```
> ai-path-advisor-frontend-pro@0.2.0 dev
> next dev -p 3000

   ▲ Next.js 14.2.5
   - Local:        http://localhost:3000
   - Network:      http://[your-ip]:3000

 ✓ Starting...
 ✓ Ready in 2.5s
```

## 🌐 Access Points

Once both servers are running:

1. **Frontend Application**: http://localhost:3000
2. **Backend API**: http://localhost:8000
3. **API Documentation**: http://localhost:8000/docs

## 🧪 Test the Setup

### Test Backend API:
```bash
curl http://localhost:8000/
```

Should return:
```json
{
  "name": "AI Path Advisor Pro",
  "version": "2.0.0",
  "features": [...]
}
```

### Test Roles Endpoint:
```bash
curl http://localhost:8000/roles
```

### Test Plan Generation:
```bash
curl -X POST http://localhost:8000/plan \
  -H "Content-Type: application/json" \
  -d '{
    "role": "software_engineer",
    "weekly_hours": 10,
    "budget": 100,
    "variant": "balanced"
  }'
```

## 🔧 Troubleshooting

### Issue: "Port already in use"
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Issue: "Module not found"
```bash
# Reinstall backend dependencies
cd /workspace/ai-path-advisor-pro/backend
pip install --break-system-packages fastapi uvicorn pydantic pulp

# Reinstall frontend dependencies
cd /workspace/ai-path-advisor-pro/frontend
npm install
```

### Issue: "Cannot connect to backend"
Make sure:
1. Backend is running on port 8000
2. Frontend is running on port 3000
3. No firewall blocking the ports

## 📱 Using the Application

1. **Open Browser**: Navigate to http://localhost:3000

2. **Configuration Tab**:
   - Select Career Role or Academic Major
   - Set study hours and budget
   - Choose preferred learning formats
   - Adjust optimization weights

3. **Quiz Tab**:
   - Take baseline assessment
   - System will infer your existing skills

4. **Generate Roadmap**:
   - Click "Generate Roadmap" button
   - View your personalized learning path

5. **Progress Tab**:
   - Track your weekly progress
   - View burndown chart
   - Save/load your progress

## 🎯 Quick Test Workflow

1. Start both servers (backend & frontend)
2. Open http://localhost:3000
3. Select "Software Engineer" role
4. Set 15 hours/week, $200 budget
5. Click "Generate Roadmap"
6. View your personalized plan!

## 💡 Tips

- Use Chrome DevTools (F12) to debug frontend issues
- Check backend logs in Terminal 1 for API errors
- The API docs at http://localhost:8000/docs are interactive
- All data is stored in `/backend/data/*.json` files

## 🛑 Stopping the Servers

- **Backend**: Press `Ctrl+C` in Terminal 1
- **Frontend**: Press `Ctrl+C` in Terminal 2

## 📝 Notes

- Backend runs on port 8000
- Frontend runs on port 3000
- Both servers support hot-reload (automatic restart on file changes)
- Progress is saved to `/backend/data/progress.json`

---

If you still have issues, check the detailed logs in each terminal window!