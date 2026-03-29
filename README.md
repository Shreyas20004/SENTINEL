# SENTINEL - Public Safety AI System

**A real-time threat detection, live mapping, and emergency dispatch platform for public safety infrastructure.**

## 📋 Project Overview

SENTINEL is an open-source, multi-layer AI platform designed for Indian public safety infrastructure. It ingests video feeds from IP CCTV cameras, applies real-time computer vision (YOLOv8), and surfaces actionable intelligence through a command dashboard and geospatial threat map.

**Version:** 1.0.0  
**Status:** Phase 1 - Foundation (Development)  
**Compliance:** IT Act 2000 · PDPB 2023 · NDMA Guidelines

---

## 🎯 Core Objectives

| Objective | Description |
|-----------|-------------|
| **Detect** | Identify threats (perimeter breaches, abandoned objects, crowd surges, loitering) from CCTV at real-time inference speed (<50 ms/frame) |
| **Assess** | Compute per-zone risk scores, rank alerts by severity, suppress duplicates to prevent operator fatigue |
| **Communicate** | Deliver a live threat map consumable by field officers and command centres with self-updating incident timelines |
| **Dispatch** | Enable one-touch escalation to correct emergency authority (112, 181, 100, 108, 1098) based on operator geolocation |
| **Learn** | Continuously retrain models on confirmed-positive events to reduce false-positive rates over time |

---

## 🏗️ System Architecture

SENTINEL is organized into **5 horizontal layers**, each independently scalable and replaceable:

```
Layer 5 —— Presentation (React + Vite + Leaflet.js)
Layer 4 —— Application API (FastAPI + WebSocket + Redis Pub/Sub)
Layer 3 —— AI Inference Engine (YOLOv8 + ByteTrack + OSNet + Scikit-learn)
Layer 2 —— Data Ingestion (OpenCV + FFmpeg + ONNX + Kafka)
Layer 1 —— Data Sources (IP CCTV · NCRB Open Data · GADM GeoJSON · OSM)
```

---

## 📦 Technology Stack

### Backend
- **Framework:** FastAPI (Python 3.11)
- **Real-time:** Redis Pub/Sub, WebSockets, Celery
- **Database:** PostgreSQL 16 + PostGIS, Redis (cache)
- **Async:** asyncio, asyncpg

### Frontend
- **UI Framework:** React 18 + Vite
- **Mapping:** Leaflet.js + OpenStreetMap
- **Styling:** Tailwind CSS
- **Charts:** Chart.js
- **Real-time:** Socket.IO Client

### AI/ML
- **Detection:** YOLOv8 (Ultralytics)
- **Tracking:** ByteTrack, DeepSORT
- **Re-ID:** OSNet (torchreid)
- **Optimization:** ONNX Runtime, TensorRT
- **Analytics:** Scikit-learn

### DevOps
- **Containerization:** Docker + Docker Compose
- **Server:** Uvicorn, Gunicorn, NGINX
- **Monitoring:** Prometheus, Grafana
- **CI/CD:** GitHub Actions

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for frontend development)
- Python 3.11+ (for backend development)
- GPU (NVIDIA/CUDA) optional but recommended

### 1. Clone & Setup
```bash
cd SENTINEL
docker-compose up -d
```

This starts:
- **Backend API:** http://localhost:8000
- **Frontend UI:** http://localhost:5173
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

### 2. Verify System Health
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy", "version": "1.0.0"}
```

### 3. Access UI
Open browser to **http://localhost:5173**

### 4. Create Test Camera
```bash
curl -X POST http://localhost:8000/api/v1/cameras \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CAM-01",
    "zone_id": "zone_1",
    "location": "Main Gate",
    "rtsp_url": "rtsp://camera-ip:554/stream"
  }'
