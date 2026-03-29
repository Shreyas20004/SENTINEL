# SENTINEL Documentation Index

Complete reference guide to SENTINEL documentation, source files, and development resources.

## 📚 Documentation

### Getting Started
- **[README.md](README.md)** - Project overview, architecture, core objectives
- **[PHASE1_SUMMARY.md](PHASE1_SUMMARY.md)** - Phase 1 implementation status (60% complete)
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Docker & deployment guide with troubleshooting
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Developer workflow, Phase 2-4 preview, testing

### API Reference
- **[API_EXAMPLES.md](API_EXAMPLES.md)** - cURL examples for all endpoints, batch testing

### Architecture
- **[SENTINEL_System_Architecture.pdf](SENTINEL_System_Architecture.pdf)** - Original spec document (attached)

---

## 🗂️ Project Structure

### Root Configuration
```
.gitignore                  # Git ignore patterns
docker-compose.yml         # Multi-service orchestration
PHASE1_SUMMARY.md          # Phase 1 status report
README.md                  # Main documentation
DEPLOYMENT.md              # Deployment guide
DEVELOPMENT.md             # Developer guide
API_EXAMPLES.md            # API usage examples
```

### Backend Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry
│   ├── models.py                  # SQLAlchemy ORM models
│   ├── schemas.py                 # Pydantic validation schemas
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── database.py            # PostgreSQL setup
│   │   └── redis_client.py        # Redis pub/sub client
│   ├── api/
│   │   ├── __init__.py
│   │   ├── incidents.py           # Incident CRUD endpoints
│   │   ├── alerts.py              # Alert creation & listing
│   │   ├── metrics.py             # System metrics endpoints
│   │   ├── zones.py               # Zone management (Phase 3)
│   │   ├── cameras.py             # Camera registration
│   │   ├── dispatch.py            # Emergency dispatch (Phase 3)
│   │   └── reports.py             # Report generation (Phase 4)
│   ├── models/                    # AI/ML models
│   │   ├── __init__.py
│   │   ├── yolo_inference.py      # YOLOv8 detector (Phase 2)
│   │   ├── frame_capture.py       # RTSP capture (Phase 2)
│   │   └── tracking.py            # ByteTrack tracker (Phase 2)
│   └── analytics/                 # Behavioral analytics
│       ├── __init__.py
│       ├── rules.py               # Rules engine (Phase 2)
│       └── scoring.py             # Alert scoring (Phase 2)
├── .env.example                   # Environment template
├── requirements.txt               # Python dependencies
└── Dockerfile                     # Backend container
```

### Frontend Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── CommandDashboard.tsx   # Main operator dashboard
│   │   ├── ThreatQueue.tsx        # Real-time incident list
│   │   ├── MetricsCard.tsx        # Risk dial & KPIs
│   │   ├── CameraGrid.tsx         # Camera status grid
│   │   └── LiveMap.tsx            # Geospatial map (Phase 3)
│   ├── services/
│   │   ├── api.ts                 # API client
│   │   └── websocket.ts           # WebSocket service
│   ├── App.tsx                    # Main app component
│   ├── main.tsx                   # React entry point
│   ├── index.css                  # Global styles
│   └── config.ts                  # Frontend config
├── vite.config.ts                 # Vite build config
├── vite-env.d.ts                  # Type definitions
├── tsconfig.json                  # TypeScript config
├── tsconfig.node.json             # Node TypeScript config
├── tailwind.config.js             # Tailwind CSS config
├── package.json                   # NPM dependencies
├── index.html                     # HTML entry point
└── Dockerfile                     # Frontend container
```

---

## 🗄️ Database Schema

### Core Tables
- **cameras** - RTSP stream registry (12 fields)
- **zones** - Geographic regions with PostGIS geometry (5 fields)
- **incidents** - Aggregated threat events (14 fields)
- **alerts** - Frame-level detections (10 fields)
- **detections** - Raw YOLOv8 output (7 fields)
- **metrics** - System KPIs (5 fields)

All tables have proper indexing and timestamps.

---

## 🔌 API Endpoints

### Incidents (`GET, POST, PATCH`)
- `POST /api/v1/incidents` - Create
- `GET /api/v1/incidents` - List (with filters)
- `GET /api/v1/incidents/{id}` - Get one
- `PATCH /api/v1/incidents/{id}` - Update

### Alerts (`GET, POST`)
- `POST /api/v1/alerts` - Create (from inference)
- `GET /api/v1/alerts` - List recent

