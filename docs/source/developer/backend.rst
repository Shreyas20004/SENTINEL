.. _developer-backend:

===============
Backend Guide
===============

Deep-dive guide for backend development.

Backend Stack
==============

- **Framework:** FastAPI 0.104.1 (async-first ASGI)
- **ORM:** SQLAlchemy 2.0.23 (async support via asyncpg)
- **Database:** PostgreSQL 16 + PostGIS 3.4
- **Cache:** Redis 7.2 (pub/sub, session)
- **Validation:** Pydantic 2.5.0 (type hints)
- **ASGI Server:** Uvicorn 0.24 (production: Gunicorn)
- **Testing:** pytest 7.4 + pytest-asyncio

FastAPI Application Structure
==============================

**Entry Point: `app/main.py`**

.. code-block:: python

   from fastapi import FastAPI
   from contextlib import asynccontextmanager
   
   @asynccontextmanager
   async def lifespan(app: FastAPI):
       # Startup logic
       await init_db()
       redis_client.connect()
       yield
       # Shutdown logic
       await redis_client.disconnect()
   
   app = FastAPI(lifespan=lifespan)
   
   @app.get("/health")
   async def health():
       return {"status": "healthy"}
   
   app.include_router(incidents.router)
   app.include_router(alerts.router)
   # ... other routers

**Key patterns:**

1. **Lifespan context manager** handles DB/Redis connections
2. **Router modules** define endpoint groups
3. **Dependency injection** for database session access
4. **Async/await throughout** for I/O-bound operations

Database Access Patterns
========================

**Get database session:**

.. code-block:: python

   from app.core.database import get_db
   
   @app.get("/incidents")
   async def list_incidents(db: AsyncSession = Depends(get_db)):
       result = await db.execute(select(Incident).limit(10))
       return result.scalars().all()

**Create new record:**

.. code-block:: python

   @app.post("/incidents")
   async def create_incident(
       incident: IncidentCreate,
       db: AsyncSession = Depends(get_db)
   ):
       db_incident = Incident(**incident.dict())
       db.add(db_incident)
       await db.commit()
       await db.refresh(db_incident)
       return db_incident

**Query with filters:**

.. code-block:: python

   from sqlalchemy import select, and_
   
   stmt = select(Incident).where(
       and_(
           Incident.zone_id == zone_id,
           Incident.severity == "HIGH",
           Incident.created_at > cutoff_time
       )
   ).order_by(Incident.created_at.desc())
   
   result = await db.execute(stmt)
   incidents = result.scalars().all()

**Transaction management:**

.. code-block:: python

   async with db.begin():  # Auto-commit/rollback
       db.add(incident)
       # If exception: auto-rollback
   # If success: auto-commit

Error Handling & Logging
==========================

**Custom exception handlers:**

.. code-block:: python

   from fastapi import HTTPException
   
   class IncidentNotFound(HTTPException):
       def __init__(self, incident_id: str):
           super().__init__(
               status_code=404,
               detail=f"Incident {incident_id} not found"
           )
   
   @app.get("/incidents/{incident_id}")
   async def get_incident(incident_id: str, db: AsyncSession = Depends(get_db)):
       incident = await db.get(Incident, incident_id)
       if not incident:
           raise IncidentNotFound(incident_id)
       return incident

**Structured logging:**

.. code-block:: python

   import logging
   import json
   
   logger = logging.getLogger(__name__)
   
   @app.post("/incidents")
   async def create_incident(...):
       logger.info(json.dumps({
           "action": "create_incident",
           "zone_id": incident.zone_id,
           "severity": incident.severity,
           "timestamp": datetime.utcnow().isoformat()
       }))

Redis Integration
=================

**Pub/Sub pattern (alert broadcasting):**

.. code-block:: python

   from app.core.redis_client import redis_client
   
   @app.post("/alerts")
   async def create_alert(alert: AlertCreate, db: AsyncSession = Depends(get_db)):
       # Save to database
       db_alert = Alert(**alert.dict())
       db.add(db_alert)
       await db.commit()
       
       # Publish to subscribers
       message = alert.dict()
       await redis_client.publish("sentinel:alerts", json.dumps(message))
       
       return db_alert

