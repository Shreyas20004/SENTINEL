.. _guide-introduction:

==================
Introduction
==================

Welcome to SENTINEL, a **real-time public safety AI system** designed for threat detection, live mapping, and emergency dispatch.

What is SENTINEL?
=================

SENTINEL is an open-source, multi-layer AI platform built for Indian public safety infrastructure (extensible globally). It:

- **Ingests** video feeds from IP CCTV cameras
- **Analyzes** video in real-time using YOLOv8 computer vision
- **Detects** threats (loitering, crowd surges, abandoned objects, perimeter breaches)
- **Visualizes** incidents on a live geospatial map
- **Enables** one-tap emergency dispatch to local authorities

Core Objectives
===============

.. tabs::

   .. tab:: Detect

      Identify threats from CCTV at real-time inference speed (<50 ms/frame):
      
      - Perimeter breaches
      - Abandoned objects
      - Crowd surges
      - Loitering behavior

   .. tab:: Assess

      Compute and rank threats:
      
      - Per-zone risk scores
      - Severity ranking (HIGH/MED/LOW)
      - Duplicate alert suppression
      - Operator fatigue prevention

   .. tab:: Communicate

      Deliver intelligence to operators:
      
      - Live threat map
      - Real-time incident timeline
      - Command dashboard
      - Threat severity indicators

   .. tab:: Dispatch

      Enable fast emergency response:
      
      - One-touch escalation to authorities
      - Geolocation-aware routing
      - Emergency number mapping (112, 181, 100, 108, 1098)
      - Call logging & statistics

   .. tab:: Learn

      Continuously improve detection:
      
      - Retraining on confirmed-positive events
      - False-positive rate reduction
      - Model drift detection
      - Performance monitoring

Key Features
============

✅ **Real-time Processing**
   YOLOv8-powered inference with <50ms frame latency. Processes 25 cameras @ 25 FPS simultaneously.

✅ **Zero Facial Recognition**
   Behavior-based and object-based detection only. No identity tracking. PDPB 2023 compliant.

✅ **Live Geospatial Map**
   Leaflet.js-based map with state/district boundaries. GeoJSON visualization. Nominatim reverse geocoding.

✅ **Open Source Stack**
   100% free and open-source technologies. No vendor lock-in. Deploy anywhere.

✅ **Production Ready**
   Docker Compose for development. Kubernetes-ready (Phase 4). Cloud deployment guides included.

✅ **Comprehensive Monitoring**
   System metrics (uptime, alerts/hour, response time). Prometheus + Grafana (Phase 4).

Architecture at a Glance
=========================

SENTINEL is organized into **5 horizontal layers**, each independently scalable:

.. code-block:: text

    Layer 5 ──── Presentation (React + Vite + Leaflet.js)
                    ↑ WebSocket/REST
    Layer 4 ──── Application API (FastAPI + WebSocket + Redis)
                    ↑ SQL + Pub/Sub
    Layer 3 ──── AI Inference (YOLOv8 + ByteTrack + Rules Engine)
                    ↑ Events
    Layer 2 ──── Data Ingestion (OpenCV + FFmpeg + ONNX Runtime)
                    ↑ Streams
    Layer 1 ──── Data Sources (CCTV Cameras + Open Data)

Technology Stack
================

.. list-table::
   :widths: 25 50
   :header-rows: 1

   * - Category
     - Technologies
   * - **Backend**
     - FastAPI, Python 3.11, SQLAlchemy, Pydantic
   * - **Database**
     - PostgreSQL 16, PostGIS, Redis
   * - **Frontend**
     - React 18, TypeScript, Tailwind CSS, Leaflet.js
   * - **AI/ML**
     - YOLOv8, ByteTrack, OpenCV, ONNX, TensorRT
   * - **DevOps**
     - Docker, Docker Compose, GitHub Actions, Kubernetes (Phase 4)
   * - **Monitoring**
     - Prometheus, Grafana, Python Logging

Use Cases
=========

**Law Enforcement Agencies**
   Real-time threat detection for traffic, perimeter, crowd monitoring. Predictive policing.

**Critical Infrastructure**
   Airport, port, railway, power plant security. Automated breach detection.

