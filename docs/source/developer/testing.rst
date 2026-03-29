.. _developer-testing:

=======
Testing
=======

Comprehensive testing guide for SENTINEL.

Testing Pyramid
================

.. code-block:: text

   △
   │  End-to-End Tests (5%)
   │  - Full system integration
   │  - Real browsers, real APIs
   │
   │  Integration Tests (15%)
   │  - Multiple components
   │  - Database + API + Cache
   │
   │  Unit Tests (80%)
   │  - Single functions
   │  - Mocked dependencies
   ▽

Unit Test Strategy
===================

**Python backend unit tests:**

.. code-block:: bash

   cd backend
   pytest tests/unit/ -v --cov=app --cov-report=term-missing

**Test structure:**

.. code-block:: text

   backend/tests/
   ├── unit/
   │   ├── api/
   │   │   ├── test_incidents.py
   │   │   ├── test_alerts.py
   │   │   └── test_metrics.py
   │   ├── models/
   │   │   ├── test_yolo.py (Phase 2)
   │   │   └── test_tracking.py (Phase 2)
   │   └── services/
   │       └── test_redis.py
   │
   ├── integration/
   │   ├── test_api.py
   │   └── test_database.py
   │
   └── conftest.py

**Example unit test:**

.. code-block:: python

   import pytest
   from unittest.mock import AsyncMock, patch
   
   @pytest.mark.asyncio
   async def test_get_incidents_filters_by_severity():
       # Mock database
       mock_db = AsyncMock()
       mock_db.execute.return_value.scalars.return_value.all.return_value = [
           Incident(id="1", severity="HIGH"),
           Incident(id="2", severity="HIGH")
       ]
       
       # Call endpoint
       result = await get_incidents(severity="HIGH", db=mock_db)
       
       # Assert
       assert len(result) == 2
       assert all(i.severity == "HIGH" for i in result)

**Mocking patterns:**

.. code-block:: python

   # Mock external service
   @patch('app.services.redis_client.publish')
   async def test_create_alert_publishes(mock_publish):
       await create_alert(...)
       mock_publish.assert_called_once()

   # Mock database
   from sqlalchemy.pool import StaticPool
   
   @pytest.fixture
   def db():
       engine = create_async_engine(
           "sqlite+aiosqlite:///:memory:",
           poolclass=StaticPool
       )
       yield engine

**Running tests:**

.. code-block:: bash

   # Run all tests
   pytest

   # Run specific test file
   pytest tests/unit/api/test_incidents.py

   # Run with coverage
   pytest --cov=app --cov-report=html

   # Run in watch mode
   ptw  # pip install pytest-watch

Frontend Unit Tests
====================

**React component testing:**

.. code-block:: bash

   cd frontend
   npm run test

**Test structure:**

.. code-block:: text

   frontend/src/__tests__/
   ├── components/
   │   ├── CommandDashboard.test.tsx
   │   ├── ThreatQueue.test.tsx
   │   └── MetricsCard.test.tsx
   │
   ├── services/
   │   ├── api.test.ts
   │   └── websocket.test.ts
   │
   └── hooks/
       └── useAlerts.test.ts

**Example React test (Vitest):**

.. code-block:: typescript

   import { describe, it, expect, vi } from 'vitest';
   import { render, screen } from '@testing-library/react';
   import ThreatQueue from './ThreatQueue';
   
   describe('ThreatQueue', () => {
     it('displays incidents in severity order', async () => {
       const incidents = [
         { id: '1', severity: 'MED' },
         { id: '2', severity: 'HIGH' },
         { id: '3', severity: 'LOW' }
       ];
       
       vi.mocked(apiClient.getIncidents).mockResolvedValue(incidents);
       
       render(<ThreatQueue />);
       
       const items = await screen.findAllByRole('listitem');
       expect(items[0]).toHaveTextContent('HIGH');
       expect(items[1]).toHaveTextContent('MED');
       expect(items[2]).toHaveTextContent('LOW');
     });
   });

Integration Tests
==================

**API integration test:**

.. code-block:: python

   @pytest.mark.asyncio
   async def test_create_and_retrieve_incident():
       # Create incident
       response = await client.post(
           "/api/v1/incidents",
           json={
               "zone_id": "zone_1",
               "incident_type": "LOITERING",
               "severity": "HIGH"
           }
       )
       assert response.status_code == 201
       incident_id = response.json()["id"]
       
       # Retrieve it
       response = await client.get(f"/api/v1/incidents/{incident_id}")
       assert response.status_code == 200
       data = response.json()
       assert data["zone_id"] == "zone_1"