**Caching pattern:**

.. code-block:: python

   @app.get("/metrics/risk-dial")
   async def get_risk_dial():
       # Check cache first
       cached = await redis_client.get("risk_dial")
       if cached:
           return json.loads(cached)
       
       # Compute if not cached
       result = compute_risk_dial()
       
       # Store with TTL
       await redis_client.set(
           "risk_dial",
           json.dumps(result),
           ex=300  # 5 min TTL
       )
       
       return result

Testing Backend Code
====================

**Unit test example:**

.. code-block:: python

   import pytest
   from httpx import AsyncClient
   from app.main import app
   
   @pytest.mark.asyncio
   async def test_create_incident():
       async with AsyncClient(app=app, base_url="http://test") as client:
           response = await client.post(
               "/api/v1/incidents",
               json={
                   "zone_id": "zone_1",
                   "incident_type": "LOITERING",
                   "severity": "HIGH",
                   "description": "Test"
               }
           )
           assert response.status_code == 201
           data = response.json()
           assert data["zone_id"] == "zone_1"

**Database fixtures:**

.. code-block:: python

   @pytest.fixture
   async def db_session():
       db = AsyncSessionLocal()
       yield db
       await db.rollback()  # Don't persist test data
   
   @pytest.mark.asyncio
   async def test_list_incidents(db_session):
       # Create test data
       incident = Incident(zone_id="test", severity="HIGH")
       db_session.add(incident)
       await db_session.commit()
       
       # Query
       result = await db_session.execute(select(Incident))
       incidents = result.scalars().all()
       assert len(incidents) == 1

Performance Optimization
==========================

**N+1 Query Prevention:**

.. code-block:: python

   # Bad (N+1):
   incidents = await db.execute(select(Incident))
   for incident in incidents:
       print(incident.alerts)  # Separate DB query per incident!
   
   # Good (eager load):
   from sqlalchemy.orm import selectinload
   
   stmt = select(Incident).options(
       selectinload(Incident.alerts)
   )
   incidents = await db.execute(stmt)

**Index optimization:**

Edit `models.py`:

.. code-block:: python

   class Incident(Base):
       __tablename__ = "incidents"
       
       # Composite index for common queries
       __table_args__ = (
           Index('idx_incidents_zone_severity', 'zone_id', 'severity', 'created_at'),
       )

**Connection pooling:**

Environment variables in `.env`:

.. code-block:: bash

   DB_POOL_SIZE=20
   DB_POOL_RECYCLE=3600

Deployment Best Practices
==========================

**Use Gunicorn for production:**

.. code-block:: bash

   # Instead of uvicorn
   gunicorn app.main:app \
     --workers 4 \     # CPU-bound
     --worker-class uvicorn.workers.UvicornWorker \
     --bind 0.0.0.0:8000 \
     --timeout 60

**Health check endpoint:**

.. code-block:: python

   @app.get("/health")
   async def health(db: AsyncSession = Depends(get_db)):
       # Verify database connectivity
       try:
           await db.execute(select(1))
       except Exception:
           raise HTTPException(status_code=503)
       
       return {
           "status": "healthy",
           "database": "connected",
           "redis": "connected"
       }

**Graceful shutdown:**

.. code-block:: python

   import signal
   import asyncio
   
   async def shutdown_signal():
       await redis_client.disconnect()
       await db_engine.dispose()

Debugging & Profiling
=====================

**Enable debug logging:**

.. code-block:: bash

   LOG_LEVEL=DEBUG uvicorn app.main:app --reload

**Profile with cProfile:**

.. code-block:: bash

   python -m cProfile -s cumulative app/main.py

**Memory profiling:**

.. code-block:: bash

   pip install memory-profiler
   python -m memory_profiler app/main.py

Next Steps
==========

→ See :ref:`developer-testing` for comprehensive testing guide

→ Check :ref:`api-endpoints` for endpoint details

--------

**Last Updated:** March 29, 2026
