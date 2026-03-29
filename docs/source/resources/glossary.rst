.. _resources-glossary:

==============
Glossary
==============

Technical Terms
================

**RTSP**
   Real Time Streaming Protocol. Standard protocol for video streaming used by all IP cameras.
   Example: ``rtsp://192.168.1.100:554/stream``

**ONVIF**
   Open Network Video Interface Forum. Standard for IP camera communication and discovery.

**YOLOv8**
   You Only Look Once version 8. Real-time object detection model. Detects persons, vehicles, animals.
   Speed: 15-50ms per frame depending on hardware.

**Inference**
   The process of running a trained ML model on new data (camera frames) to make predictions.
   Also called "forward pass" or "prediction".

**Confidence Score**
   Probability that a detection is correct (0-1 scale).
   Example: Person detected with 0.87 confidence (87% sure).

**Bounding Box**
   Rectangle coordinates (x1, y1, x2, y2) that marks object location in image.

**ByteTrack**
   Multi-object tracking algorithm that assigns consistent IDs to the same person across frames.
   Enables dwell-time computation.

**Track ID**
   Unique identifier for person/object within a camera feed. Resets when camera reboots.
   Example: Person first appears as track_id=5, stays until they leave.

**Dwell Time**
   How long a person stays in a zone. Used for loitering detection (> 600 seconds = alert).

**PostGIS**
   PostgreSQL extension for spatial (geography) queries.
   Enables zone containment checks: "Is this incident inside the zone polygon?"

**GeoJSON**
   Standard format for geographic data (points, polygons, coordinates).
   Example: Indian state boundaries in GeoJSON format.

**GADM**
   Global Administrative Division Maps. Provides boundary polygons for all countries, states, districts.

**Pub/Sub**
   Publish-Subscribe messaging pattern. Publishers send alerts, subscribers listen on Redis channels.
   Enables real-time dashboard updates.

**WebSocket**
   Bidirectional communication protocol over TCP. Enables server pushing alerts to browser without polling.

**Async/Await**
   Non-blocking I/O pattern. FastAPI uses this to handle 1000s of concurrent requests efficiently.

**ORM**
   Object-Relational Mapping. SQLAlchemy ORM maps database tables to Python classes.
   Example: ``incident = session.query(Incident).filter_by(id='abc').first()``

**ACID**
   Atomicity, Consistency, Isolation, Durability. Database guarantees for data reliability.

System Architecture Terms
==========================

**Layer 1 (Data Sources)**
   CCTV cameras, open data APIs (NCRB crime stats, GADM boundaries, weather).

**Layer 2 (Data Ingestion)**
   OpenCV RTSP frame capture, FFmpeg decoding, preprocessing (resize, normalize).

**Layer 3 (AI Inference)**
   YOLOv8 object detection, ByteTrack tracking, rules engine, alert scoring.

**Layer 4 (Application API)**
   FastAPI REST endpoints, WebSocket server, SQL database, Redis pub/sub.

**Layer 5 (Presentation)**
   React web dashboard, maps, camera grids, operator controls.

Alert & Incident Terms
======================

**Alert**
   Single frame-level detection. Triggered when rules engine detects behavior in one frame.
   High volume (1000s per hour during active threat).
   Short-lived, auto-purged after 7 days.

**Incident**
   Aggregated threat event across multiple frames/cameras.
   Long-lived, persists for operator investigation.
   Examples: "Loitering at main gate", "Crowd surge in parking".

**Incident Type**
   Classification of threat: LOITERING, CROWD_SURGE, ABANDONED_OBJECT, PERIMETER_BREACH, etc.

**Severity**
   Alert/incident priority: LOW (monitor), MED (review), HIGH (action required).
   Determined by rules engine confidence and rule importance.

**Risk Score**
   Calculated: (HIGH×3 + MED×1.5 + LOW×1) / camera_count
   Displayed on risk dial (0-100 scale).
   Used to prioritize operator attention.

**Risk Dial**
   Animated gauge showing system-wide threat level.
   Colors: GREEN (0-45 low), AMBER (45-70 med), RED (70-100 high).