**Database + API integration:**

.. code-block:: python

   @pytest.mark.asyncio
   async def test_incident_persists_in_database(db_session):
       # Create via API
       incident = Incident(zone_id="zone_1", severity="HIGH")
       db_session.add(incident)
       await db_session.commit()
       
       # Query directly from DB
       result = await db_session.execute(
           select(Incident).where(Incident.zone_id == "zone_1")
       )
       retrieved = result.scalar_one()
       assert retrieved.zone_id == "zone_1"

End-to-End Tests
================

**Full system test (using Playwright):**

.. code-block:: python

   import pytest
   from playwright.async_api import async_playwright
   
   @pytest.mark.asyncio
   async def test_create_incident_appears_on_dashboard():
       async with async_playwright() as p:
           browser = await p.chromium.launch()
           page = await browser.new_page()
           
           # Navigate to dashboard
           await page.goto("http://localhost:5173")
           
           # Create incident via API
           await page.request.post(
               "http://localhost:8000/api/v1/incidents",
               data={
                   "zone_id": "zone_1",
                   "incident_type": "LOITERING",
                   "severity": "HIGH"
               }
           )
           
           # Assert it appears on page
           threat_item = await page.get_by_role("listitem").first
           assert "LOITERING" in await threat_item.text_content()
           
           await browser.close()

**Run E2E tests:**

.. code-block:: bash

   pytest tests/e2e/ --browser=chromium

Test Coverage Goals
===================

.. list-table::
   :widths: 20 20
   :header-rows: 1

   * - Component
     - Target Coverage
   * - Models
     - 100%
   * - Schemas
     - 95%
   * - API Endpoints
     - >90%
   * - Services
     - >85%
   * - Database
     - >80%
   * - Frontend Components
     - >80%
   * - Hooks
     - >85%

**Current Phase 1 status:**

.. list-table::
   :widths: 20 15
   :header-rows: 1

   * - Component
     - Coverage
   * - Backend
     - 0% (Phase 1 task)
   * - Frontend
     - 0% (Phase 1 task)

Performance Testing
===================

**Load testing with Locust:**

.. code-block:: python

   from locust import HttpUser, task, between
   
   class SentinelUser(HttpUser):
       wait_time = between(1, 3)
       
       @task
       def get_incidents(self):
           self.client.get("/api/v1/incidents")
       
       @task
       def get_metrics(self):
           self.client.get("/api/v1/metrics")

**Run load test:**

.. code-block:: bash

   locust -f locustfile.py --host http://localhost:8000 --users 100 --spawn-rate 10

**Expected results (Phase 1):**

- Latency: <200ms for GET /incidents
- Throughput: >1000 req/sec
- Error rate: <0.1%

Continuous Integration (Phase 4)
=================================

**GitHub Actions workflow (.github/workflows/test.yml):**

.. code-block:: yaml

   name: Tests
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - run: pip install -r backend/requirements-test.txt
         - run: pytest backend/tests/ --cov
         
     frontend:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-node@v3
           with:
             node-version: '20'
         - run: cd frontend && npm install && npm run test

Test Data Management
=====================

**Fixtures for repeatable tests:**

.. code-block:: python

   @pytest.fixture
   def sample_incident():
       return {
           "zone_id": "zone_1",
           "incident_type": "LOITERING",
           "severity": "HIGH",
           "description": "Test incident"
       }
   
   @pytest.mark.asyncio
   async def test_something(sample_incident):
       result = await create_incident(sample_incident)
       assert result.zone_id == "zone_1"

**Test database population:**

.. code-block:: python

   @pytest.fixture
   async def populated_db(db_session):
       # Add sample data
       for i in range(10):
           incident = Incident(
               zone_id=f"zone_{i % 3}",
               severity=["LOW", "MED", "HIGH"][i % 3]
           )
           db_session.add(incident)
       await db_session.commit()
       yield db_session

Debugging Tests
================

**Verbose output:**

.. code-block:: bash

   pytest -vv --tb=long

**Drop into debugger on failure:**

.. code-block:: bash

   pytest --pdb

**Run single test:**

.. code-block:: bash

   pytest tests/unit/api/test_incidents.py::test_create_incident -vv

**Print debug statements:**

.. code-block:: python

   import logging
   logging.basicConfig(level=logging.DEBUG)
   
   def test_something():
       print("Debug info here")
       logging.debug("More details")

Next Steps
==========

→ See :ref:`developer-setup` for environment setup

→ Check :ref:`developer-backend` for detailed backend patterns

--------

**Last Updated:** March 29, 2026
