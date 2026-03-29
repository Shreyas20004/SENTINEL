# SENTINEL Development Guide

This guide provides instructions for continuing SENTINEL development across all 4 phases.

## Current Status: Phase 1 ~50% Complete

**Completed:**
- ✅ Docker Compose infrastructure
- ✅ FastAPI application framework
- ✅ PostgreSQL + PostGIS database setup
- ✅ REST API endpoints (CRUD for incidents, alerts, cameras)
- ✅ React + Vite frontend skeleton
- ✅ API client service
- ✅ WebSocket service stub

**Remaining Phase 1:**
- ⏳ YOLOv8 model integration
- ⏳ OpenCV RTSP frame pipeline  
- ⏳ ByteTrack integration stub
- ⏳ Behavioural analytics rules engine
- ⏳ WebSocket alert streaming
- ⏳ Unit tests
- ⏳ Frontend component refinement

---

## Development Environment Setup

### Prerequisites
```bash
# Check versions
python --version       # 3.11+
node --version         # 20+
docker --version       # 24+
docker-compose --version  # 2.0+
```

### Initial Setup
```bash
# 1. Clone repository
cd SENTINEL

# 2. Copy environment file
cp backend/.env.example backend/.env

# 3. Start Docker containers
docker-compose up --build -d

# 4. Wait for services to be healthy
sleep 10

# 5. Verify
curl http://localhost:8000/health
```

### IDE Setup (VS Code)
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.formatOnSave": true
  },
  "redhat.telemetry.enabled": false
}
```

---

## Phase 1 Completion Tasks

### 1. Implement YOLOv8 Model Loading

Create `backend/app/models/yolo_inference.py`:

```python
"""YOLOv8 inference engine"""
import logging
from typing import List, Tuple
from ultralytics import YOLO
from app.core.config import settings

logger = logging.getLogger(__name__)

class YOLOv8Inference:
    def __init__(self):
        self.model = YOLO(settings.YOLO_MODEL_PATH)
        self.model.to('cuda' if settings.GPU_ENABLED else 'cpu')
    
    def predict(self, frame) -> dict:
        """Run inference on frame"""
        results = self.model.predict(
            frame,
            conf=settings.CONFIDENCE_THRESHOLD,
            iou=settings.IOU_THRESHOLD,
            verbose=False
        )
        
        detections = []
        for r in results:
            for box in r.boxes:
                detections.append({
                    'class_id': int(box.cls),
                    'class_name': r.names[int(box.cls)],
                    'confidence': float(box.conf),
                    'bbox': box.xyxy[0].tolist()
                })
        
        return {'detections': detections}

yolo_engine = YOLOv8Inference()
```

### 2. Implement OpenCV RTSP Capture

Create `backend/app/models/frame_capture.py`:

```python
"""OpenCV RTSP stream capture"""
import logging
import threading
from collections import deque
from datetime import datetime
import cv2

logger = logging.getLogger(__name__)