**Confidence**
   YOLOv8 detection confidence. Higher = more certain.
   Typical threshold: 0.5 (50% sure). Configurable per deployment.

**False Positive**
   Alert that is not a real threat (tree moving, reflection, vehicle).
   Marked by operator as non-threat for model retraining (Phase 4).

**Deduplication**
   Removing duplicate alerts for same person/object.
   Uses MinHash algorithm to compare detection images (Phase 2).

Operational Terms
==================

**Operator**
   Human user monitoring the dashboard and responding to alerts.
   Dashboard shows threat queue, metrics, camera feeds.

**Escalation**
   Sending HIGH alerts to emergency authorities (police, security teams).
   Methods: SMS, WhatsApp, emergency hotline (Phase 3).

**Dispatch**
   Sending security/police unit to investigate incident.
   Tracked in database for response time metrics.

**SOS Panel**
   Emergency state helpline contacts (police, fire, ambulance).
   Shown on map. Triggered when high-threat incident detected.

**Zone**
   Geographic area of interest. Defined by polygon (GeoJSON).
   Examples: Main gate perimeter, parking lot, building entrance.

**Camera Registry**
   List of all managed RTSP cameras with metadata (location, zone, status).

**Heartbeat**
   Periodic ping from camera to confirm it's alive.
   Expected every 30 seconds. Absence triggers offline alert.

Database Terms
===============

**Schema**
   Database table structure. SENTINEL has 6 tables: Cameras, Zones, Incidents, Alerts, Detections, Metrics.

**Index**
   Database optimization technique. Composite index on (zone_id, severity, created_at) enables sub-100ms queries.

**Composite Index**
   Index on multiple columns together.
   Example: WHERE zone_id='zone_1' AND severity='HIGH' is fast.

**Full-Text Index**
   Index for searching text. Used for incident description search (Phase 3).

**Spatial Index**
   PostGIS index on geometry column. Enables fast "is point in polygon" queries.

**Foreign Key**
   Database constraint linking tables. Alert.incident_id → Incident.id.

**Query Plan**
   Execution strategy for SQL query. Use ``EXPLAIN ANALYZE`` to optimize slow queries.

**Normalization**
   Database design principle to reduce redundancy.
   SENTINEL uses 3NF (third normal form).

Development Terms
===================

**GitHub**
   Version control platform. Hosts SENTINEL code repository.

**Git**
   Version control system. Commands: ``git add``, ``git commit``, ``git push``.

**Pull Request (PR)**
   Proposed code change. Reviewed before merging to main branch.

**Merge**
   Combining code from one branch into another.

**Docker**
   Containerization technology. ``docker-compose.yml`` defines all services.

**Container**
   Lightweight virtual machine. PostgreSQL, Redis, FastAPI each run in containers.

**Image**
   Blueprint for building containers. Defined in ``Dockerfile``.

**Docker Compose**
   Tool for multi-container orchestration. Manages PostgreSQL, Redis, backend, frontend together.

**Environment Variables**
   Configuration values defined in ``.env`` file.
   Examples: DATABASE_URL, YOLO_CONFIDENCE_THRESHOLD.

**Type Hints**
   Annotations in Python/TypeScript specifying variable types.
   Example: ``def get_incidents(limit: int) -> List[Incident]:``

**Async/Await**
   Keywords for non-blocking I/O. Allows handling 1000s of concurrent connections.

**REST API**
   Representational State Transfer. Standard for HTTP APIs.
   Methods: GET (retrieve), POST (create), PATCH (update), DELETE (remove).

**OpenAPI**
   Standard specification for REST APIs.
   FastAPI auto-generates interactive docs at ``/docs``.

**Pagination**
   Splitting large result sets. Parameters: ``limit``, ``offset``.
   Example: ``GET /incidents?limit=50&offset=100`` returns items 100-150.

**Linting**
   Automated code quality checks. Python: pylint, Black. TypeScript: ESLint.

**Unit Test**
   Test for single function. Example: Test get_incidents() returns 10 items.

**Integration Test**
   Test for multiple components working together.
   Example: Test that creating incident updates database and publishes alert.

