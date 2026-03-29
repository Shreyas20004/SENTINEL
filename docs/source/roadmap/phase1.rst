.. _roadmap-phase1:

============
Phase 1: Foundation
============

Details on Phase 1 implementation and current status.

Phase 1 Objectives
===================

✅ **Complete** (60% total):

1. **Infrastructure Setup** (100%)
   - Docker Compose orchestration ✅
   - PostgreSQL + PostGIS ✅
   - Redis pub/sub ✅
   - Backend + Frontend containers ✅

2. **API Framework** (100%)
   - FastAPI async foundation ✅
   - 14+ REST endpoints ✅
   - Pydantic validation ✅
   - OpenAPI auto-docs ✅

3. **Database Schema** (100%)
   - 6 normalized tables ✅
   - Spatial indexing ✅
   - Proper relationships ✅
   - Audit trail ready ✅

4. **Frontend Shell** (100%)
   - React + TypeScript ✅
   - Component architecture ✅
   - Tailwind styling ✅
   - Routing structure ✅

⏳ **Remaining** (40% total):

5. **YOLOv8 Model Integration** (0%)
   - Skeleton: yolo_inference.py
   - Task: Load model, run inference
   - Est. effort: 20-40 hours

6. **OpenCV RTSP Capture** (0%)
   - Skeleton: frame_capture.py
   - Task: Implement frame buffering
   - Est. effort: 15-30 hours

7. **WebSocket Real-time Streaming** (0%)
   - Skeleton: websocket.ts
   - Task: Implement FastAPI WebSocket endpoint
   - Est. effort: 10-20 hours

8. **Unit Tests** (0%)
   - Task: pytest suite for all APIs
   - Target: >80% coverage
   - Est. effort: 20-30 hours

Completed Components
====================

**Backend (`backend/app/main.py`)**

- FastAPI application with lifespan management
- Health check endpoint
- CORS middleware configured
- 7 API routers included
- Production-ready error handling

**Core Modules**

- `config.py`: Environment-based settings
- `database.py`: AsyncSession factory, PostGIS init
- `redis_client.py`: Pub/Sub wrapper
- `models.py`: 6 SQLAlchemy ORM tables
- `schemas.py`: Pydantic validation models

**API Endpoints**

.. list-table::
   :widths: 25 40
   :header-rows: 1

   * - Module
     - Operations
   * - **incidents.py**
     - GET /incidents, GET /incidents/{id}, POST, PATCH
   * - **alerts.py**
     - GET /alerts, POST (with Redis publishing)
   * - **metrics.py**
     - GET /metrics, GET /metrics/risk-dial
   * - **cameras.py**
     - GET /cameras, POST, PATCH
   * - **zones.py**
     - GET /zones, GET /zones/{id}
   * - **dispatch.py**
     - POST /dispatch/escalate (stub)
   * - **reports.py**
     - POST /reports/generate (stub)

**Frontend**

- React 18 + TypeScript project structure
- 5 components: CommandDashboard, ThreatQueue, MetricsCard, CameraGrid, LiveMap
- API client service (axios wrapper)
- WebSocket service skeleton
- React Router v6 navigation
- Tailwind CSS dark theme

**Documentation**

- README.md (architecture + roadmap)
- DEPLOYMENT.md (operational guide)
- DEVELOPMENT.md (dev workflow)
- API_EXAMPLES.md (curl recipes)
- PHASE1_SUMMARY.md (status report)
- INDEX.md (navigation guide)
- ReadTheDocs infrastructure (Sphinx config)
- 10+ guide pages

Remaining Phase 1 Work
======================

**High Priority (by dependency order):**

1. **YOLOv8 Model Loading** (5 days)

   File: `backend/app/ai/yolo_inference.py`

   Tasks:
   - Load YOLOv8 pretrained model from cache/hub
   - Implement predict() with batch processing
   - Support CPU + GPU mode
   - Return consistent format: {class_id, class_name, confidence, bbox, track_id}
   - Optimize inference <50ms on GPU

   Tests: Verify on COCO sample image