### Metrics (`GET`)
- `GET /api/v1/metrics?window={1h,6h,24h,7d}` - System metrics
- `GET /api/v1/metrics/risk-dial` - Real-time risk gauge

### Cameras (`GET, POST, PATCH`)
- `GET /api/v1/cameras` - List with filters
- `POST /api/v1/cameras` - Register camera
- `PATCH /api/v1/cameras/{id}` - Update config

### Zones (`GET`)
- `GET /api/v1/zones` - List zones
- `GET /api/v1/zones/{id}` - Get specific zone

### Dispatch (`POST`)
- `POST /api/v1/dispatch/escalate` - Escalate alerts (Phase 3)

### Reports (`POST`)
- `POST /api/v1/reports/generate` - Generate PDF (Phase 4)

### Health (`GET`)
- `GET /health` - Health check

---

## 🎯 Implementation Phases

### Phase 1: Foundation (Weeks 1-4) — 60% COMPLETE
**Status:** Core API, database, UI shell  
**Completed:** Docker, FastAPI, models, REST API, React components  
**Remaining:** YOLOv8 loading, RTSP capture, WebSocket streaming, tests  
**Effort:** ~1 week remaining  

**Key Files:**
- [backend/app/main.py](backend/app/main.py)
- [backend/app/core/database.py](backend/app/core/database.py)
- [frontend/src/App.tsx](frontend/src/App.tsx)

---

### Phase 2: Intelligence (Weeks 5-10) — NOT STARTED
**Focus:** Real-time detection & event processing  
**Deliverables:** ByteTrack, rules engine, alert scoring, Kafka, WebSocket updates  

**Key Files (Stubs):**
- [backend/app/models/yolo_inference.py](backend/app/models/yolo_inference.py)
- [backend/app/models/frame_capture.py](backend/app/models/frame_capture.py)
- [backend/app/models/tracking.py](backend/app/models/tracking.py)
- [backend/app/analytics/rules.py](backend/app/analytics/rules.py)
- [backend/app/analytics/scoring.py](backend/app/analytics/scoring.py)

---

### Phase 3: Geospatial (Weeks 11-15) — NOT STARTED
**Focus:** Spatial awareness & emergency dispatch  
**Deliverables:** Leaflet.js map, PostGIS queries, Geolocation, SOS panel, tel: dispatch  

**Key Files (TODO):**
- frontend/src/components/LiveMap.tsx (full implementation)
- backend/app/api/geolocation.py (new)

---

### Phase 4: Hardening (Weeks 16-20) — NOT STARTED
**Focus:** Production-readiness & compliance  
**Deliverables:** TensorRT, Prometheus, Grafana, RBAC, Kubernetes, load testing  

**Key Files (TODO):**
- backend/app/models/tensorrt_engine.py (new)
- backend/app/security/auth.py (new)
- helm/ folder (new)

---

## 🧪 Testing

### Backend Tests
```bash
# Unit tests
docker-compose exec backend pytest app/tests/unit/ -v

# Integration tests
docker-compose exec backend pytest app/tests/integration/ -v

# All tests
docker-compose exec backend pytest -v
```

### Frontend Tests
```bash
cd frontend
npm test
npm run type-check
```

### API Testing
```bash
# See API_EXAMPLES.md for curl examples
bash test.sh  # Batch test script
```

---

## 🚀 Quick Reference

### Start Development
```bash
docker-compose up --build -d
curl http://localhost:8000/health
# Open http://localhost:5173
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f frontend
```

### Database Access
```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U sentinel -d sentinel_db

# List tables
\dt

# Redis CLI
docker-compose exec redis redis-cli
```

### Create Test Camera
```bash
curl -X POST http://localhost:8000/api/v1/cameras \
  -H "Content-Type: application/json" \
  -d '{
    "name":"CAM-01",
    "zone_id":"zone_1",
    "rtsp_url":"rtsp://192.168.1.100:554/stream"
  }'
```

### Get Metrics
```bash
curl http://localhost:8000/api/v1/metrics?window=1h | jq
```

---

## 📖 Reading Guide

### For Project Managers
1. Read [README.md](README.md) - Overview & architecture
2. Read [PHASE1_SUMMARY.md](PHASE1_SUMMARY.md) - Current status
3. Review implementation roadmap timeline

### For Architects
1. Read [README.md](README.md) - System architecture (Section 02)
2. Read [DEVELOPMENT.md](DEVELOPMENT.md) - Code structure & patterns
3. Review database schema in [backend/app/models.py](backend/app/models.py)

