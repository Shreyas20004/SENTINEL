.. _api-schemas:

================
Request/Response
================

Complete reference for all request and response data models.

Incident Schema
================

**Incident Object (Response):**

.. code-block:: json

   {
     "id": "incident_abc123def456",
     "zone_id": "zone_1",
     "incident_type": "LOITERING",
     "severity": "MED",
     "status": "OPEN",
     "description": "Person loitering at main gate for 10 minutes",
     "location_lat": 28.6139,
     "location_lng": 77.2090,
     "alert_count": 2,
     "detected_at": "2024-01-15T10:30:00Z",
     "resolved_at": null,
     "created_at": "2024-01-15T10:30:00Z",
     "updated_at": "2024-01-15T10:35:00Z"
   }

**Create Incident (Request):**

.. code-block:: json

   {
     "zone_id": "zone_1",
     "incident_type": "LOITERING",
     "severity": "MED",
     "description": "Test incident",
     "location_lat": 28.6139,
     "location_lng": 77.2090
   }

**Enums:**

- **incident_type**: LOITERING, CROWD_SURGE, ABANDONED_OBJECT, PERIMETER_BREACH
- **severity**: LOW, MED, HIGH
- **status**: OPEN, INVESTIGATING, RESOLVED, FALSE_ALARM

Alert Schema
============

**Alert Object:**

.. code-block:: json

   {
     "id": "alert_xyz789abc123",
     "incident_id": "incident_abc123def456",
     "camera_id": "cam_001",
     "alert_type": "LOITERING",
     "severity": "MED",
     "confidence": 0.87,
     "bbox": {
       "x1": 100,
       "y1": 150,
       "x2": 180,
       "y2": 250
     },
     "metadata": {
       "track_id": 5,
       "dwell_time": 120,
       "frame_count": 30
     },
     "is_duplicate": false,
     "is_confirmed": false,
     "created_at": "2024-01-15T10:30:15Z"
   }

Camera Schema
=============

**Camera Object:**

.. code-block:: json

   {
     "id": "cam_abc123def456",
     "name": "CAM-01",
     "zone_id": "zone_1",
     "location": "Main Gate",
     "rtsp_url": "rtsp://192.168.1.100:554/stream",
     "is_active": true,
     "uptime_percentage": 99.8,
     "last_heartbeat": "2024-01-15T10:35:00Z",
     "created_at": "2024-01-15T00:00:00Z"
   }

Zone Schema
===========

**Zone Object:**

.. code-block:: json

   {
     "id": "zone_1",
     "name": "Main Gate",
     "risk_score": 50.0,
     "severity": "MED",
     "created_at": "2024-01-01T00:00:00Z",
     "updated_at": "2024-01-15T10:30:00Z"
   }

Metrics Schema
==============

**Metrics Response:**

.. code-block:: json

   {
     "uptime_percentage": 99.8,
     "alerts_per_hour": 2.3,
     "average_response_time_minutes": 2.5,
     "total_incidents": 156,
     "active_incidents": 3,
     "camera_count": 12,
     "zone_count": 5
   }

**Risk Dial Response:**

.. code-block:: json

   {
     "risk_score": 62.5,
     "severity": "MED",
     "high_count": 1,
     "med_count": 3,
     "low_count": 5
   }

Error Schema
============

**Error Response:**

.. code-block:: json

   {
     "detail": "Incident not found",
     "status": 404,
     "type": "NOT_FOUND"
   }

**Validation Error (422):**

.. code-block:: json

   {
     "detail": [
       {
         "loc": ["body", "incident_type"],
         "msg": "value is not a valid enumeration member",
         "type": "type_error.enum"
       }
     ]
   }

Field Types & Validation
=========================

.. list-table::
   :widths: 15 15 50
   :header-rows: 1

   * - Field
     - Type
     - Validation
   * - **id**
     - string (UUID)
     - Format: ``incident_abc123def456``
   * - **zone_id**
     - string
     - Required, max 50 chars
   * - **severity**
     - enum
     - Required, one of: LOW, MED, HIGH
   * - **confidence**
     - float
     - Range: 0-1 (0-100%)
   * - **location_lat**
     - float
     - Range: -90.0 to 90.0
   * - **location_lng**
     - float
     - Range: -180.0 to 180.0
   * - **uptime_percentage**
     - float
     - Range: 0-100
   * - **created_at**
     - ISO 8601 datetime
     - Format: ``2024-01-15T10:30:00Z``

Time Windows
============

For `/metrics?window=X`:

.. list-table::
   :widths: 15 50
   :header-rows: 1

   * - Value
     - Duration
   * - ``1h``
     - Last 1 hour
   * - ``6h``
     - Last 6 hours
   * - ``24h``
     - Last 24 hours
   * - ``7d``
     - Last 7 days

Pagination Query Parameters
===========================

.. list-table::
   :widths: 15 15 50
   :header-rows: 1

   * - Parameter
     - Type
     - Default
   * - **limit**
     - integer
     - 100 (max 1000)
   * - **offset**
     - integer
     - 0
   * - **sort_by**
     - string
     - created_at
   * - **order**
     - string
     - desc (asc|desc)

List Response Format
====================

All list endpoints return:

.. code-block:: json

   {
     "items": [...],
     "total": 1500,
     "limit": 50,
     "offset": 0
   }

Example:

.. code-block:: json

   {
     "items": [
       {"id": "incident_1", "severity": "HIGH"},
       {"id": "incident_2", "severity": "MED"}
     ],
     "total": 1500,
     "limit": 50,
     "offset": 0
   }

Status Codes
============

.. list-table::
   :widths: 15 50
   :header-rows: 1

   * - Code
     - Meaning
   * - **200 OK**
     - Successful GET/PATCH
   * - **201 Created**
     - Successful POST
   * - **204 No Content**
     - Successful DELETE
   * - **400 Bad Request**
     - Malformed request
   * - **404 Not Found**
     - Resource doesn't exist
   * - **422 Unprocessable Entity**
     - Validation failed
   * - **500 Internal Server Error**
     - Server error

Date/Time Format
================

All timestamps are ISO 8601 UTC:

.. code-block:: text

   Format: YYYY-MM-DDTHH:MM:SSZ
   Example: 2024-01-15T10:30:00Z

For queries, use:

.. code-block:: text

   GET /incidents?from=2024-01-01T00:00:00Z&to=2024-01-31T23:59:59Z

WebSocket Message Format (Phase 2)
==================================

**Alert message from server:**

.. code-block:: json

   {
     "type": "alert",
     "data": {
       "id": "alert_xyz789",
       "incident_id": "incident_abc123",
       "camera_id": "cam_001",
       "alert_type": "LOITERING",
       "severity": "MED",
       "confidence": 0.87,
       "created_at": "2024-01-15T10:30:00Z"
     }
   }

**Status message:**

.. code-block:: json

   {
     "type": "status",
     "data": {
       "camera_id": "cam_001",
       "status": "online",
       "uptime": 99.8
     }
   }

Next Steps
==========

→ See :ref:`api-examples` for practical usage examples

→ Check :ref:`api-endpoints` for endpoint details

--------

**Last Updated:** March 29, 2026
