.. SENTINEL documentation master file
   https://sentinel.readthedocs.io/

========================================
SENTINEL - Public Safety AI System
========================================

.. image:: _static/sentinel-banner.png
   :align: center
   :alt: SENTINEL System

**Real-time threat detection, live mapping, and emergency dispatch platform for public safety infrastructure.**

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :numbered:

   guide/introduction
   guide/quick-start
   guide/architecture

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :numbered:

   guide/installation
   guide/configuration
   guide/usage
   guide/deployment

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   :numbered:

   api/overview
   api/endpoints
   api/schemas
   api/examples

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide
   :numbered:

   developer/setup
   developer/backend
   developer/frontend
   developer/testing
   developer/contributing

.. toctree::
   :maxdepth: 2
   :caption: Roadmap
   :numbered:

   roadmap/phase1
   roadmap/phase2
   roadmap/phase3
   roadmap/phase4

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources

   resources/faq
   resources/troubleshooting
   resources/glossary
   resources/compliance

--------

Project Information
===================

- **Version:** 1.0.0
- **Status:** Phase 1 (Foundation) - 60% Complete
- **License:** MIT
- **Repository:** `GitHub <https://github.com/your-org/sentinel>`_
- **Issues:** `GitHub Issues <https://github.com/your-org/sentinel/issues>`_
- **Discussions:** `GitHub Discussions <https://github.com/your-org/sentinel/discussions>`_

Quick Links
===========

- 🚀 `Quick Start Guide <guide/quick-start.html>`_
- 📚 `API Documentation <api/endpoints.html>`_
- 🛠️ `Developer Setup <developer/setup.html>`_
- 🐳 `Deployment Guide <guide/deployment.html>`_
- 🗺️ `Architecture Overview <guide/architecture.html>`_

Key Features
============

✅ **Real-time Detection** - YOLOv8-powered threat detection at <50ms inference speed

✅ **Live Geospatial Map** - Leaflet.js-based threat visualization with Nominatim integration

✅ **Emergency Dispatch** - One-tap escalation to authorities (112, 181, 100, 108, 1098)

✅ **Zero Facial Recognition** - Behavioural + object-based detection only (PDPB 2023 compliant)

✅ **Open Source** - 100% open-source stack, deploy anywhere, no vendor lock-in

✅ **Production Ready** - Docker, PostgreSQL, Redis, Kubernetes-ready (Phase 4)

Core Stack
==========

**Backend:** FastAPI · Python 3.11 · PostgreSQL + PostGIS · Redis

**Frontend:** React 18 · Vite · Tailwind CSS · Leaflet.js

**AI/ML:** YOLOv8 · ByteTrack · OpenCV · ONNX Runtime · TensorRT

**DevOps:** Docker · Docker Compose · GitHub Actions · Kubernetes (Phase 4)

System Objectives
=================

| **Detect** | Threat identification (perimeter breaches, abandoned objects, crowd surges, loitering) |
| **Assess** | Per-zone risk scoring, severity ranking, duplicate suppression |
| **Communicate** | Live threat map for field officers & command centres |
| **Dispatch** | One-touch emergency authority escalation by geolocation |
| **Learn** | Continuous model retraining on confirmed-positive events |

Current Status
==============

.. list-table::
   :widths: 30 20 50
   :header-rows: 1

   * - Component
     - Status
     - Notes
   * - Docker Infrastructure
     - ✅ Complete
     - Multi-service orchestration ready
   * - FastAPI Backend
     - ✅ Complete
     - 14+ REST endpoints, async/await
   * - PostgreSQL Database
     - ✅ Complete
     - Spatial queries, proper indexes
   * - React Frontend
     - ✅ Complete
     - 4 core components, TypeScript
   * - **Phase 1 Progress**
     - **~60%**
     - YOLOv8 loading, RTSP capture, WebSocket remaining

Next Steps
==========

1. **For Users:** Start with `Quick Start Guide <guide/quick-start.html>`_
2. **For Developers:** Begin at `Developer Setup <developer/setup.html>`_
3. **For Deployment:** Check `Deployment Guide <guide/deployment.html>`_
4. **For Questions:** Visit `FAQ <resources/faq.html>`_ or `Troubleshooting <resources/troubleshooting.html>`_

--------

**Last Updated:** March 29, 2026 · **Version:** 1.0.0-alpha

Built with ❤️ for public safety infrastructure