### For Backend Developers
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) - Setup & workflow
2. Review [API_EXAMPLES.md](API_EXAMPLES.md) - API patterns
3. Study [backend/app/api/incidents.py](backend/app/api/incidents.py) - Example endpoint
4. Check Phase 2 stubs for implementation tasks

### For Frontend Developers
1. Read [DEVELOPMENT.md](DEVELOPMENT.md) - Setup & testing
2. Review [frontend/src/services/api.ts](frontend/src/services/api.ts) - API client
3. Study component files in frontend/src/components/
4. Check Phase 3 stubs for map implementation

### For DevOps/Infrastructure
1. Read [DEPLOYMENT.md](DEPLOYMENT.md) - Docker & deployment
2. Review [docker-compose.yml](docker-compose.yml) - Service definitions
3. Check Phase 4 section for Kubernetes/cloud guides

---

## 🎓 Architecture Decision Log

| Decision | Rationale | Status |
|----------|-----------|--------|
| FastAPI + async | Native WebSocket, fast, modern Python | ✅ Implemented |
| PostgreSQL + PostGIS | Spatial queries, proven, open-source | ✅ Implemented |
| Docker Compose | Dev/prod parity, reproducible | ✅ Implemented |
| React 18 + TypeScript | Type safety, Concurrent rendering | ✅ Implemented |
| Tailwind CSS | Dark theme ready, utility-first | ✅ Implemented |
| YOLOv8 | 80+ FPS, Apache 2.0, free | ⏳ Phase 2 |
| ByteTrack | Better than SORT, Phase 2 | ⏳ Phase 2 |
| Leaflet.js | No API key, 100% open-source | ⏳ Phase 3 |
| Kubernetes | Scalability, Phase 4 | ⏳ Phase 4 |

---

## 💾 File Statistics

### Backend
- **Python Files:** 21 (main.py, models.py, 7 API routers, 5 core modules, 4 analytics, __init__ files)
- **Configuration:** 3 (.env.example, Dockerfile, requirements.txt)
- **Lines of Code:** ~2,500 (well-documented with Type hints)

### Frontend
- **TypeScript Files:** 12 (5 components, 2 services, App, main, config)
- **Configuration:** 5 (vite.config.ts, tsconfig.json, tailwind.config.js, package.json, index.html)
- **CSS:** styles.css with Tailwind
- **Lines of Code:** ~1,200 (React components + API client)

### Documentation
- **Markdown Files:** 6 (README, PHASE1_SUMMARY, DEVELOPMENT, DEPLOYMENT, API_EXAMPLES, this INDEX)
- **Total Words:** ~15,000

---

## 🔗 External Resources

### Official Docs
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PostgreSQL & PostGIS](https://postgis.net/)
- [React 18](https://react.dev/)
- [YOLOv8](https://docs.ultralytics.com/)
- [Leaflet.js](https://leafletjs.com/)

### Papers & References
- ByteTrack: [arxiv.org/abs/2110.06864](https://arxiv.org/abs/2110.06864)
- YOLOv8: [arxiv.org/abs/2305.09972](https://arxiv.org/abs/2305.09972)

### Standards
- [PDPB 2023](https://www.meity.gov.in/data-protection-bill) (Privacy)
- [IT Act 2000](https://www.meity.gov.in/it-act-2000) (Compliance)
- [NDMA Guidelines](http://ndma.gov.in/) (Disaster Management)

---

## ✅ Verification Checklist

Before starting Phase 2, verify:

- [ ] Docker containers all healthy (`docker-compose ps`)
- [ ] Backend API responds (`curl http://localhost:8000/health`)
- [ ] Frontend loads (`http://localhost:5173`)
- [ ] PostgreSQL has tables (`\dt` in psql)
- [ ] Redis pub/sub works (`redis-cli PUBLISH test 'hello'`)
- [ ] Can create camera via API
- [ ] Can list incidents via API
- [ ] Frontend metrics display

---

## 📞 Getting Help

- **Questions?** Check corresponding .md file
- **Code Example?** See [API_EXAMPLES.md](API_EXAMPLES.md)
- **Bug Report?** Create GitHub issue with logs
- **Feature Request?** Discuss in GitHub Discussions
- **Architecture Question?** Post in Discussions

---

**Last Updated:** March 29, 2026  
**Version:** 1.0.0-alpha (Phase 1 - 60% Complete)