```

---

## 📋 Implementation Roadmap

### Phase 1 — Foundation (Weeks 1–4) ✅ In Progress
- [ ] Docker Compose stack (FastAPI + PostgreSQL + Redis)
- [ ] OpenCV RTSP ingestion & frame pipeline
- [ ] YOLOv8 weights integration
- [ ] Basic REST API (GET /incidents, POST /alerts, GET /metrics)
- [ ] React shell with placeholder dashboard
- [ ] Database initialization script

**Status:** ~50% complete

### Phase 2 — Intelligence (Weeks 5–10)
- [ ] ByteTrack multi-object tracking
- [ ] Behavioural rules engine (loitering, crowd surge, abandoned object)
- [ ] Alert scoring, deduplication, severity ranking
- [ ] Kafka integration for audit log
- [ ] Dashboard WebSocket real-time updates
- [ ] Risk dial animation

### Phase 3 — Geospatial (Weeks 11–15)
- [ ] GADM GeoJSON state/district polygons → Leaflet
- [ ] PostGIS spatial query endpoint (/incidents?region=)
- [ ] Browser Geolocation API + Nominatim reverse geocoding
- [ ] Dynamic emergency helpline panel (state-keyed)
- [ ] tel: protocol dispatch integration
- [ ] Call logging

### Phase 4 — Hardening (Weeks 16–20)
- [ ] TensorRT model optimization
- [ ] Prometheus + Grafana monitoring
- [ ] Role-based access control (admin, operator, viewer)
- [ ] Load testing (25 concurrent cameras @ 25 FPS)
- [ ] PDPB 2023 compliance review
- [ ] Production deployment guide

---

## 📚 API Reference

### Incidents
```
GET    /api/v1/incidents?region=&severity=&limit=100     List incidents
GET    /api/v1/incidents/{incident_id}                   Get incident
POST   /api/v1/incidents                                 Create incident
PATCH  /api/v1/incidents/{incident_id}                   Update incident
```

### Alerts
```
POST   /api/v1/alerts                    Create alert (from inference)
GET    /api/v1/alerts?incident_id=&limit=50  List alerts
```

### Metrics
```
GET    /api/v1/metrics?window=1h         System metrics (uptime, alerts/hr, response time)
GET    /api/v1/metrics/risk-dial         Real-time risk dial data
```

### Cameras
```
GET    /api/v1/cameras?zone=&active_only=false  List cameras
POST   /api/v1/cameras                         Register camera
PATCH  /api/v1/cameras/{camera_id}             Update camera
```

### Dispatch
```
POST   /api/v1/dispatch/escalate        Escalate HIGH alerts to supervisor
```

### Reports
```
POST   /api/v1/reports/generate         Generate signed PDF report
```

---

## 🗄️ Database Schema

### Core Tables
- **cameras** — CCTV streams with heartbeat tracking
- **zones** — Geographical regions with risk scores & PostGIS geometry
- **incidents** — Aggregated threat events with timeline
- **alerts** — Low-level detections (frame-level)
- **detections** — YOLOv8 raw output (audio trail)

### Indexing
All tables indexed by severity, zone, timestamp for sub-100ms spatial queries.

---

## 🔐 Security & Compliance

### Privacy-First Design
- **Zero facial recognition:** All detection is behaviour-based & object-based
- **PDPB 2023 compliant:** Data minimisation, audit trails, deletion policies
- **Operator anonymity:** User location + geolocation, not identity
- **No vendor lock-in:** 100% open-source or publicly licensed

### Authentication (Phase 4)
- JWT-based role-based access control (admin, operator, viewer)
- API key authentication for inference engines
- SSL/TLS in production

---

## 📊 Deployment Targets

| Environment | Stack | Status |
|-------------|-------|--------|
| **Local / Dev** | Docker Compose (MacOS, Linux, Windows) | ✅ Ready |
| **Kubernetes** | Helm charts (coming Phase 4) | 📋 Planned |
| **Cloud** | AWS ECS, GCP GKE, Azure ACS (coming Phase 4) | 📋 Planned |
| **On-Prem** | Docker Swarm, bare metal (coming Phase 4) | 📋 Planned |

---

## 🤝 Contributing

SENTINEL is open-source under the MIT License. Contributions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

MIT License - see [LICENSE.md](LICENSE.md) for details.

---

## 💬 Questions?

- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** sentinel-admin@example.local

---

## ⚡ Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| **Detection Latency** | <50 ms/frame | 📋 Phase 2 |
| **Detection-to-Dispatch** | <60 seconds | 📋 Phase 3 |
| **Alert Precision** | >90% | 📋 Phase 2 |
| **System Uptime** | >99.5% | 📋 Phase 4 |
| **Concurrent Cameras** | 25 @ 25 FPS | 📋 Phase 4 |

---

**Last Updated:** March 29, 2026  
**Status:** Phase 1 - Foundation (In Progress)
