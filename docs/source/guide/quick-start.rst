.. _quick-start:

===========
Quick Start
===========

Get SENTINEL up and running in 10 minutes.

Prerequisites
=============

Before starting, ensure you have:

- **Docker Desktop** or Docker Engine (latest stable)
- **Docker Compose** 2.0+
- **Git**
- ~2GB free disk space
- Optional: NVIDIA GPU (CUDA 11.8+) for GPU acceleration

Step 1: Clone Repository
========================

.. code-block:: bash

   git clone https://github.com/your-org/sentinel.git
   cd sentinel

Step 2: Configure Environment
=============================

Copy the example environment file:

.. code-block:: bash

   cp backend/.env.example backend/.env

Review and adjust settings if needed (defaults work for local development):

.. code-block:: bash

   # backend/.env
   DEBUG=True
   DATABASE_URL=postgresql://sentinel:sentinel_secure_pwd_2024@postgres:5432/sentinel_db
   REDIS_URL=redis://redis:6379
   JWT_SECRET_KEY=your-secret-key-change-in-production
   GPU_ENABLED=True  # Set to False if no GPU

Step 3: Start Services
======================

Launch all services with Docker Compose:

.. code-block:: bash

   docker-compose up --build -d

This starts:

- **Backend API:** http://localhost:8000
- **Frontend UI:** http://localhost:5173
- **PostgreSQL:** localhost:5432
- **Redis:** localhost:6379

Wait ~30 seconds for services to initialize.

Step 4: Verify Installation
============================

Check that all services are healthy:

.. code-block:: bash

   docker-compose ps

All services should show ``Up`` status.

.. code-block:: bash

   # Check API health
   curl http://localhost:8000/health

Expected response:

.. code-block:: json

   {
     "status": "healthy",
     "version": "1.0.0",
     "service": "SENTINEL"
   }

Step 5: Access UI
=================

Open your browser and navigate to: **http://localhost:5173**

You should see the SENTINEL command dashboard with:

- Threat Queue (empty initially)
- Risk Index dial
- Metrics cards (uptime, response time)
- Zone risk map
- Camera status grid

Step 6: Create Test Camera
===========================

Register a test camera via API:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/cameras \
     -H "Content-Type: application/json" \
     -d '{
       "name": "CAM-01",
       "zone_id": "zone_1",
       "location": "Main Gate",
       "rtsp_url": "rtsp://192.168.1.100:554/stream"
     }'

Response:

.. code-block:: json

   {
     "id": "cam_abc123def456",
     "name": "CAM-01",
     "zone_id": "zone_1",
     "is_active": true,
     "uptime_percentage": 100.0,
     "created_at": "2024-01-15T10:30:00Z"
   }

Step 7: Create Test Incident
==============================

Create an incident to see it in the dashboard:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/incidents \
     -H "Content-Type: application/json" \
     -d '{
       "zone_id": "zone_1",
       "incident_type": "LOITERING",
       "severity": "HIGH",
       "description": "Test incident for demo",
       "location_lat": 28.6139,
       "location_lng": 77.2090
     }'

Refresh the UI at http://localhost:5173 to see the incident in the Threat Queue.

Step 8: Get System Metrics
===========================

Query system metrics:

.. code-block:: bash

   curl http://localhost:8000/api/v1/metrics?window=1h | jq

Response:

.. code-block:: json

   {
     "uptime_percentage": 99.8,
     "alerts_per_hour": 0.0,
     "average_response_time_minutes": 2.5,
     "total_incidents": 1,
     "active_incidents": 1,
     "camera_count": 1,
     "zone_count": 0
   }

Next Steps
==========

✅ **System is running!** Here's what to do next:

**Explore the API:**
   See :ref:`api-endpoints` for all available endpoints and examples.

**Read the Architecture:**
   Understand the system design in :ref:`guide-architecture`.

**Deploy to Production:**
   Follow :ref:`guide-deployment` for Docker and cloud setup.

**Start Development:**
   Begin with :ref:`dev-setup` if you're a developer.

View Logs
=========

Monitor what's happening:

.. code-block:: bash

   # All services
   docker-compose logs -f

   # Specific service
   docker-compose logs -f backend
   docker-compose logs -f postgres
   docker-compose logs -f redis
   docker-compose logs -f frontend

Access Database
===============

Connect to PostgreSQL to explore the schema:

.. code-block:: bash

   docker-compose exec postgres psql -U sentinel -d sentinel_db

Common commands:

.. code-block:: sql

   -- List tables
   \dt

   -- Query incidents
   SELECT id, incident_type, severity, created_at FROM incidents;

   -- Query cameras
   SELECT id, name, zone_id, is_active FROM cameras;

   -- Exit
   \q

Access Redis
============

Interact with Redis directly:

.. code-block:: bash

   docker-compose exec redis redis-cli

Commands:

.. code-block:: bash

   # Ping Redis
   PING

   # Subscribe to alerts (in another terminal)
   SUBSCRIBE sentinel:alerts

   # Publish test alert
   PUBLISH sentinel:alerts '{"alert_id":"test01","type":"LOITERING"}'

Troubleshooting
===============

**Port already in use:**

.. code-block:: bash

   # Find what's using the port
   lsof -i :8000

   # Kill the process
   kill -9 <PID>

**Database connection error:**

.. code-block:: bash

   # Restart PostgreSQL
   docker-compose restart postgres

   # Check logs
   docker-compose logs postgres

**Frontend can't connect to backend:**

Make sure backend is healthy:

.. code-block:: bash

   curl http://localhost:8000/health

If this fails, restart the backend:

.. code-block:: bash

   docker-compose restart backend

**Memory issues:**

Increase Docker Desktop memory allocation:

1. Docker Desktop → Preferences/Settings
2. Resources → Memory → Increase to 8GB+
3. Restart Docker

Stop Services
=============

When done, stop all services:

.. code-block:: bash

   docker-compose down

To also remove volumes (⚠️ data loss):

.. code-block:: bash

   docker-compose down -v

What's Next?
============

- 📚 Read :ref:`guide-installation` for advanced setup
- 🔌 Explore :ref:`api-endpoints` reference
- 🛠️ Start :ref:`dev-setup` if developing
- 🐳 Review :ref:`guide-deployment` for production

Common Tasks
============

**List all incidents:**

.. code-block:: bash

   curl http://localhost:8000/api/v1/incidents?limit=50 | jq

**Get incident details:**

.. code-block:: bash

   curl http://localhost:8000/api/v1/incidents/{incident_id} | jq

**List alerts:**

.. code-block:: bash

   curl http://localhost:8000/api/v1/alerts?limit=50 | jq

**View API documentation:**

Navigate to: http://localhost:8000/docs

**(Interactive Swagger UI with all endpoints)**

Performance Notes
=================

**Phase 1 Performance (Current):**

- ✅ Single machine, 10 concurrent cameras
- ✅ <100ms API response times
- ✅ Database queries <50ms
- ✅ Real-time updates via Redis

**Phase 4 Performance (Future):**

- 25 concurrent cameras @ 25 FPS
- <60s detection-to-dispatch latency
- >90% alert precision
- >99.5% system uptime

Getting Help
============

- 📖 **Questions?** Check :ref:`resources-faq`
- 🐛 **Found a bug?** `Report on GitHub <https://github.com/your-org/sentinel/issues>`_
- 💬 **Need help?** `GitHub Discussions <https://github.com/your-org/sentinel/discussions>`_

--------

**Congratulations! SENTINEL is now running locally.** ✅

**Continue reading:** :ref:`guide-installation` for advanced configuration

**Last Updated:** March 29, 2026