2. **OpenCV RTSP Capture** (5 days)

   File: `backend/app/ai/frame_capture.py`

   Tasks:
   - Implement cv2.VideoCapture with RTSP URL
   - Ring buffer (128 frames)
   - FPS control (match camera FPS)
   - Error handling for stream interruptions
   - Heartbeat monitoring
   - Thread-safe frame access

   Tests: Test with public RTSP streams

3. **WebSocket Real-time Alerts** (3 days)

   File: `backend/app/main.py` + `frontend/src/services/websocket.ts`

   Tasks:
   - Add FastAPI @app.websocket("/ws/alerts") endpoint
   - Subscribe to Redis channel
   - Forward to connected clients
   - Auto-reconnection on client side
   - Connection lifecycle management

   Tests: Test with multiple concurrent WebSocket clients

4. **Unit Test Suite** (5 days)

   Directory: `backend/tests/`

   Tests needed:
   - 30+ pytest cases for API endpoints
   - Database operation tests
   - Mock tests for external dependencies
   - Target: >80% code coverage

   Tests: Run with ``pytest -v --cov``

**Medium Priority:**

5. **Frontend WebSocket Integration** (2 days)
   - Connect to WebSocket endpoint
   - Display real-time alerts in ThreatQueue
   - Animated notifications

6. **Performance Testing** (2 days)
   - Latency profiling (target <250ms)
   - Throughput testing (10 concurrent cameras)
   - Load testing (1000 concurrent API requests)

7. **Documentation Updates** (1 day)
   - Add example request/response to each endpoint
   - Troubleshooting guide
   - Performance tuning guide

Timeline
========

Recommended Phase 1 completion timeline (assuming 2-person team):

.. list-table::
   :widths: 15 50
   :header-rows: 1

   * - Week
     - Tasks
   * - **Week 1** (Done)
     - Infrastructure, API framework, database
   * - **Week 2** (Done)
     - Frontend shell, documentation
   * - **Week 3** (Current)
     - YOLOv8 + OpenCV skeleton
   * - **Week 4**
     - Model training, frame capture implementation
   * - **Week 5**
     - WebSocket endpoint, real-time streaming
   * - **Week 6**
     - Unit tests, performance optimization
   * - **Week 7**
     - Bug fixes, documentation polish
   * - **Week 8**
     - Phase 1 completion, Phase 2 planning

**Target Phase 1 Completion: Week 8 (2 months from start)**

Success Criteria
================

Phase 1 is complete when:

✅ All 7 endpoints functional with >95% uptime

✅ YOLOv8 inference <50ms on GPU (or <100ms on CPU)

✅ Frame capture from 10+ cameras simultaneously

✅ Real-time alert streaming via WebSocket <200ms latency

✅ Unit tests >80% code coverage

✅ All documentation current and tested

✅ Zero critical bugs in production

✅ Docker-based deployment working in <5 minutes

Known Limitations (Phase 1)
===========================

1. **No facial recognition** (intentional, privacy-first)
2. **Single machine deployment** (scale in Phase 2)
3. **No authentication** (added Phase 4)
4. **Stub endpoints** for dispatch/reports (Phase 3+)
5. **WebSocket stub** (full implementation Phase 2)
6. **No cross-camera correlation** (Phase 3)
7. **No TensorRT optimization** (Phase 4)

Deployment Path (Phase 1)
==========================

.. code-block:: text

   Local Development
       ↓
   Docker Compose (Single machine)
       ↓
   Testing on sample CCTV data
       ↓
   Pilot deployment (5-10 cameras)
       ↓
   Phase 1 complete → Phase 2 planning

Next Steps
==========

→ See :ref:`roadmap-phase2` for next phase objectives

→ Check :ref:`developer-setup` to start coding Phase 1 remaining tasks

--------

**Last Updated:** March 29, 2026
