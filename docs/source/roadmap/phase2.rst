.. _roadmap-phase2:

=====================
Phase 2: ML Pipeline
=====================

Detailed roadmap for Phase 2 implementation (Weeks 5-8).

Phase 2 Vision
==============

**"Operational Intelligence System"**

By end of Phase 2, SENTINEL:

- Detects threats in real-time from camera feeds
- Tracks individuals across frames
- Applies behavioral rules (loitering, crowd surge, abandoned objects)
- Publishes alerts to command center
- Enables multi-camera incident correlation (same person across zones)

Phase 2 Objectives
===================

**Primary:**

1. **Complete YOLOv8 Integration** (Week 1)
   - Load pretrained YOLO model
   - Batch inference from frame buffers
   - GPU acceleration (T4: <20ms, A100: <10ms)
   - Confidence thresholding
   - Class filtering (persons only initially)

2. **Implement ByteTrack Tracking** (Week 1)
   - Across-frame object association
   - Persistent track ID assignment
   - Velocity/acceleration computation
   - Trajectory logging for Phase 3 analysis

3. **Develop Behavioral Rules Engine** (Week 2)
   - Loitering detection (dwell_time > 600s)
   - Crowd surge detection (person_count > threshold)
   - Abandoned object detection (stationary > 300s)
   - Perimeter breach detection (location crossing boundary)

4. **Implement Alert Scoring** (Week 2)
   - Confidence-weighted severity ranking
   - Duplicate alert suppression (MinHash)
   - False positive filtering (ensemble thresholds)
   - Risk score aggregation per zone

5. **Complete WebSocket Real-time Streaming** (Week 2)
   - FastAPI WebSocket endpoint
   - Redis Pub/Sub integration
   - Browser-side reconnection logic
   - Dashboard real-time updates

6. **Scale to 25+ Cameras** (Week 3)
   - Multi-camera frame buffering
   - Celery task queue for parallel inference
   - Database connection pooling
   - Load balancing strategies

**Secondary:**

7. **Unit Tests & Performance** (Week 3-4)
   - pytest suite (>80% coverage)
   - Load testing (25 cameras × 30ms = 750 inferences/sec)
   - Latency profiling
   - Memory optimization

Architecture Changes
====================

**New Layer 2 → 3 Pipeline:**

.. code-block:: text

   Frame Capture Thread-Pool
        ↓ (queue frame packets)
   YOLOv8 Inference Worker Pool (Celery)
        ↓ (detections batch)
   ByteTrack Association
        ↓ (track IDs + velocity)
   Behavioral Rules Engine
        ↓ (applicable rules met)
   Alert Scoring Engine
        ↓ (confidence > threshold)
   PostgreSQL Insert + Redis Publish
        ↓
   WebSocket Broadcast → Browser
        ↓
   Dashboard Real-time Alert Animation

New Files (Phase 2)
====================

**Fully Implement:**

.. list-table::
   :widths: 35 40
   :header-rows: 1

   * - File
     - Purpose
   * - **backend/app/ai/yolo_inference.py**
     - YOLOv8 model loading + inference
   * - **backend/app/ai/frame_capture.py**
     - OpenCV RTSP stream acquisition
   * - **backend/app/ai/tracking.py**
     - ByteTrack multi-object tracker
   * - **backend/app/domain/rules.py**
     - Behavioral rule detection
   * - **backend/app/domain/scoring.py**
     - Alert severity computation
   * - **backend/tasks/inference.py**
     - Celery task for parallel processing
   * - **backend/tests/test_yolo.py**
     - YOLOv8 inference tests
   * - **backend/tests/test_tracking.py**
     - ByteTrack tests
   * - **backend/tests/test_rules.py**
     - Rules engine tests
   * - **frontend/src/hooks/useAlerts.ts**
     - React hook for real-time updates

Key Implementation Details
==========================

**YOLOv8 Configuration:**

.. code-block:: python

   from ultralytics import YOLO
   
   model = YOLO('yolov8m.pt')  # medium model
   # Inference modes:
   # - CPU: ~50ms per 640x480 frame
   # - GPU T4: ~15ms
   # - GPU A100: ~5ms
   
   results = model.predict(frame, 
     conf=0.5,           # confidence threshold
     iou=0.45,           # IOU for NMS
     classes=[0],        # Person class only
     device=0            # GPU device ID
   )
   
   # Output format for ByteTrack:
   # [[x1, y1, x2, y2, conf, class_id], ...]

**ByteTrack Parameters:**

.. code-block:: python

   from bytetrack import ByteTracker
   
   tracker = ByteTracker(
     track_thresh=0.6,
     track_buffer=30,          # frames to retain
     match_thresh=0.8,         # Hungarian algorithm
     frame_rate=25
   )
   
   # Update per frame:
   tracks = tracker.update(detections, image.shape)
   
   # Output: [Track(track_id, bbox, velocity, dwell_time), ...]

**Rules Engine Logic:**