**Public Events**
   Crowd management. Anomaly detection at festivals, marathons, public gatherings.

**Border Security**
   Perimeter monitoring. Cross-border threat detection.

**Disaster Management**
   NDMA-compliant emergency response. Rapid incident coordination.

Compliance & Standards
======================

✅ **IT Act 2000** - Information Technology governance

✅ **PDPB 2023** - Personal Data Protection Bill compliance (India)

✅ **NDMA Guidelines** - National Disaster Management Authority standards

✅ **No Facial Recognition** - Privacy-first design principle

System Performance Targets
==========================

.. list-table::
   :widths: 40 20 20
   :header-rows: 1

   * - Metric
     - Target
     - Timeline
   * - **Inference Latency**
     - <50 ms/frame
     - Phase 2
   * - **Detection-to-Dispatch**
     - <60 seconds
     - Phase 3
   * - **Alert Precision**
     - >90%
     - Phase 2
   * - **Concurrent Cameras**
     - 25 @ 25 FPS
     - Phase 4
   * - **System Uptime**
     - >99.5%
     - Phase 4
   * - **False Positive Rate**
     - <10%
     - Phase 2

Deployment Model
================

**Phase 1** (Foundation)
   Single-machine Docker Compose. Development & testing.

**Phase 2** (Intelligence)
   Multi-instance capable. Load testing. Real-time features.

**Phase 3** (Geospatial)
   Distributed tracking. Regional deployment ready.

**Phase 4** (Hardening)
   Kubernetes-ready. Cloud deployment (AWS/GCP/Azure). Enterprise SLA.

Learning Path
=============

**New Users:**
   1. Read this introduction
   2. Follow :ref:`quick-start`
   3. Explore the :ref:`api-endpoints`

**System Administrators:**
   1. Review :ref:`guide-installation`
   2. Study :ref:`guide-deployment`
   3. Configure :ref:`guide-configuration`

**Backend Developers:**
   1. Complete :ref:`dev-setup`
   2. Understand :ref:`dev-architecture`
   3. Review :ref:`dev-backend`
   4. Study API implementation

**Frontend Developers:**
   1. Complete :ref:`dev-setup`
   2. Review :ref:`dev-frontend`
   3. Explore component hierarchy

**DevOps Engineers:**
   1. Read :ref:`guide-deployment`
   2. Review Docker setup
   3. Plan scaling strategy

Project Status
==============

**Current Phase:** Phase 1 - Foundation (60% Complete)

**Completed:**
   - ✅ Docker infrastructure
   - ✅ FastAPI backend with 14+ endpoints
   - ✅ PostgreSQL + PostGIS database
   - ✅ React frontend with 4 core components
   - ✅ Complete documentation

**In Progress:**
   - ⏳ YOLOv8 model loading
   - ⏳ OpenCV RTSP capture
   - ⏳ WebSocket real-time updates
   - ⏳ Unit tests

**Next Up (Phase 2):**
   - ByteTrack multi-object tracking
   - Behavioral rules engine
   - Alert scoring and deduplication
   - Kafka event streaming
   - Dashboard real-time animations

**Roadmap:**
   - Phase 3: Geospatial features (Weeks 11-15)
   - Phase 4: Hardening & production (Weeks 16-20)

Contributing
============

SENTINEL is open-source and welcomes contributions!

- 🐛 **Found a bug?** `Report an issue <https://github.com/your-org/sentinel/issues>`_
- 💡 **Have a feature idea?** `Start a discussion <https://github.com/your-org/sentinel/discussions>`_
- 👨‍💻 **Ready to code?** Check :ref:`contributing` guidelines
- 📝 **Want to improve docs?** Suggest edits!

Support
=======

- 📖 **Documentation:** This guide
- 💬 **Community:** GitHub Discussions
- 🐛 **Issues:** GitHub Issues
- 📧 **Email:** sentinel-admin@example.local

Next Steps
==========

Ready to get started? 

→ **Begin with** :ref:`quick-start` **to set up SENTINEL in 10 minutes**

--------

**Last Updated:** March 29, 2026 | **Version:** 1.0.0-alpha
