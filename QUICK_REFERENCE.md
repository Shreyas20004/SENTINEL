# Quick Reference - SENTINEL Phase 1

## 🚀 Get Started in 5 Minutes

### 1. Setup Environment

```bash
# Clone and navigate
git clone https://github.com/Shreyas20004/SENTINEL.git
cd SENTINEL

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup (new terminal)
cd frontend
npm install
```

### 2. Start Services

```bash
# In project root: Start Docker
docker-compose up -d

# Backend dev server (backend terminal)
cd backend
uvicorn app.main:app --reload

# Frontend dev server (frontend terminal)
cd frontend
npm run dev
```

### 3. Access

- **API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
- **Frontend:** http://localhost:5173
- **Postgres:** localhost:5432
- **Redis:** localhost:6379

---

## 📚 Essential Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `PHASE1_COMPLETION.md` | ✅ What's complete |
| `TESTING.md` | How to run tests |
| `docs/source/guide/quick-start.rst` | 10-min setup guide |
| `.env.example` | Environment variables template |
| `docker-compose.yml` | Service definitions |

---

## 🔧 Common Commands

### Backend

```bash
# Run tests
pytest tests/ -v

# Test with coverage
pytest tests/ --cov=app --cov-report=html

# Format code
black app/

# Type check
mypy app/

# Lint
flake8 app/
```

### Frontend

```bash
# Build
npm run build

# Lint
npm run lint

# Format
npm run format

# Test (after setup)
npm run test
```

### Docker

```bash
# Start all services
docker-compose up -d

# Stop all
docker-compose down

# View logs
docker-compose logs -f backend

# Restart specific service
docker-compose restart postgres
```

---

## 📊 API Quick Reference

### Incidents

```bash
# Get all
curl http://localhost:8000/api/v1/incidents

# Create
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "incident_type": "LOITERING",
    "severity": "HIGH",
    "zone_id": "zone_1",
    "description": "Test"
  }'

# Filter by severity
curl http://localhost:8000/api/v1/incidents?severity=HIGH

# Update status
curl -X PATCH http://localhost:8000/api/v1/incidents/{id} \
  -H "Content-Type: application/json" \
  -d '{"status": "RESOLVED"}'
```

### Alerts

```bash
# Get alerts
curl http://localhost:8000/api/v1/alerts

# Create alert with payload
curl -X POST http://localhost:8000/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": "incident_1",
    "camera_id": "cam_1",
    "alert_type": "MOTION",
    "severity": "MEDIUM",
    "confidence": 0.95
  }'
```

### Metrics

```bash
# Risk score
curl http://localhost:8000/api/v1/metrics/risk

# All metrics
curl http://localhost:8000/api/v1/metrics
```

### Cameras

```bash
# List cameras
curl http://localhost:8000/api/v1/cameras

# Create camera
curl -X POST http://localhost:8000/api/v1/cameras \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main Gate",
    "zone_id": "zone_1",
    "rtsp_url": "rtsp://...",
    "is_active": true
  }'
```

---

## 🧪 Testing Quick Start

```bash
cd backend

# Run all tests
pytest tests/

# Test specific endpoint
pytest tests/test_api.py::TestIncidentsAPI::test_create_incident -v

# View coverage
pytest tests/ --cov=app
open htmlcov/index.html  # macOS
```

---

## 📝 Project Structure

```
SENTINEL/
├── backend/
│   ├── app/
│   │   ├── main.py                 # Flask app
│   │   ├── api/                    # Route handlers
│   │   │   ├── incidents.py
│   │   │   ├── alerts.py
│   │   │   ├── metrics.py
│   │   │   ├── cameras.py
│   │   │   ├── zones.py
│   │   │   ├── dispatch.py
│   │   │   ├── reports.py
│   │   │   └── websocket.py        # ✅ NEW
│   │   ├── models/
│   │   │   ├── yolo_inference.py   # ✅ COMPLETE
│   │   │   ├── frame_capture.py    # ✅ COMPLETE
│   │   │   └── ...
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── redis_client.py
│   │   ├── models.py               # DB models
│   │   └── schemas.py              # Pydantic validators
│   ├── tests/
│   │   ├── test_api.py             # ✅ 20+ tests
│   │   ├── conftest.py             # ✅ Fixtures
│   │   └── pytest.ini              # ✅ Config
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CommandDashboard.tsx
│   │   │   ├── ThreatQueue.tsx
│   │   │   └── ...
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   └── websocket.ts
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                           # ✅ 28+ pages
│   ├── source/
│   │   ├── guide/
│   │   ├── api/
│   │   ├── developer/
│   │   └── roadmap/
│   └── conf.py
│
├── docker-compose.yml
├── README.md
├── PHASE1_COMPLETION.md            # ✅ This file
├── TESTING.md                      # ✅ Testing guide
└── requirements.txt
```

---

## 🚨 Troubleshooting

### Backend won't start

```
ERROR: Could not connect to database
```

**Fix:**
```bash
# Ensure Postgres is running
docker-compose up -d postgres
# Wait 10 seconds for init
sleep 10
uvicorn app.main:app --reload
```

### Frontend missing node_modules

```bash
cd frontend
npm install
npm run dev
```

### WebSocket connection fails

Check that Redis is running:
```bash
redis-cli ping  # Should return "PONG"
```

### Port already in use

```bash
# Find process on port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend
lsof -i :5432  # Postgres

# Kill it
kill -9 <PID>
```

---

## 🔗 Useful Resources

- **API Swagger Docs:** http://localhost:8000/docs
- **Postgres Admin:** `psql -U postgres -d sentinel`
- **Redis CLI:** `redis-cli`
- **React DevTools:** Install browser extension
- **Vite Docs:** https://vitejs.dev

---

## 📚 Next Steps

1. ✅ Phase 1 complete - see PHASE1_COMPLETION.md
2. 🔄 Start Phase 2 - ByteTrack tracking
3. 📖 Read docs/source/developer/setup.rst
4. 🧪 Run tests: `pytest tests/ -v`
5. 🚀 Deploy locally: `docker-compose up -d`

---

## 💡 Tips

- **Hot reload:** Both backend (Uvicorn) and frontend (Vite) support hot reload
- **Swagger playground:** Use /docs to test endpoints interactively
- **Logging:** Check docker logs: `docker-compose logs -f backend`
- **Database shell:** Connect with `psql sentinel`
- **Redis monitor:** Use `redis-cli MONITOR` to see pub/sub

---

**Version:** 1.0.0  
**Updated:** March 29, 2026  
**Status:** ✅ Phase 1 Complete

For more details, see `PHASE1_COMPLETION.md` and `docs/`
