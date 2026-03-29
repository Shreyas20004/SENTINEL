.. _api-endpoints:

=================
API Endpoints
=================

Complete reference for all SENTINEL REST API endpoints.

Base URL
========

.. code-block:: text

    http://localhost:8000/api/v1

Authentication
==============

**Phase 1:** No authentication required

**Phase 4:** JWT Bearer tokens

.. code-block:: bash

    Authorization: Bearer <jwt_token>

Incident Endpoints
===================

Create Incident
---------------

.. http:post:: /incidents

   Create a new incident.

   **Request:**

   .. code-block:: json

      {
        "zone_id": "zone_1",
        "incident_type": "PERIMETER_BREACH",
        "severity": "HIGH",
        "description": "Unauthorized entry at main gate",
        "location_lat": 28.6139,
        "location_lng": 77.2090
      }

   **Response:** ``201 Created``

   .. code-block:: json

      {
        "id": "incident_abc123def456",
        "zone_id": "zone_1",
        "incident_type": "PERIMETER_BREACH",
        "severity": "HIGH",
        "status": "OPEN",
        "description": "Unauthorized entry at main gate",
        "location_lat": 28.6139,
        "location_lng": 77.2090,
        "alert_count": 0,
        "detected_at": "2024-01-15T10:30:00Z",
        "created_at": "2024-01-15T10:30:00Z"
      }

List Incidents
--------------

.. http:get:: /incidents

   List incidents with optional filtering.

   **Query Parameters:**

   - ``region`` (string, optional): Filter by zone ID
   - ``severity`` (string, optional): ``LOW``, ``MED``, ``HIGH``
   - ``status`` (string, optional): ``OPEN``, ``INVESTIGATING``, ``RESOLVED``, ``FALSE_ALARM``
   - ``limit`` (integer, optional, default=100, max=1000): Results per page
   - ``offset`` (integer, optional, default=0): Pagination offset

   **Example:**

   .. code-block:: bash

      GET /incidents?region=zone_1&severity=HIGH&limit=50

   **Response:** ``200 OK``

   .. code-block:: json

      [
        {
          "id": "incident_abc123def456",
          "zone_id": "zone_1",
          "incident_type": "LOITERING",
          "severity": "MED",
          "status": "OPEN",
          "alert_count": 2,
          "detected_at": "2024-01-15T10:30:00Z"
        }
      ]

Get Incident
------------

.. http:get:: /incidents/{incident_id}

   Retrieve a specific incident with all alerts.

   **Response:** ``200 OK``

   .. code-block:: json

      {
        "id": "incident_abc123def456",
        "zone_id": "zone_1",
        "incident_type": "LOITERING",
        "severity": "MED",
        "status": "OPEN",
        "description": "Person loitering 15+ minutes",
        "alert_count": 3,
        "detected_at": "2024-01-15T10:30:00Z",
        "created_at": "2024-01-15T10:30:00Z"
      }

Update Incident
---------------

.. http:patch:: /incidents/{incident_id}

   Update an incident status or details.

   **Request:**

   .. code-block:: json

      {
        "status": "RESOLVED",
        "severity": "LOW",
        "false_positive": false
      }

   **Response:** ``200 OK``

Alert Endpoints
================

Create Alert
------------

.. http:post:: /alerts

   Ingest alert from inference engine.

   **Note:** This endpoint is called by the AI inference pipeline, not typically by external users.

   **Request:**

   .. code-block:: json

      {
        "camera_id": "cam_001",
        "incident_id": "incident_abc123def456",
        "alert_type": "LOITERING",
        "severity": "MED",
        "confidence": 0.87,
        "bbox": {
          "x1": 100,
          "y1": 150,
          "x2": 150,
          "y2": 210
        },
        "metadata": {
          "track_id": 5,
          "dwell_time": 720,
          "history_frames": 30
        }
      }

   **Response:** ``201 Created``

   .. code-block:: json

      {
        "id": "alert_xyz789abc123",
        "incident_id": "incident_abc123def456",
        "camera_id": "cam_001",
        "alert_type": "LOITERING",
        "severity": "MED",
        "confidence": 0.87,
        "is_confirmed": false,
        "created_at": "2024-01-15T10:30:15Z"
      }