.. code-block:: text

   For each track:
     if track.dwell_time > LOITERING_THRESHOLD:
       severity = HIGH if dwell_time > 1200 else MED
       alert_type = "LOITERING"
       publish alert
     
     if nearby_tracks > CROWD_SURGE_THRESHOLD:
       alert_type = "CROWD_SURGE"
       severity = HIGH if count > 20 else MED
       publish alert
     
     if track.bbox not in zone.polygon:
       alert_type = "PERIMETER_BREACH"
       severity = HIGH
       publish alert

Integration Points
===================

**With Existing Phase 1 Code:**

1. **Database**: Alert insertion triggers Redis publish
   - `backend/app/api/alerts.py` modified to call rules engine

2. **WebSocket**: Redis subscriber listens for alerts
   - New endpoint: `@app.websocket("/ws/alerts")`
   - Forwards to connected clients

3. **Frontend**: Dashboard updates on WebSocket message
   - `ThreatQueue.tsx` subscribes to WebSocket
   - Real-time incident list refresh

4. **Metrics**: Incident counts update risk dial
   - `GET /metrics/risk-dial` reflects current incidents

Performance Targets
===================

**Latency Breakdown (Frame → Alert):**

.. list-table::
   :widths: 30 20
   :header-rows: 1

   * - Step
     - Time
   * - Frame capture
     - 2ms
   * - Preprocessing
     - 2ms
   * - YOLOv8 inference (GPU)
     - 15ms
   * - ByteTrack association
     - 3ms
   * - Rules engine
     - 2ms
   * - Alert scoring
     - 1ms
   * - DB insert + Redis publish
     - 3ms
   * - WebSocket delivery
     - 50-100ms
   * - Browser render
     - 100-200ms
   * - **Total**
     - **~200ms** (sub-second)

**Throughput:**

- Single GPU: 50-100 FPS (depends on model)
- Multi-GPU: 200-400 FPS (4 × T4 cards)
- Cameras supported: 25-50 per server

Testing Strategy
================

**Unit Tests:**

.. code-block:: bash

   pytest backend/tests/test_yolo.py -v
   pytest backend/tests/test_tracking.py -v
   pytest backend/tests/test_rules.py -v
   
**Integration Tests:**

   - Simulate frame stream → alert → WebSocket
   - Test with public RTSP streams

**Load Testing:**

   - 25 simultaneous cameras
   - 1000 concurrent WebSocket clients
   - Database connection pooling

**Performance Profiling:**

   - CPU usage < 80% per core
   - Memory < 12GB
   - Inference latency < 30ms

Dependencies to Add
===================

.. list-table::
   :widths: 20 30
   :header-rows: 1

   * - Library
     - Version
   * - **ultralytics** (YOLOv8)
     - 8.0.207
   * - **torch**
     - 2.1.1
   * - **torchvision**
     - 0.16.1
   * - **ByteTrack**
     - 0.2.1
   * - **celery**
     - 5.3.4
   * - **scikit-learn**
     - 1.3.2
   * - **datasketch** (MinHash)
     - 1.0.9

Add to `backend/requirements.txt`.

Expected Challenges
====================

1. **GPU Memory Exhaustion**
   - Batch size tuning critical
   - Consider gradient checkpointing

2. **Frame Synchronization Across Cameras**
   - Camera FPS varies (15-30 typical)
   - Solution: Frame timestamp alignment

3. **Track ID Reassignment After Occlusion**
   - Person leaves frame, returns later
   - ByteTrack track buffer tuning needed

4. **False Positive Alerts**
   - Tree moving in wind = loitering?
   - Solution: Dedup + spatial context

5. **Multi-Zone Correlation**
   - Same person in zone_1 then zone_2?
   - Solution: Phase 3 task (inter-zone tracking)

Deliverables (Phase 2)
======================

By end of Phase 2:

✅ YOLOv8 model loaded and inferencing

✅ Frame captured from 25+ cameras

✅ ByteTrack tracking enabled

✅ Behavioral rules detected

✅ Alert scoring implemented

✅ WebSocket streaming real-time alerts

✅ Unit tests >80% coverage

✅ Performance targets met (<200ms latency)

✅ Documentation updated with new APIs

✅ Pilot deployment on real CCTV feeds

Success Criteria
================

Phase 2 is complete when:

- [ ] YOLOv8 detects persons in test video with >90% accuracy
- [ ] ByteTrack assigns consistent track IDs across 30 frames
- [ ] Rules engine correctly identifies loitering (10+ min test) as HIGH severity
- [ ] WebSocket delivers alerts to 100 concurrent clients <100ms
- [ ] Database handles 1000 alerts/hour without latency increase
- [ ] System runs on single GPU with <12GB memory
- [ ] All unit tests passing with >80% coverage
- [ ] End-to-end latency <250ms (frame to browser)
- [ ] Pilot deployment on 10-camera test site successful

Next Steps
==========

→ See :ref:`roadmap-phase3` for Phase 3 objectives

→ Start Phase 2 development with :ref:`developer-backend` guide

--------

**Last Updated:** March 29, 2026

**Timeline:** 4 weeks (Weeks 5-8 of project)
