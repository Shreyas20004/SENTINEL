.. _api-overview:

========
Overview
========

REST API reference and usage guide.

API Base URL
============

**Development:**

.. code-block:: text

   http://localhost:8000/api/v1

**Production:**

.. code-block:: text

   https://sentinel.yourdomain.com/api/v1

API Tiers
=========

**Tier 1 - Public (No Auth)**

Phase 1 endpoints. All unauthenticated access.

**Tier 2 - Protected (API Key)**

Phase 3. Requires ``X-API-Key`` header.

**Tier 3 - Authenticated (JWT)**

Phase 4. Requires ``Authorization: Bearer <token>`` header.

Request Format
==============

All requests use standard HTTP methods:

- **GET** - Retrieve resource
- **POST** - Create resource
- **PATCH** - Partially update resource
- **DELETE** - Remove resource (Phase 3)

Content-Type: ``application/json``

Response Format
===============

All responses are JSON:

.. code-block:: json

   {
     "data": {...},
     "meta": {
       "timestamp": "2024-01-15T10:30:00Z",
       "version": "1.0.0"
     }
   }

Error responses:

.. code-block:: json

   {
     "error": "Not found",
     "status": 404,
     "trace_id": "abc123xyz789"
   }

API Documentation
==================

**Auto-generated Swagger UI:**

Visit: http://localhost:8000/docs

**Auto-generated ReDoc:**

Visit: http://localhost:8000/redoc

Both auto-generated from OpenAPI specification.

Common Patterns
===============

**Filtering:**

.. code-block:: bash

   GET /api/v1/incidents?severity=HIGH&status=OPEN

**Pagination:**

.. code-block:: bash

   GET /api/v1/incidents?limit=50&offset=100

**Sorting:**

.. code-block:: bash

   GET /api/v1/incidents?sort_by=created_at&order=desc

**Time Range (Phase 3):**

.. code-block:: bash

   GET /api/v1/incidents?from=2024-01-01T00:00:00Z&to=2024-01-31T23:59:59Z

Rate Limiting (Phase 4)
======================

**Limits:**

- 1000 requests/hour per IP
- 10000 requests/hour per API key

**Headers returned:**

.. code-block:: text

   X-RateLimit-Limit: 1000
   X-RateLimit-Remaining: 999
   X-RateLimit-Reset: 1705329600

Example with curl:

.. code-block:: bash

   curl -i http://localhost:8000/api/v1/incidents | grep X-RateLimit

Authentication (Phase 4)
========================

**API Key (Service-to-Service):**

.. code-block:: bash

   curl -H "X-API-Key: your-api-key" \
     http://localhost:8000/api/v1/incidents

**JWT Token (User Auth):**

.. code-block:: bash

   # Get token (Phase 4)
   TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
     -d '{"username":"operator1","password":"..."}' | jq .token)
   
   # Use token
   curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/v1/incidents

Webhooks (Phase 3)
===================

Subscribe to incident events:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/webhooks \
     -H "Content-Type: application/json" \
     -d '{
       "event": "incident.created",
       "url": "https://your-server.com/webhooks/incidents"
     }'

SENTINEL will POST to your URL:

.. code-block:: json

   {
     "event": "incident.created",
     "timestamp": "2024-01-15T10:30:00Z",
     "data": {
       "id": "incident_abc123",
       "severity": "HIGH",
       ...
     }
   }

Bulk Operations (Phase 3)
==========================

**Batch create incidents:**

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/incidents/batch \
     -H "Content-Type: application/json" \
     -d '[
       {"zone_id": "zone_1", "incident_type": "LOITERING", ...},
       {"zone_id": "zone_2", "incident_type": "CROWD_SURGE", ...}
     ]'

**Expected response:**

.. code-block:: json

   {
     "success": 2,
     "failed": 0,
     "ids": ["incident_1", "incident_2"]
   }

GraphQL API (Phase 4)
=====================

Alternative to REST for complex queries:

.. code-block:: graphql

   query {
     incidents(severity: HIGH, status: OPEN) {
       id
       zone { name }
       alerts(limit: 10) {
         cameraid
         confidence
       }
     }
   }

Client Libraries (Phase 3)
===========================

**Python:**

.. code-block:: python

   from sentinel_client import SentinelAPI
   
   client = SentinelAPI(api_key='...')
   incidents = client.incidents.list(severity='HIGH')

**JavaScript/TypeScript:**

.. code-block:: typescript

   import { SentinelClient } from 'sentinel-client-js';
   
   const client = new SentinelClient({ apiKey: '...' });
   const incidents = await client.incidents.list({ severity: 'HIGH' });

**Go:**

.. code-block:: go

   import "github.com/sentinel-ai/sentinel-go"
   
   client := sentinel.NewClient("api-key")
   incidents := client.Incidents.List(ctx, &sentinel.FilterOptions{
     Severity: "HIGH",
   })

SDK Documentation Coming Phase 3.

Testing API
===========

**Using cURL:**

.. code-block:: bash

   curl -X GET http://localhost:8000/api/v1/health -v

**Using Postman:**

1. Import OpenAPI spec: http://localhost:8000/openapi.json
2. Use environment variables for base_url
3. Test each endpoint

**Using Python:**

.. code-block:: python

   import requests
   
   response = requests.get('http://localhost:8000/api/v1/incidents')
   print(response.json())

Backward Compatibility
======================

**API Versions:**

- v1: Current (Phase 1+)
- v2: Planned (Phase 4)

All breaking changes announced 6 months in advance. v1 supported for 2 years minimum.

**Deprecation notices:**

Old endpoint: ``GET /incidents`` (deprecated in v3)

New endpoint: ``GET /incidents/list`` (preferred)

Both work for 1 year.

Next Steps
==========

→ See :ref:`api-endpoints` for complete endpoint reference

→ Check :ref:`api-examples` for practical cURL examples

→ Review :ref:`api-schemas` for request/response models

--------

**Last Updated:** March 29, 2026
