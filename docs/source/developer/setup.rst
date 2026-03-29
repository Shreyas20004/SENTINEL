.. _developer-setup:

==========================
Developer Setup
==========================

Step-by-step guide to set up your development environment for SENTINEL.

Prerequisites
==============

**Required:**

- Git
- Docker & Docker Compose (v20.10+)
- Python 3.11 (for backend development)
- Node.js 20+ and npm (for frontend development)
- 8GB RAM minimum (16GB recommended for GPU)
- 20GB disk space

**Optional:**

- NVIDIA GPU with CUDA 12.1 support (for fast YOLOv8 inference)
- Postman (for API testing)
- PostgreSQL client tools (for database debugging)
- Redis CLI (for cache debugging)

Clone Repository
=================

.. code-block:: bash

   git clone https://github.com/yourusername/SENTINEL.git
   cd SENTINEL
   git checkout development

Environment Setup
==================

**Step 1: Create .env file**

.. code-block:: bash

   cp .env.example .env

**Step 2: Edit .env with development settings**

.. code-block:: bash

   # Database
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/sentinel_dev
   
   # Redis
   REDIS_URL=redis://localhost:6379/0
   
   # API
   API_HOST=0.0.0.0
   API_PORT=8000
   API_RELOAD=true
   DEBUG=true
   
   # AI/ML
   GPU_ENABLED=false  # Set true if you have NVIDIA GPU
   YOLO_CONFIDENCE_THRESHOLD=0.5
   
   # Frontend
   VITE_API_URL=http://localhost:8000

**Step 3: Verify variables**

.. code-block:: bash

   cat .env | grep -v "^#" | grep -v "^$"

Backend Development
====================

**1. Start Docker services (PostgreSQL, Redis)**

.. code-block:: bash

   docker-compose up -d postgres redis

Verify they're running:

.. code-block:: bash

   docker-compose ps

Expected:

:: 

   NAME        STATUS
   postgres    Up (healthy)
   redis       Up

**2. Create Python virtual environment**

.. code-block:: bash

   python3.11 -m venv venv_backend
   
   # Activate
   # On Unix/macOS:
   source venv_backend/bin/activate
   
   # On Windows:
   venv_backend\Scripts\activate

**3. Install dependencies**

.. code-block:: bash

   pip install -r backend/requirements.txt

Verify installation:

.. code-block:: bash

   python -c "import fastapi; import sqlalchemy; print('OK')"

**4. Initialize database**

.. code-block:: bash

   cd backend
   python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"
   cd ..

Expected output: Tables created, PostGIS extension enabled.

**5. Start backend dev server**

.. code-block:: bash

   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Visit: http://localhost:8000/docs (OpenAPI interactive docs)

Exit with: ``Ctrl+C``

Frontend Development
======================

**1. Create Node.js virtual environment**

.. code-block:: bash

   cd frontend
   nvm use 20
   npm install

   # Verify
   npm --version
   node --version

**2. Start dev server**

.. code-block:: bash

   npm run dev

Visit: http://localhost:5173 (Vite hot reload enabled)

Exit with: ``Ctrl+C``

**3. Type checking**

TypeScript will auto-compile, but check for errors:

.. code-block:: bash

   npm run type-check

**4. Linting**

.. code-block:: bash

   npm run lint

Complete Development Setup
============================

Run all services at once using Docker Compose:

.. code-block:: bash

   docker-compose up

Services:

.. list-table::
   :widths: 20 15 40
   :header-rows: 1

   * - Service
     - Port
     - URL
   * - **PostgreSQL**
     - 5432
     - (Internal only)
   * - **Redis**
     - 6379
     - (Internal only)
   * - **Backend**
     - 8000
     - http://localhost:8000
   * - **Frontend**
     - 5173
     - http://localhost:5173 (via npm run dev)

Health Check
=============

Verify all services are running:

.. code-block:: bash

   #!/bin/bash

   echo "Checking API..."
   curl -s http://localhost:8000/health | jq .

   echo "Checking database..."
   psql postgresql://postgres:postgres@localhost:5432/sentinel_dev -c "SELECT version();"

   echo "Checking Redis..."
   redis-cli ping

   echo "All services OK!"

Database Access
================

**Using psql client:**

.. code-block:: bash

   psql postgresql://postgres:postgres@localhost:5432/sentinel_dev

**Common queries:**

.. code-block:: sql

   -- List tables
   \dt

   -- Count incidents
   SELECT COUNT(*) FROM incidents;

   -- Recent incidents
   SELECT id, incident_type, severity, created_at 
   FROM incidents 
   ORDER BY created_at DESC 
   LIMIT 10;

   -- Zone risk scores
   SELECT name, risk_score, severity 
   FROM zones 
   ORDER BY risk_score DESC;

Exit with: ``\q``

**Using pgAdmin (web interface):**

After ``docker-compose up``, visit: http://localhost:5050

Login: ``admin@example.com`` / ``admin``

Redis Access
=============

**Using redis-cli:**

.. code-block:: bash

   redis-cli

**Common commands:**

.. code-block:: bash

   # Check connection
   PING

   # List all keys
   KEYS *

   # Get all alerts (if any)
   SUBSCRIBE sentinel:alerts

   # Check memory
   INFO memory

Exit with: ``exit``

Code Structure
===============