class RTSPCapture:
    def __init__(self, camera_id: str, rtsp_url: str, fps: int = 25):
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.fps = fps
        self.frame_buffer = deque(maxlen=128)
        self.is_running = False
        self.last_frame_time = None
    
    def start(self):
        """Start capture thread"""
        self.is_running = True
        thread = threading.Thread(target=self._capture_loop)
        thread.daemon = True
        thread.start()
    
    def _capture_loop(self):
        """Capture frames from RTSP stream"""
        cap = cv2.VideoCapture(self.rtsp_url)
        
        while self.is_running:
            ret, frame = cap.read()
            
            if not ret:
                logger.warning(f"Failed to read frame from {self.camera_id}")
                continue
            
            self.frame_buffer.append({
                'frame': frame,
                'timestamp': datetime.utcnow(),
                'camera_id': self.camera_id
            })
            
            # Maintain target FPS
            cv2.waitKey(1000 // self.fps)
        
        cap.release()
    
    def get_frame(self):
        """Get latest frame"""
        if self.frame_buffer:
            return self.frame_buffer[-1]
        return None
    
    def stop(self):
        """Stop capture thread"""
        self.is_running = False
```

### 3. Add WebSocket Alert Streaming

Update `backend/app/main.py`:

```python
from fastapi import WebSocket
import json

@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """WebSocket endpoint for real-time alerts"""
    await websocket.accept()
    
    # Subscribe to Redis channel
    pubsub = redis_client.client.pubsub()
    await pubsub.subscribe('sentinel:alerts')
    
    try:
        async for message in pubsub.listen():
            if message['type'] == 'message':
                alert_data = json.loads(message['data'])
                await websocket.send_json(alert_data)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await websocket.close()
```

### 4. Add Unit Tests

Create `backend/tests/test_api.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_create_camera():
    response = client.post(
        "/api/v1/cameras",
        json={
            "name": "Test Camera",
            "zone_id": "zone_1",
            "rtsp_url": "rtsp://test:554/stream"
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_metrics():
    response = client.get("/api/v1/metrics?window=1h")
    assert response.status_code == 200
    data = response.json()
    assert "uptime_percentage" in data
    assert "alerts_per_hour" in data
```

Run tests:
```bash
docker-compose exec backend pytest tests/ -v
```

---

## Phase 2 Preview: Intelligence

**Timeline:** Weeks 5-10

### Tasks
1. **ByteTrack Integration** (`app/models/bytetrack.py`)
   - Multi-object tracking across frames
   - Persistent track IDs
   - Velocity & dwell-time computation

2. **Behavioural Rules Engine** (`app/analytics/rules.py`)
   - Dwell time > 600s → Loitering
   - Zone count > threshold → Crowd surge
   - Unowned object > 300s → Abandoned object

3. **Alert Scoring** (`app/analytics/scoring.py`)
   - Scikit-learn rule ensemble
   - Severity ranking (HIGH/MED/LOW)
   - Duplicate suppression (MinHash)

4. **Kafka Integration** (`app/streaming/kafka.py`)
   - Event streaming to Kafka topics
   - Full audit log

5. **Dashboard Updates**
   - Real-time WebSocket updates
   - Risk dial animation
   - Live threat queue

### Key Files to Create
- `backend/app/models/bytetrack.py`
- `backend/app/analytics/rules.py`
- `backend/app/analytics/scoring.py`
- `backend/app/streaming/kafka.py`
- `frontend/src/hooks/useAlerts.ts`
- `frontend/src/hooks/useMetrics.ts`

---

## Phase 3 Preview: Geospatial

**Timeline:** Weeks 11-15

### Tasks
1. **GADM GeoJSON Integration**
   - Download India state/district boundaries
   - Render in Leaflet.js
   - Dynamic fill colors by risk

2. **PostGIS Spatial Queries**
   - Store incident geometries
   - ST_Within for region filtering
   - Sub-100ms query performance

3. **Geolocation & Reverse Geocoding**
   - Browser Geolocation API
   - Nominatim reverse geocoding
   - Emergency panel state lookup

4. **Dispatch Integration**
   - Direct tel: protocol URLs
   - Phone number mapping by state
   - Call logging to database

### Key Files to Create
- `data/gadm_india_states.geojson`
- `frontend/src/components/LiveMap.tsx` (full)
- `backend/app/api/geolocation.py`
- `backend/app/api/dispatch.py` (phase 3+)

---

## Phase 4 Preview: Hardening

**Timeline:** Weeks 16-20

### Tasks
1. **TensorRT Optimization**
   - Convert models to ONNX
   - TensorRT optimization
   - Benchmarking

2. **Monitoring & Observability**
   - Prometheus metrics
   - Grafana dashboards
   - Model drift detection

3. **Security Hardening**
   - JWT authentication
   - Role-based access control
   - API rate limiting

4. **Production Deployment**
   - Kubernetes Helm charts
   - Cloud deployment guides
   - Load testing (25 cameras @ 25 FPS)
   - Compliance audit trail

### Key Files to Create
- `backend/app/models/tensorrt_engine.py`
- `backend/app/monitoring/metrics.py`
- `backend/app/security/auth.py`
- `helm/sentinel/Chart.yaml`
- `k8s/sentinel-deployment.yaml`

---

## Code Style & Standards

### Python
```bash
# Format code
docker-compose exec backend black app/

# Sort imports
docker-compose exec backend isort app/

# Lint
docker-compose exec backend flake8 app/

# Type check
docker-compose exec backend mypy app/
```

### Frontend
```bash
# Format
cd frontend && npm run lint

# Type check
npm run type-check
```

### Commit Message Format
```
feat(scope): brief description

Longer description if needed.

Fixes #123
```

---

## Database Migrations

### Create Migration
```bash
docker-compose exec backend alembic revision --autogenerate -m "Add new column"
```

### Review Migration
```bash
cat backend/app/migrations/versions/XXX_*.py
```

### Apply Migration
```bash
docker-compose exec backend alembic upgrade head
```

### Rollback
```bash
docker-compose exec backend alembic downgrade -1
```

---

## Troubleshooting

### Port Already in Use
```bash
lsof -i :8000  # Check what's using port
kill -9 <PID>  # Kill process
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart
docker-compose restart postgres
```

### Memory Issues
```bash
# Check Docker memory
docker stats

# Increase Docker Desktop memory limits
# Settings → Resources → Memory → Increase to 8GB+
```

### Backend Won't Start
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Rebuild image
docker-compose build --no-cache backend

# Start with logs
docker-compose up backend
```

---

## Performance Profiling

### Backend Profiling
```python
# Add to route
from cProfile import Profile
from pstats import Stats
from io import StringIO

profiler = Profile()
profiler.enable()
# ... your code ...
profiler.disable()
stats = Stats(profiler, stream=StringIO())
stats.print_stats()
```

### Frontend Performance
```javascript
// Browser DevTools
console.time('metric-name');
// ... code ...
console.timeEnd('metric-name');
```

---

## Resources

### Documentation
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [React Docs](https://react.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [YOLOv8 Docs](https://docs.ultralytics.com/)
- [Leaflet.js Docs](https://leafletjs.com/)

### Testing
- [pytest Documentation](https://docs.pytest.org/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)

### Deployment
- [Docker Docs](https://docs.docker.com/)
- [Kubernetes Docs](https://kubernetes.io/docs/)

---

## Getting Help

- **Issues:** Create issue on GitHub with reproduction steps
- **Discussions:** Use GitHub Discussions for architecture questions
- **Code Review:** Submit PR even if incomplete for feedback

---

**Last Updated:** March 29, 2026  
**Version:** Phase 1 (50% complete)
