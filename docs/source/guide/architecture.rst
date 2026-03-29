.. _guide-architecture:

============
Architecture
============

Detailed overview of SENTINEL's system architecture, design principles, and component interactions.

System Overview
===============

SENTINEL is organized into **5 horizontal layers**, with data flowing upward from raw camera streams to operator interfaces:

.. code-block:: text

    ┌─────────────────────────────────────────────────────────────┐
    │ Layer 5: PRESENTATION (React + Vite + Leaflet.js)           │
    │ - Command Dashboard  - Live Threat Map  - Camera Grid       │
    └─────────────────────────────────────────────────────────────┘
                              ↑ WebSocket/REST
    ┌─────────────────────────────────────────────────────────────┐
    │ Layer 4: APPLICATION API (FastAPI + WebSocket + Redis)      │
    │ - REST Endpoints  - WebSocket Server  - Pub/Sub Router      │
    └─────────────────────────────────────────────────────────────┘
                              ↑ SQL + Pub/Sub
    ┌─────────────────────────────────────────────────────────────┐
    │ Layer 3: AI INFERENCE ENGINE (YOLOv8 + ByteTrack + Rules)   │
    │ - Object Detection  - Multi-object Tracking  - Analytics    │
    └─────────────────────────────────────────────────────────────┘
                              ↑ Events
    ┌─────────────────────────────────────────────────────────────┐
    │ Layer 2: DATA INGESTION (OpenCV + FFmpeg + ONNX)            │
    │ - RTSP Stream Capture  - Frame Preprocessing  - Inference   │
    └─────────────────────────────────────────────────────────────┘
                              ↑ Streams
    ┌─────────────────────────────────────────────────────────────┐
    │ Layer 1: DATA SOURCES (CCTV Cameras + Open Data)            │
    │ - IP CCTV Streams  - Crime Data  - Geospatial Boundaries    │
    └─────────────────────────────────────────────────────────────┘

Layer 1 - Data Sources
======================

**IP CCTV Cameras**
   RTSP/ONVIF streams from standard surveillance equipment.
   No proprietary hardware required.

**Open Data Sources**
   - NCRB crime statistics
   - GADM GeoJSON (state/district boundaries)
   - OSM/Nominatim (reverse geocoding)
   - NWP weather data (Phase 3)

Layer 2 - Data Ingestion
========================

**OpenCV Frame Capture**
   - Reads RTSP/H.264 streams at 25 FPS
   - Ring buffer with 128-frame capacity
   - Handles connection drops gracefully

**FFmpeg Video Decoding**
   - Efficient H.264/H.265 decoding
   - Pre-processing: resize, normalize, batch

**Inference Optimization**
   - ONNX Runtime for CPU inference
   - TensorRT for GPU optimization (Phase 4)
   - Batching: 4 frames per batch

Layer 3 - AI Inference
======================

**YOLOv8 Object Detection**
   - Pretrained weights (COCO dataset)
   - Outputs: class ID, confidence, bounding box
   - <15ms inference on T4 GPU

**ByteTrack Multi-Object Tracking**
   - Associates detections across frames
   - Assigns persistent track IDs
   - Computes velocity & dwell-time

**Behavioral Rules Engine**
   - Loitering (dwell_time > 600s)
   - Crowd surge (persons > threshold)
   - Abandoned object (stationary > 300s)
   - Cross-camera pattern analysis (Phase 3)

**Alert Scoring**
   - Scikit-learn rule ensemble
   - Confidence thresholding
   - Duplicate suppression (MinHash)
   - Severity ranking (HIGH/MED/LOW)

Layer 4 - Application API
==========================

**FastAPI REST API**
   - Async request handlers
   - Type-safe request/response validation
   - Auto-generated OpenAPI docs
   - CORS configured

**WebSocket Server**
   - Real-time alert streaming
   - Low-latency browser push (<100ms)
   - Automatic reconnection

**Redis Pub/Sub**
   - Sub-millisecond alert fan-out
   - Publish from inference layer
   - Subscribe from API & frontend

**Request/Response Pipeline**

.. code-block:: text

    Camera Feed
        ↓
    Frame Capture → YOLOv8 → ByteTrack → Rules Engine → Alert Scoring
        ↓
    Alert Event
        ↓
    Store in PostgreSQL ----┐
                           ↓
    Publish to Redis → Pub/Sub → WebSocket → Frontend
                           ↓
                    REST GET /incidents

Layer 5 - Presentation
======================

**React Command Dashboard**
   - Threat Queue (real-time incident stream)
   - Risk Dial (animated gauge showing severity)
   - Metrics cards (uptime, response time, incident counts)
   - Zone Risk Map (color-coded by risk level)
   - Camera Status Grid (live feed thumbnails)

**Live Threat Map (Phase 3)**
   - Leaflet.js with OpenStreetMap tiles
   - GADM GeoJSON state/district polygons
   - Incident bubble markers (sized by count)
   - SOS emergency panel (state-driven helplines)

**Camera Analytics Grid**
   - MJPEG thumbnail streams
   - AI overlay (bounding boxes, track IDs, dwell time)
   - Alert animation effects
   - Full-screen modal for detailed analysis

Data Flow & Latency
===================

**Frame to Alert Flow:**

.. code-block:: text

    Frame Capture (0ms)
        ↓ ─ Frame buffered in ring buffer
    Pre-processing (2ms)
        ↓ ─ Resize, normalize, batch
    YOLOv8 Inference (15ms)
        ↓ ─ Bounding boxes + confidence
    ByteTrack Tracking (3ms)
        ↓ ─ Track ID assignment
    Rules Engine (2ms)
        ↓ ─ Behavioral analysis
    Alert Scoring (1ms)
        ↓ ─ Severity ranking
    PostgreSQL Persist (3ms)
        ↓ ─ ACID guaranteed storage
    Redis Publish (<1ms)
        ↓ ─ Sub-millisecond fan-out
    WebSocket Push (50-100ms)
        ↓ ─ Network latency
    Browser Render (100-200ms)
        ↓ ─ DOM update
    TOTAL: ~200-250ms per frame