List Alerts
-----------

.. http:get:: /alerts

   List recent alerts.

   **Query Parameters:**

   - ``incident_id`` (string, optional): Filter by incident
   - ``camera_id`` (string, optional): Filter by camera
   - ``limit`` (integer, optional, default=100): Results to return
   - ``offset`` (integer, optional, default=0): Pagination offset

   **Response:** ``200 OK``

   .. code-block:: json

      [
        {
          "id": "alert_xyz789abc123",
          "incident_id": "incident_abc123def456",
          "camera_id": "cam_001",
          "alert_type": "LOITERING",
          "severity": "MED",
          "confidence": 0.87,
          "created_at": "2024-01-15T10:30:15Z"
        }
      ]

Metrics Endpoints
==================

Get System Metrics
-------------------

.. http:get:: /metrics

   Get system-wide metrics for a time window.

   **Query Parameters:**

   - ``window`` (string, optional, default=1h): Time window
     - ``1h``: Last hour
     - ``6h``: Last 6 hours
     - ``24h``: Last 24 hours
     - ``7d``: Last 7 days

   **Response:** ``200 OK``

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

Get Risk Dial
--------------

.. http:get:: /metrics/risk-dial

   Get real-time risk dial data.

   **Response:** ``200 OK``

   .. code-block:: json

      {
        "risk_score": 62,
        "severity": "MED",
        "high_count": 1,
        "med_count": 3,
        "low_count": 5
      }

Zone Endpoints
===============

List Zones
----------

.. http:get:: /zones

   List all zones with risk scores.

   **Response:** ``200 OK``

   .. code-block:: json

      [
        {
          "id": "zone_1",
          "name": "Main Gate",
          "risk_score": 50.0,
          "severity": "MED",
          "created_at": "2024-01-01T00:00:00Z"
        }
      ]

Get Zone
--------

.. http:get:: /zones/{zone_id}

   Get specific zone details.

   **Response:** ``200 OK``

   .. code-block:: json

      {
        "id": "zone_1",
        "name": "Main Gate",
        "risk_score": 50.0,
        "severity": "MED",
        "created_at": "2024-01-01T00:00:00Z"
      }

Camera Endpoints
=================

List Cameras
------------

.. http:get:: /cameras

   List cameras with optional filters.

   **Query Parameters:**

   - ``zone`` (string, optional): Filter by zone ID
   - ``active_only`` (boolean, optional, default=false): Show only active cameras

   **Response:** ``200 OK``

   .. code-block:: json

      [
        {
          "id": "cam_001",
          "name": "CAM-01",
          "zone_id": "zone_1",
          "location": "Main Gate",
          "is_active": true,
          "uptime_percentage": 99.8,
          "last_heartbeat": "2024-01-15T10:35:00Z",
          "created_at": "2024-01-01T00:00:00Z"
        }
      ]

Create Camera
-------------

.. http:post:: /cameras

   Register a new RTSP camera.

   **Request:**

   .. code-block:: json

      {
        "name": "CAM-01",
        "zone_id": "zone_1",
        "location": "Main Gate",
        "rtsp_url": "rtsp://192.168.1.100:554/stream"
      }

   **Response:** ``201 Created``

   .. code-block:: json

      {
        "id": "cam_abc123def456",
        "name": "CAM-01",
        "zone_id": "zone_1",
        "location": "Main Gate",
        "is_active": true,
        "uptime_percentage": 100.0,
        "last_heartbeat": "2024-01-15T10:00:00Z",
        "created_at": "2024-01-15T10:00:00Z"
      }

Get Camera
----------

.. http:get:: /cameras/{camera_id}

   Get specific camera details.

   **Response:** ``200 OK``

Update Camera
-------------

.. http:patch:: /cameras/{camera_id}

   Update camera configuration.

   **Request:**

   .. code-block:: json

      {
        "name": "CAM-01-MAIN",
        "is_active": true,
        "zone_id": "zone_1"
      }

   **Response:** ``200 OK``

