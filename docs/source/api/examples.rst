.. _api-examples:

============
API Examples
============

Practical examples for all SENTINEL API endpoints using cURL.

Create Incident
================

Register a new threat incident:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/incidents \
     -H "Content-Type: application/json" \
     -d '{
       "zone_id": "zone_1",
       "incident_type": "PERIMETER_BREACH",
       "severity": "HIGH",
       "description": "Unauthorized entry detected at main gate",
       "location_lat": 28.6139,
       "location_lng": 77.2090
     }'

Response:

.. code-block:: json

   {
     "id": "incident_abc123def456",
     "zone_id": "zone_1",
     "incident_type": "PERIMETER_BREACH",
     "severity": "HIGH",
     "status": "OPEN",
     "description": "Unauthorized entry detected at main gate",
     "location_lat": 28.6139,
     "location_lng": 77.2090,
     "alert_count": 0,
     "detected_at": "2024-01-15T10:30:00Z",
     "created_at": "2024-01-15T10:30:00Z"
   }

List Incidents
==============

Get all incidents:

.. code-block:: bash

   curl http://localhost:8000/api/v1/incidents

With filters:

.. code-block:: bash

   # Filter by zone and severity
   curl "http://localhost:8000/api/v1/incidents?region=zone_1&severity=HIGH"

   # Pagination
   curl "http://localhost:8000/api/v1/incidents?limit=50&offset=100"

   # Combined
   curl "http://localhost:8000/api/v1/incidents?region=zone_1&severity=HIGH&limit=25&offset=0"

Get Single Incident
====================

.. code-block:: bash

   curl http://localhost:8000/api/v1/incidents/incident_abc123def456

Update Incident
================

Change incident status to resolved:

.. code-block:: bash

   curl -X PATCH http://localhost:8000/api/v1/incidents/incident_abc123def456 \
     -H "Content-Type: application/json" \
     -d '{
       "status": "RESOLVED",
       "severity": "LOW"
     }'

Register Camera
================

Add a new CCTV stream:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/cameras \
     -H "Content-Type: application/json" \
     -d '{
       "name": "CAM-01",
       "zone_id": "zone_1",
       "location": "Main Gate",
       "rtsp_url": "rtsp://192.168.1.100:554/stream"
     }'

Register Multiple Cameras
===========================

.. code-block:: bash

   #!/bin/bash

   BASE_URL="http://localhost:8000/api/v1"

   # Camera 1
   curl -X POST $BASE_URL/cameras \
     -H "Content-Type: application/json" \
     -d '{
       "name": "CAM-01",
       "zone_id": "zone_1",
       "location": "Gate 1",
       "rtsp_url": "rtsp://192.168.1.101:554/stream"
     }' | jq .

   # Camera 2
   curl -X POST $BASE_URL/cameras \
     -H "Content-Type: application/json" \
     -d '{
       "name": "CAM-02",
       "zone_id": "zone_2",
       "location": "Gate 2",
       "rtsp_url": "rtsp://192.168.1.102:554/stream"
     }' | jq .

   # Camera 3
   curl -X POST $BASE_URL/cameras \
     -H "Content-Type: application/json" \
     -d '{
       "name": "CAM-03",
       "zone_id": "zone_1",
       "location": "Parking",
       "rtsp_url": "rtsp://192.168.1.103:554/stream"
     }' | jq .

Save this as ``register_cameras.sh`` and run: ``bash register_cameras.sh``

List Cameras
============

.. code-block:: bash

   # All cameras
   curl http://localhost:8000/api/v1/cameras

   # Active only
   curl "http://localhost:8000/api/v1/cameras?active_only=true"

   # By zone
   curl "http://localhost:8000/api/v1/cameras?zone=zone_1"

Get System Metrics
===================

Get metrics for last hour:

.. code-block:: bash

   curl http://localhost:8000/api/v1/metrics?window=1h | jq

Other windows:

.. code-block:: bash

   # Last 6 hours
   curl http://localhost:8000/api/v1/metrics?window=6h | jq

   # Last 24 hours
   curl http://localhost:8000/api/v1/metrics?window=24h | jq

   # Last 7 days
   curl http://localhost:8000/api/v1/metrics?window=7d | jq

Get Risk Dial
==============

Get real-time risk status:

.. code-block:: bash

   curl http://localhost:8000/api/v1/metrics/risk-dial | jq

Expected response:

.. code-block:: json

   {
     "risk_score": 62.5,
     "severity": "MED",
     "high_count": 1,
     "med_count": 3,
     "low_count": 5
   }

Create Alert
=============

Ingest alert from inference engine:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/alerts \
     -H "Content-Type: application/json" \
     -d '{
       "camera_id": "cam_001",
       "alert_type": "LOITERING",
       "severity": "MED",
       "confidence": 0.87,
       "bbox": {"x": 100, "y": 150, "width": 50, "height": 60},
       "metadata": {"track_id": 5, "dwell_time": 120}
     }'

List Alerts
============

.. code-block:: bash

   # Recent alerts
   curl "http://localhost:8000/api/v1/alerts?limit=50"

   # By incident
   curl "http://localhost:8000/api/v1/alerts?incident_id=incident_abc123"

   # By camera
   curl "http://localhost:8000/api/v1/alerts?camera_id=cam_001"

Escalate Alert
===============