**Target (Phase 4):** <60 seconds detection-to-dispatch

Database Architecture
=====================

**Entity Relationship Diagram:**

.. code-block:: text

    Cameras (1) ──────────→ (N) Detections
       │
       └─────────→ (N) Alerts ──────→ (1) Incidents
       │                              │
       └──────────────────────────────┘

**Core Tables:**

.. list-table::
   :widths: 20 15 50
   :header-rows: 1

   * - Table
     - Records
     - Purpose
   * - **cameras**
     - ~50
     - RTSP stream registry with heartbeat
   * - **zones**
     - ~100
     - Geographic regions (PostGIS geometry)
   * - **incidents**
     - 1000s
     - Aggregated threat events
   * - **alerts**
     - 10000s
     - Frame-level detections (audit trail)
   * - **detections**
     - 100000s
     - Raw YOLOv8 output

**Indexes:**

- Composite: (zone_id, severity, created_at)
- Spatial: GiST index on zone geometry
- Full-text: On incident description (Phase 3)

Real-time Architecture
======================

**Alert Broadcasting Flow:**

.. code-block:: text

    Inference Engine (Backend)
        │
        ├→ Store in PostgreSQL
        │
        └→ Publish to Redis
            │
            └→ redis-cli PUBLISH sentinel:alerts '{"alert_id":"..."}'
                │
                ├→ FastAPI WebSocket Handlers
                │   │
                │   └→ await websocket.send_json(alert)
                │
                └→ Frontend WebSocket Client
                    │
                    └→ Update Threat Queue (real-time)

**Latency Breakdown:**

- Inference: 15-30ms
- Perry store: 3-5ms
- Redis publish: <1ms
- WebSocket delivery: 50-100ms
- Browser render: 100-200ms
- **Total:** ~200-300ms (sub-second visible update)

Scalability Considerations
==========================

**Current (Phase 1):**
- Single machine
- 10 concurrent cameras
- In-memory queue

**Phase 2:**
- Multi-instance capable
- 25 concurrent cameras
- Celery background jobs

**Phase 3:**
- Distributed tracking
- Regional deployment
- Cross-camera correlation

**Phase 4:**
- Kubernetes clusters
- Geo-distributed nodes
- Load balancing

Security Architecture
=====================

**Authentication (Phase 4):**
- JWT tokens for API access
- Role-based access control (RBAC)
- API key rotation

**Data Protection:**
- Encryption in transit (SSL/TLS)
- Encryption at rest (optional)
- Database access control via PostgreSQL roles
- Audit logging of all actions

**Privacy:**
- Zero facial recognition
- Behavior-based detection only
- Data minimization (detections auto-purge after 30 days)
- GDPR/PDPB compliant

Configuration Management
========================

**Environment-based:**

.. code-block:: text

    Development:
    - DEBUG=True
    - Reduced batch sizes
    - Verbose logging

    Staging:
    - DEBUG=False
    - Full batch sizes
    - Log aggregation

    Production:
    - DEBUG=False
    - Optimized inference
    - Monitoring enabled

Caching Strategy
================

**Redis Cache:**
- Metrics (avg_response_time): 5 min TTL
- Zone risk scores: 2 min TTL
- Camera status: 30 sec TTL

**Database Indexes:**
- Speed up incident filtering
- Support sub-100ms queries at scale

Monitoring & Observability
===========================

**Metrics Exposed (Phase 4):**
- Inference latency (histogram)
- Alert throughput (gauge)
- Model accuracy (counter)
- System uptime (gauge)
- API response time (histogram)

**Logging:**
- Structured logging (JSON format)
- Centralized log aggregation
- Alert-level tracking

Design Principles
=================

#. **Layered Isolation** - Each layer independent, replaceable
#. **Async-First** - Non-blocking I/O throughout
#. **Open Standards** - No proprietary formats or dependencies
#. **Privacy-Preserving** - Zero biometric identification
#. **Fail-Safe Design** - Graceful degradation on errors
#. **Transparency** - Auditable, explainable decisions

Technology Rationale
====================

.. list-table::
   :widths: 25 50
   :header-rows: 1

   * - Technology
     - Why Chosen
   * - **FastAPI**
     - Async-first, native WebSocket, automatic docs
   * - **PostgreSQL**
     - ACID compliance, PostGIS for spatial queries
   * - **Redis**
     - Sub-millisecond pub/sub, proven in production
   * - **React 18**
     - Concurrent rendering, large ecosystem
   * - **YOLOv8**
     - 80+ FPS accuracy, Apache 2.0 license, free
   * - **ByteTrack**
     - Superior to SORT/DeepSORT, works without re-ID
   * - **Docker**
     - Dev/prod parity, reproducible environments
   * - **Kubernetes**
     - Scalability, cloud-native (Phase 4)

Fault Tolerance
===============

**Camera Stream Down:**
- Inference pauses, doesn't crash
- Automatic retry every 5 seconds
- Operator notified via dashboard

**Database Connection Lost:**
- Request queued in Redis
- Automatic reconnect with exponential backoff
- Data never lost

**API Crash:**
- Kubernetes auto-restart (Phase 4)
- Health checks every 10 seconds
- Graceful shutdown with cleanup

Next Steps
==========

→ Explore :ref:`api-endpoints` to understand API contracts

→ Continue to :ref:`dev-architecture` for detailed implementation

--------

**Last Updated:** March 29, 2026