Dispatch Endpoints
===================

Escalate Alert
---------------

.. http:post:: /dispatch/escalate

   Escalate HIGH alerts to emergency authorities.

   **Note:** Phase 3 will integrate actual SMS/WhatsApp and tel: protocol.

   **Request:**

   .. code-block:: json

      {
        "alert_ids": ["alert_001", "alert_002"],
        "unit_id": "unit_123",
        "notes": "Perimeter breach, possible intruder"
      }

   **Response:** ``200 OK``

   .. code-block:: json

      {
        "dispatch_id": "dispatch_xyz789",
        "alert_ids": ["alert_001", "alert_002"],
        "status": "DISPATCHED",
        "timestamp": "2024-01-15T10:30:00Z"
      }

Report Endpoints
=================

Generate Report
----------------

.. http:post:: /reports/generate

   Generate a signed PDF incident report.

   **Note:** Phase 4 will implement actual PDF generation.

   **Request:**

   .. code-block:: json

      {
        "from_date": "2024-01-01T00:00:00Z",
        "to_date": "2024-01-31T23:59:59Z",
        "zone_id": "zone_1"
      }

   **Response:** ``200 OK``

   .. code-block:: json

      {
        "report_id": "report_abc123",
        "download_url": "https://api.sentinel.local/reports/report_abc123/download",
        "expires_at": "2024-01-16T10:30:00Z"
      }

Health Endpoints
=================

Health Check
-------------

.. http:get:: /health

   Check API health status.

   **Response:** ``200 OK``

   .. code-block:: json

      {
        "status": "healthy",
        "version": "1.0.0",
        "service": "SENTINEL"
      }

WebSocket Endpoints (Phase 2)
==============================

Real-time Alert Stream
-----------------------

.. code-block:: text

    WS wss://api.sentinel.local/ws/alerts

**Authentication:** Bearer token in query parameter (Phase 4)

**Message Format:**

.. code-block:: json

    {
      "id": "alert_xyz789",
      "incident_id": "incident_abc123",
      "camera_id": "cam_001",
      "alert_type": "LOITERING",
      "severity": "MED",
      "confidence": 0.87,
      "created_at": "2024-01-15T10:30:00Z"
    }

Status Codes
============

.. list-table::
   :widths: 10 60
   :header-rows: 1

   * - Code
     - Meaning
   * - ``200 OK``
     - Successful request
   * - ``201 Created``
     - Resource created successfully
   * - ``204 No Content``
     - Successful request with no response body
   * - ``400 Bad Request``
     - Invalid request parameters
   * - ``401 Unauthorized``
     - Missing or invalid authentication (Phase 4)
   * - ``403 Forbidden``
     - Insufficient permissions (Phase 4)
   * - ``404 Not Found``
     - Resource not found
   * - ``422 Unprocessable Entity``
     - Validation error in request body
   * - ``500 Internal Server Error``
     - Server error
   * - ``503 Service Unavailable``
     - Service temporarily down

Error Response Format
=====================

.. code-block:: json

    {
      "detail": "Incident not found",
      "status": 404,
      "type": "NOT_FOUND"
    }

Rate Limiting (Phase 4)
=======================

**Limits:**

- 1000 requests/hour per IP
- 10000 requests/hour per API key
- WebSocket: 10 connections per user

**Response Headers:**

.. code-block:: text

    X-RateLimit-Limit: 1000
    X-RateLimit-Remaining: 999
    X-RateLimit-Reset: 1705329600

Pagination
==========

All list endpoints support pagination:

.. code-block:: bash

    GET /incidents?limit=50&offset=0

**Default:** limit=100, offset=0

**Maximum:** limit=1000

Response includes:

.. code-block:: json

    {
      "items": [...],
      "total": 1500,
      "limit": 50,
      "offset": 0
    }

Next Steps
==========

→ See :ref:`api-examples` for detailed cURL examples

→ Review :ref:`api-schemas` for request/response models

--------

**Last Updated:** March 29, 2026