Send alert to emergency authorities:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/dispatch/escalate \
     -H "Content-Type: application/json" \
     -d '{
       "alert_ids": ["alert_001", "alert_002"],
       "unit_id": "unit_123",
       "notes": "Perimeter breach, possible intruder"
     }'

Generate Report
=================

Create PDF report for date range:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/reports/generate \
     -H "Content-Type: application/json" \
     -d '{
       "from_date": "2024-01-01T00:00:00Z",
       "to_date": "2024-01-31T23:59:59Z",
       "zone_id": "zone_1"
     }' | jq

Health Check
=============

Verify API is running:

.. code-block:: bash

   curl http://localhost:8000/health

Response:

.. code-block:: json

   {
     "status": "healthy",
     "version": "1.0.0",
     "service": "SENTINEL"
   }

Pretty Output
==============

Add ``| jq`` to format JSON nicely:

.. code-block:: bash

   curl http://localhost:8000/api/v1/incidents | jq '.'

   # Pretty and colorized
   curl http://localhost:8000/api/v1/incidents | jq -C '.'

   # Extract specific fields
   curl http://localhost:8000/api/v1/incidents | jq '.[] | {id: .id, severity: .severity}'

Error Handling
==============

Test invalid request:

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/incidents \
     -H "Content-Type: application/json" \
     -d '{
       "zone_id": "zone_1"
       # Missing required fields
     }'

Response (422 Unprocessable Entity):

.. code-block:: json

   {
     "detail": [
       {
         "loc": ["body", "incident_type"],
         "msg": "field required",
         "type": "value_error.missing"
       }
     ]
   }

Batch Testing Script
====================

Save this as ``test_api.sh``:

.. code-block:: bash

   #!/bin/bash

   set -e  # Exit on error

   BASE_URL="http://localhost:8000/api/v1"
   BLUE='\033[0;34m'
   GREEN='\033[0;32m'
   NC='\033[0m'  # No Color

   echo -e "${BLUE}=== SENTINEL API Test Suite ===${NC}\n"

   # Health check
   echo -e "${BLUE}Testing health check...${NC}"
   curl http://localhost:8000/health | jq .
   echo

   # Create incidents
   echo -e "${BLUE}Creating test incidents...${NC}"
   for i in {1..3}; do
     curl -X POST $BASE_URL/incidents \
       -H "Content-Type: application/json" \
       -d "{
         \"zone_id\": \"zone_1\",
         \"incident_type\": \"LOITERING\",
         \"severity\": $([ $i -eq 1 ] && echo '\"HIGH\"' || echo '\"MED\"'),
         \"description\": \"Test incident $i\"
       }" | jq . > /dev/null
     echo -e "${GREEN}✓ Created incident $i${NC}"
   done
   echo

   # List incidents
   echo -e "${BLUE}Listing incidents...${NC}"
   curl $BASE_URL/incidents | jq '.[] | {id, severity, status}'
   echo

   # Get metrics
   echo -e "${BLUE}Getting metrics...${NC}"
   curl "$BASE_URL/metrics?window=1h" | jq .
   echo

   # Get risk dial
   echo -e "${BLUE}Getting risk dial...${NC}"
   curl "$BASE_URL/metrics/risk-dial" | jq .
   echo

   echo -e "${GREEN}=== All tests passed! ===${NC}"

Run it with: ``bash test_api.sh``

Using Postman
==============

Import endpoints into Postman:

1. Create new collection: "SENTINEL"
2. Create new environment variable: ``base_url`` = ``http://localhost:8000``
3. Add requests:

.. code-block:: text

   POST {{base_url}}/api/v1/incidents
   GET  {{base_url}}/api/v1/incidents
   GET  {{base_url}}/api/v1/metrics
   POST {{base_url}}/api/v1/cameras
   etc.

Using Python
=============

.. code-block:: python

   import requests

   BASE_URL = "http://localhost:8000/api/v1"

   # Create incident
   response = requests.post(
       f"{BASE_URL}/incidents",
       json={
           "zone_id": "zone_1",
           "incident_type": "LOITERING",
           "severity": "HIGH",
           "description": "Test from Python"
       }
   )
   incident = response.json()
   print(f"Created: {incident['id']}")

   # List incidents
   response = requests.get(f"{BASE_URL}/incidents")
   incidents = response.json()
   print(f"Total: {len(incidents)}")

   # Get metrics
   response = requests.get(f"{BASE_URL}/metrics?window=1h")
   metrics = response.json()
   print(f"Uptime: {metrics['uptime_percentage']}%")

Using JavaScript/Node.js
==========================

.. code-block:: javascript

   const axios = require('axios');

   const api = axios.create({
     baseURL: 'http://localhost:8000/api/v1'
   });

   // Create incident
   async function createIncident() {
     const response = await api.post('/incidents', {
       zone_id: 'zone_1',
       incident_type: 'LOITERING',
       severity: 'HIGH',
       description: 'Test from Node.js'
     });
     return response.data;
   }

   // List incidents
   async function listIncidents() {
     const response = await api.get('/incidents?limit=50');
     return response.data;
   }

   async function main() {
     const incident = await createIncident();
     console.log('Created:', incident.id);

     const incidents = await listIncidents();
     console.log('Total:', incidents.length);
   }

   main();

Next Steps
==========

→ Explore the :ref:`api-endpoints` reference for all available operations

→ Check :ref:`resources-troubleshooting` if you encounter errors

--------

**Last Updated:** March 29, 2026
