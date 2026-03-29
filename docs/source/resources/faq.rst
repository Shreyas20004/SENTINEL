.. _resources-faq:

============================
Frequently Asked Questions
============================

General Questions
==================

**Q: What is SENTINEL?**

A: SENTINEL is a privacy-preserving, real-time threat detection system that uses AI/ML to analyze CCTV feeds. It detects loitering, crowd surges, abandoned objects, and perimeter breaches without facial recognition.

**Q: How is SENTINEL different from other surveillance systems?**

A: Unlike traditional CCTV, SENTINEL:
- Analyzes behavior, not identity (zero facial recognition)
- Operates on-premise (no cloud dependency)
- Respects privacy (PDPB 2023 compliant)
- Provides explainable decisions (visible bounding boxes)
- Integrates with open data (GADM, OSM, NCRB)

**Q: What are the licensing requirements?**

A: SENTINEL is open source (Apache 2.0 license). You can use, modify, and distribute freely. Attribution to original authors appreciated.

**Q: Can I use SENTINEL with any CCTV camera?**

A: Yes, any camera with RTSP/ONVIF support (99% of IP cameras). No special hardware required. Works with H.264 and H.265 streams.

**Q: Does SENTINEL require internet connectivity?**

A: No. SENTINEL runs entirely on-premise. All inference, storage, and alerting happen locally. Optional integrations (weather APIs, reverse geocoding) can be air-gapped.

Deployment Questions
=====================

**Q: What hardware do I need?**

A: **Minimum (Phase 1):**
- CPU: 4-core Intel/AMD
- RAM: 8GB
- Storage: 50GB SSD
- Network: 1Gbps Ethernet

**Recommended (Phase 2+):**
- CPU: 8-core Intel Xeon / AMD EPYC
- RAM: 32GB
- Storage: 500GB SSD
- GPU: NVIDIA T4/A100 (optional but strongly recommended)
- Network: 10Gbps

**Q: How many cameras can one server handle?**

A: **Phase 1:** 10-15 cameras
**Phase 2:** 25-50 cameras
**Phase 3:** 50-100 cameras (distributed)
**Phase 4:** 1000+ cameras (Kubernetes cluster)

Depends on resolution, FPS, and detection complexity.

**Q: Can I run SENTINEL in the cloud?**

A: Yes, but we recommend on-premise for latency-critical applications. You can run on AWS EC2, Google Cloud, Azure, or self-hosted Kubernetes.

**Q: What are the bandwidth requirements?**

A: **Ingestion:** 5 Mbps per camera (H.264 @ 720p 25fps)
**Egress:** <100 Kbps per user (WebSocket alerts only)

Example: 10 cameras = 50 Mbps ingestion + minimal egress.

**Q: How long do you retain incident data?**

A: Configurable (defaults):
- Raw detections: 7 days
- Incidents: 30 days
- Alerts: 90 days
- Metrics: 1 year

Older data auto-purges. Configure in `.env` or database policies.

Technical Questions
====================

**Q: What is the inference latency?**

A: **Phase 1:** ~100-150ms per frame (CPU)
**Phase 2:** ~30-50ms (GPU T4)
**Phase 3:** ~15-20ms (GPU A100)

Depends on resolution and batch size. Sub-100ms possible on modern GPUs.

**Q: Can I use custom ML models instead of YOLOv8?**

A: Yes. Phase 2 provides abstraction layer (yolo_inference.py). You can replace with:
- Faster R-CNN
- EfficientDet
- Custom PyTorch models
- TensorFlow models
- TensorRT optimized variants

Just implement the same interface.

**Q: Does SENTINEL support facial recognition?**

A: No, by design. SENTINEL uses pose estimation and behavior analysis only. Facial recognition is explicitly disabled for privacy compliance (PDPB 2023, IT Act 2000).

**Q: How does ByteTrack work?**

A: Assigns persistent track IDs across frames by:
1. Association: Hungarian algorithm matches detections to existing tracks
2. Motion prediction: Kalman filter predicts position in next frame
3. Velocity computation: Track speed helps predict future positions

Enables dwell-time and pattern detection without re-identification.

**Q: What happens if a camera goes offline?**