**Mock**
   Fake object used in testing. Example: Mock Redis client for unit tests.

**Deployment Terms**
=======================

**Environment**
   Deployment stage: Development (local), Staging (pre-prod), Production (live).

**Kubernetes**
   Container orchestration platform. Manages scaling, rolling updates, health checks.

**Helm**
   Kubernetes package manager. Simplifies deployment.

**SSL/TLS**
   Encryption protocols. Secure HTTP (HTTPS) uses TLS.

**Certificate**
   Cryptographic credential proving identity. Issued by certificate authority (CA).

**Load Balancer**
   Distributes traffic across multiple servers.
   Enables high availability (Phase 4).

**Monitoring**
   Continuous observation of system health. Metrics: CPU, memory, latency, error rate.

**Logging**
   Recording application events. Structured logs (JSON) enable log aggregation.

**Alerting**
   Notifying operators of system issues (high CPU, database down, error spike).

**Scaling**
   Adding more resources. Horizontal: more servers. Vertical: more CPU/RAM per server.

**CICD**
   Continuous Integration/Continuous Deployment. Automates testing and deployment.

**Artifact**
   Built output. Docker image, Python wheel, compiled binary.

Compliance Terms
=================

**GDPR**
   General Data Protection Regulation (EU). Regulates personal data processing.

**PDPB**
   Personal Data Protection Bill (India). Similar to GDPR.

**Privacy**
   Protection of personal information from unauthorized access.

**Consent**
   User agreement before processing personal data.

**Data Minimization**
   Collecting only necessary data. SENTINEL collects behavioral data, not biometrics.

**Encryption**
   Converting data to unreadable form without key. Protects data in transit and at rest.

**Audit Trail**
   Log of all actions on sensitive data. Who accessed what, when.

**Anonymization**
   Removing identifiable information. SENTINEL is anonymized by design (no facial recognition).

Phase-Specific Terms
====================

**Phase 1**
   Foundation: API, database, React shell. Current state.
   Target: 60% complete. Status: Infrastructure done, inference stubs ready.

**Phase 2**
   ML Pipeline: YOLOv8 + ByteTrack + Rules engine. Operational system.
   Timeline: Weeks 5-8. Deliverable: Detection + alert broadcasting.

**Phase 3**
   Multi-camera analytics: Cross-camera correlation, map integration, escalation APIs.
   Timeline: Weeks 9-12. Deliverable: Investigative tools + emergency integration.

**Phase 4**
   Production hardening: Kubernetes, monitoring, optimization, compliance.
   Timeline: Weeks 13+. Deliverable: Enterprise-grade system.

Performance Terms
==================

**Latency**
   Time delay between input and output. SENTINEL target: <250ms frame-to-alert.

**Throughput**
   Amount of data processed per unit time. Example: 50 camera feeds processed simultaneously.

**FPS (Frames Per Second)**
   Temporal resolution of video. CCTV typical: 25 FPS. Impacts latency and storage.

**Resolution**
   Image pixel dimensions. Common: 720p (1280×720), 1080p (1920×1080).
   Higher resolution = slower inference but better detection.

**Batching**
   Processing multiple frames together for efficiency.
   Example: Process 4 frames in one batch (faster than 1 frame 4 times).

**GPU**
   Graphics Processing Unit. Parallel hardware for ML inference.
   NVIDIA T4 (cloud), RTX 4090 (desktop), A100 (data center).

**CPU**
   Central Processing Unit. Slower for ML but works without GPU.

**Memory**
   RAM usage. SENTINEL: 4GB base + 2GB per 10 camera streams.

**Storage**
   Disk usage. SENTINEL: ~100GB per 100 hours of 720p recording (raw frames).
   Incident/alert metadata: 1-2GB per month.

**Throughput**
   Network bandwidth. 5 Mbps per 720p camera @ 25 FPS.

Next Steps
==========

→ Return to :ref:`resources-faq` for common questions

→ See :ref:`resources-troubleshooting` for error diagnosis

--------

**Last Updated:** March 29, 2026

**Note:** Terms are cross-referenced. Look up any unfamiliar words here.