.. code-block:: text

   SENTINEL/
   ├── backend/
   │   ├── app/
   │   │   ├── main.py              # FastAPI entry point
   │   │   ├── core/
   │   │   │   ├── config.py        # Settings
   │   │   │   ├── database.py      # DB connection
   │   │   │   └── redis_client.py  # Redis wrapper
   │   │   ├── models.py            # SQLAlchemy ORM
   │   │   ├── schemas.py           # Pydantic validation
   │   │   ├── api/
   │   │   │   ├── incidents.py     # Incident endpoints
   │   │   │   ├── alerts.py        # Alert endpoints
   │   │   │   ├── metrics.py       # Metrics endpoints
   │   │   │   ├── cameras.py       # Camera endpoints
   │   │   │   ├── zones.py         # Zone endpoints
   │   │   │   ├── dispatch.py      # Dispatch endpoints
   │   │   │   └── reports.py       # Report endpoints
   │   │   ├── models/
   │   │   │   ├── yolo_inference.py
   │   │   │   ├── frame_capture.py
   │   │   │   └── tracking.py
   │   │   └── analytics/
   │   │       ├── rules.py
   │   │       └── scoring.py
   │   └── requirements.txt
   │
   ├── frontend/
   │   ├── src/
   │   │   ├── main.tsx             # Entry point
   │   │   ├── App.tsx              # Router
   │   │   ├── services/
   │   │   │   ├── api.ts           # API client
   │   │   │   └── websocket.ts     # WebSocket client
   │   │   ├── components/
   │   │   │   ├── CommandDashboard.tsx
   │   │   │   ├── ThreatQueue.tsx
   │   │   │   ├── MetricsCard.tsx
   │   │   │   ├── CameraGrid.tsx
   │   │   │   └── LiveMap.tsx
   │   │   ├── index.html
   │   │   ├── config.ts
   │   │   └── index.css
   │   ├── package.json
   │   ├── vite.config.ts
   │   ├── tailwind.config.js
   │   └── tsconfig.json
   │
   └── docker-compose.yml

Git Workflow
=============

**Create feature branch:**

.. code-block:: bash

   git checkout -b feature/your-feature-name

**Push changes:**

.. code-block:: bash

   git add .
   git commit -m "feat: Add new feature description"
   git push origin feature/your-feature-name

**Create Pull Request** (on GitHub)

Testing
==========

**Backend unit tests (Phase 1 task):**

.. code-block:: bash

   cd backend
   pytest tests/ -v

**Frontend component tests (Phase 1 task):**

.. code-block:: bash

   cd frontend
   npm run test

**API integration tests:**

.. code-block:: bash

   bash backend/test_api.sh

Common Development Tasks
=========================

**Reset database:**

.. code-block:: bash

   docker-compose down postgres
   docker-compose up -d postgres
   cd backend && python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"

**View logs:**

.. code-block:: bash

   docker-compose logs -f backend
   docker-compose logs -f frontend

**Kill all services:**

.. code-block:: bash

   docker-compose down

**Full restart:**

.. code-block:: bash

   docker-compose down
   docker-compose up

Debugging Tips
===============

**Backend API issues:**

1. Check logs: ``docker-compose logs -f backend``
2. Verify database: ``psql postgresql://postgres:postgres@localhost:5432/sentinel_dev``
3. Test endpoint: ``curl http://localhost:8000/health``

**Frontend issues:**

1. Check browser console: F12 (DevTools)
2. Check Vite logs: See terminal where ``npm run dev`` is running
3. Clear cache: ``rm -rf frontend/node_modules/.vite``

**Database issues:**

1. Verify container: ``docker-compose ps postgres``
2. Check logs: ``docker-compose logs postgres``
3. Rebuild: ``docker-compose build --no-cache postgres``

**Redis issues:**

1. Check connection: ``redis-cli ping``
2. Monitor: ``redis-cli MONITOR``
3. Clear cache: ``redis-cli FLUSHDB``

Performance Profiling
======================

**Backend (Python cProfile):**

.. code-block:: bash

   python -m cProfile -s cumtime backend/app/main.py

**Frontend (Chrome DevTools):**

1. Open DevTools (F12)
2. Performance tab
3. Record and analyze

Memory Profiling
=================

**Backend (Memory profiler):**

.. code-block:: bash

   pip install memory-profiler
   python -m memory_profiler backend/app/main.py

IDE Setup
==========

**VS Code (Recommended)**

Extensions:

- Python (Microsoft)
- Pylance (Microsoft)
- FastAPI (Developed)
- ES7+ React/Redux/React-Native snippets (dsznajder.es7-react-js-snippets)
- Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)
- TypeScript Vue Plugin (Vue)
- Prettier - Code formatter (esbenp.prettier-vscode)

**PyCharm Professional**

Built-in support for Python, FastAPI, Docker, PostgreSQL.

**VS Code Settings (.vscode/settings.json):**

.. code-block:: json

   {
     "python.defaultInterpreterPath": "${workspaceFolder}/venv_backend/bin/python",
     "python.linting.pylintEnabled": true,
     "python.linting.pylintPath": "${workspaceFolder}/venv_backend/bin/pylint",
     "[python]": {
       "editor.defaultFormatter": "ms-python.python",
       "editor.formatOnSave": true,
       "editor.codeActionsOnSave": {
         "source.organizeImports": true
       }
     },
     "[typescript]": {
       "editor.defaultFormatter": "esbenp.prettier-vscode",
       "editor.formatOnSave": true
     }
   }

Next Steps
==========

→ Read :ref:`developer-backend` for backend architecture details

→ Read :ref:`developer-frontend` for frontend patterns

→ See :ref:`developer-testing` for comprehensive testing guide

--------

**Last Updated:** March 29, 2026