A: SENTINEL:
1. Stops capturing from that camera
2. Marks it "offline" on dashboard
3. Continues analyzing other cameras
4. Auto-reconnects every 5 seconds
5. Notifies operator after 30 seconds offline

No data loss; queued events resume when camera reconnects.

API Questions
==============

**Q: How do I create a test incident?**

A: Use cURL:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/incidents \
     -H "Content-Type: application/json" \
     -d '{
       "zone_id": "zone_1",
       "incident_type": "LOITERING",
       "severity": "MED",
       "description": "Test incident",
       "location_lat": 28.6139,
       "location_lng": 77.2090
     }' | jq

See :ref:`api-examples` for more recipes.

**Q: How do I filter incidents by severity?**

A: Use query parameters:

.. code-block:: bash

   curl "http://localhost:8000/api/v1/incidents?severity=HIGH&limit=50"

Supported: ``HIGH``, ``MED``, ``LOW``

**Q: Can I set custom thresholds?**

A: Yes. Edit `.env`:

.. code-block:: bash

   LOITERING_THRESHOLD=600        # seconds
   CROWD_SURGE_THRESHOLD=10       # persons
   CONFIDENCE_THRESHOLD=0.5       # YOLOv8 confidence
   RISK_SCORE_HIGH=70             # risk dial threshold
   RISK_SCORE_MED=45

Restart backend after changes.

**Q: How do I integrate with external systems?**

A: Phase 3 integrations (stubs ready):
- SMS via Twilio or AWS SNS
- WhatsApp via Twilio
- PagerDuty for incident routing
- SIEM integration (Splunk, ELK)
- ITSM integration (Jira, ServiceNow)

Using REST API, you can build custom integrations now.

Database Questions
===================

**Q: How do I backup the database?**

A: Using Docker:

.. code-block:: bash

   docker-compose exec postgres pg_dump -U postgres sentinel_dev > backup.sql

Restore:

.. code-block:: bash

   cat backup.sql | docker-compose exec -T postgres psql -U postgres

**Q: Can I migrate from SQLite to PostgreSQL?**

A: SENTINEL Phase 1 is PostgreSQL-only. If you need SQLite initially (for minimal setup), you can:
1. Start with SQLite (modify `database.py`)
2. Export data via REST API
3. Re-import into PostgreSQL

Not recommended for production.

**Q: How do I query incidents by zone geometry?**

A: Use PostGIS spatial queries:

.. code-block:: sql

   -- Find incidents within zone polygon
   SELECT i.id, i.incident_type, i.created_at
   FROM incidents i
   JOIN zones z ON ST_Contains(z.geometry, i.location_point)
   WHERE z.name = 'Main Gate'
   ORDER BY i.created_at DESC

Extended in Phase 3.

**Q: Can I export data?**

A: Yes:

.. code-block:: bash

   # CSV export via REST API
   curl "http://localhost:8000/api/v1/incidents" | jq -r '.[] | [.id, .severity, .status] | @csv' > incidents.csv

   # Database dump
   pg_dump -U postgres sentinel_dev > backup.sql

Troubleshooting
================

**Q: Backend won't start ("Address already in use")**

A: Port 8000 is occupied. Either:

.. code-block:: bash

   # Kill process on port 8000
   lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9

   # Or use different port
   API_PORT=8001 uvicorn app.main:app --reload

**Q: Database connection error**

A: Verify Docker PostgreSQL is running:

.. code-block:: bash

   docker-compose ps postgres
   docker-compose logs postgres

**Q: Frontend can't connect to API**

A: Check:

.. code-block:: bash

   # Verify API is running
   curl http://localhost:8000/health

   # Check CORS settings in backend/app/main.py
   # Add to .env: VITE_API_URL=http://localhost:8000

**Q: WebSocket connection fails**

A: Phase 1 has WebSocket stub. Full implementation in Phase 2. For now, use REST polling:

.. code-block:: bash

   curl http://localhost:8000/api/v1/incidents -s | jq length

**Q: Memory usage too high**

A: Reduce batch size in `.env`:

.. code-block:: bash

   YOLO_BATCH_SIZE=2  # Default 4

Or limit ring buffer:

.. code-block:: bash

   FRAME_BUFFER_SIZE=64  # Default 128

Performance Questions
======================

**Q: How do I optimize inference speed?**

A: Phase 4 techniques:

1. **Use GPU:** NVIDIA RTX 4090 gives 100+ FPS
2. **Quantization:** INT8 instead of FP32 (20% faster, 1% accuracy loss)
3. **ONNX Runtime:** 30% faster than standard PyTorch
4. **TensorRT:** NVIDIA's optimized runtime (2-3x faster)
5. **Batching:** Process 4 frames together instead of 1

Currently Phase 1 supports GPU selection. Phase 4 adds full optimization.

**Q: Why is alert latency 200ms when inference is 15ms?**

A: Latency breakdown:

.. code-block:: text

   YOLOv8 inference:      15ms
   ByteTrack:             3ms
   Rules engine:          2ms
   Database persist:      3ms
   Redis publish:         <1ms
   WebSocket delivery:    50-100ms
   Browser render:        100-200ms
   ─────────────────────────
   Total:                 200-300ms

Most latency is network/browser, not computation. Phase 4 VIP mode: <100ms target.

**Q: Can I run multiple inference workers?**

A: Phase 2 goal. Currently single-threaded. Celery task queue ready (Phase 2) for:

.. code-block:: bash

   # Run inference in parallel
   celery -A app.tasks worker --concurrency=4

Support & Contribution
======================

**Q: How do I report a bug?**

A: Create GitHub issue:

.. code-block:: text

   Title: [BUG] Cant create incident with severity=NULL
   Description: Steps to reproduce, expected vs actual behavior, logs

**Q: How do I contribute?**

A: Fork → Feature branch → Pull Request

See :ref:`developer-contributing` for detailed guidelines.

**Q: Where do I get help?**

A: 

- Docs: https://sentinel.readthedocs.io
- GitHub Issues: https://github.com/.../issues
- Email: support@sentinel-project.org
- Community Discord: (coming Phase 2)

**Q: Is there a community?**

A: SENTINEL is maintained by:
- Core team (Bangalore-based)
- Open source community
- Enterprise users (Phase 4)

Join discussions on GitHub Discussions (coming Phase 2).

Data Privacy Questions
======================

**Q: What personal data does SENTINEL collect?**

A: Only behavioral metadata:
- Bounding boxes (not faces)
- Track IDs (per-session only)
- Dwell times (how long in zone)
- Timestamp and zone

No facial templates, names, or personal identifiers stored.

**Q: Is SENTINEL GDPR compliant?**

A: Mostly yes, with caveats:
- ✅ No personal data processing
- ✅ Zero facial recognition
- ✅ Data minimization (auto-purge)
- ⚠️ Operator consent required (Phase 3)
- ⚠️ Audit logging (Phase 4)

For full GDPR compliance, implement audit trail separately.

**Q: What about PDPB 2023?**

A: PDPB compliance roadmap:

- ✅ No facial recognition
- ✅ Behavior-based detection
- ✅ Data minimization
- ⏳ Operator consent flow (Phase 3)
- ⏳ Breach notification (Phase 4)
- ⏳ Data subject access (Phase 4)

See DEPLOYMENT.md for compliance details.

License & Legal
================

**Q: What license is SENTINEL under?**

A: Apache 2.0 (open source, permissive)

You can:
- ✅ Use for commercial purposes
- ✅ Modify code
- ✅ Distribute
- ✅ Use privately

Just include LICENSE file and notice.

**Q: Can I use SENTINEL for law enforcement?**

A: Yes, subject to local regulations. SENTINEL explicitly does NOT include:
- Facial recognition
- Re-identification
- Individual tracking across cameras

Recommended for border control, critical infrastructure, public events.

**Q: What about liability?**

A: SENTINEL is provided "as is" under Apache 2.0 license. No warranties. Test thoroughly before operational deployment.

Next Steps
==========

→ See :ref:`resources-troubleshooting` for detailed error diagnosis

→ Read :ref:`resources-glossary` for technical terms

--------

**Last Updated:** March 29, 2026

**Help us improve:** Submit FAQ questions to support@sentinel-project.org
