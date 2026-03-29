.. _guide-usage:

=====
Usage
=====

Day-to-day operator guide for using SENTINEL.

Accessing the System
====================

**Web Dashboard:**

Open browser and navigate to: http://localhost:5173 (development) or https://sentinel.yourdomain.com (production)

**API Documentation (Interactive):**

Visit: http://localhost:8000/docs (Swagger UI)

Dashboard Overview
==================

The SENTINEL dashboard has 5 main sections:

.. image:: _static/dashboard-layout.png
   :alt: Dashboard layout diagram
   :align: center

**Top Navigation**
   - System status (green = healthy)
   - User profile (Phase 4)
   - Settings

**Left Sidebar**
   - Threat Queue (prioritized incidents)
   - Quick stats (active incidents, uptime)

**Center Panel**
   - Risk Dial (system threat level)
   - Zone Map (Phase 3)
   - Live metrics

**Right Panel**
   - Camera Grid (status monitors)
   - Action buttons

Threat Queue
============

The **Threat Queue** shows incidents ranked by severity and recency:

**Color Coding:**

- 🔴 **RED** (HIGH): Requires immediate action
- 🟠 **AMBER** (MED): Review and monitor
- 🟢 **GREEN** (LOW): Monitor for patterns

**Interpreting Incidents:**

Each incident shows:

- **Type**: LOITERING, CROWD_SURGE, PERIMETER_BREACH, ABANDONED_OBJECT
- **Zone**: Location (e.g., "Main Gate")
- **Duration**: How long incident ongoing (e.g., "12 min")
- **Confidence**: How certain the system is (0-100%)
- **Alert Count**: Number of frames flagged

**Example: A HIGH severity loitering at Main Gate for 12 minutes**

.. image:: _static/threat-item.png
   :alt: Threat queue item
   :align: center

Risk Dial
=========

The **Risk Dial** displays system-wide threat level:

- **Arc Position**: Current risk score (0-100)
- **Color**: RED (70-100) → AMBER (45-70) → GREEN (0-45)
- **Animation**: Updates every 2-5 minutes

**Interpreting the dial:**

- GREEN (0-45): Normal operations, routine monitoring
- AMBER (45-70): Active incidents detected, elevated alertness
- RED (70-100): Multiple HIGH incidents, immediate review required

**Risk Score Calculation:**

.. code-block:: text

   Score = (HIGH×3 + MED×1.5 + LOW×1) / total_cameras
   
   Example: 2 HIGH + 3 MED + 5 LOW across 10 cameras = (6 + 4.5 + 5)/10 = 1.55 → 80 (HIGH)

Metrics Cards
=============

Display system KPIs:

**Uptime Percentage**
   - Target: > 99% (4.3 hours downtime/month)
   - Green if > 99%, yellow if 95-99%, red if < 95%

**Average Response Time**
   - Time from detection to operator action
   - Target: < 5 minutes
   - Tracked for HIGH severity incidents only

**Active Incidents**
   - Count of open incidents
   - Cleared when marked RESOLVED

**Alerts/Hour**
   - Rate of detection
   - Increases during threat windows
   - Useful for anomaly detection

Creating Incidents
===================

Manual incident creation (for testing or non-automatic detections):

**Step 1: Click "Create Incident" button**

**Step 2: Fill form:**

.. list-table::
   :widths: 20 40
   :header-rows: 1

   * - Field
     - Example
   * - Incident Type
     - LOITERING
   * - Zone
     - Main Gate
   * - Severity
     - HIGH
   * - Description
     - Suspicious person loitering 15+ minutes
   * - Location (optional)
     - Latitude: 28.6139, Longitude: 77.2090

**Step 3: Submit**

Incident created and added to threat queue.

Responding to Incidents
=======================

**Step 1: Review incident details**

Click incident in threat queue to see:
- Full description
- All related alerts
- Timeline of events
- Camera feeds (Phase 2)

**Step 2: Validate incident (if uncertain)**

- View camera feed overlay
- Check confidence score
- Look for patterns

**Step 3: Choose action:**

**If it's a real threat (HIGH):**

1. Click **"Escalate"** button
2. Confirm escalation
3. System sends alert to authorities (Phase 3)

**If it's a false positive:**

1. Mark **"False Positive"**
2. System learns and adjusts
3. Incident closed

**If it's resolved:**

1. Click **"Mark Resolved"**
2. Incident archived
3. Included in reports

Managing Cameras
================

**Register a new camera:**

.. code-block:: bash

   curl -X POST http://localhost:8000/api/v1/cameras \
     -H "Content-Type: application/json" \
     -d '{
       "name": "CAM-01",
       "zone_id": "zone_1",
       "location": "Main Gate",
       "rtsp_url": "rtsp://192.168.1.100:554/stream"
     }'

**Monitor camera status:**

Camera grid shows:
- 🟢 Green = Online, streaming
- 🔴 Red = Offline, not responding
- 🟡 Yellow = Degraded, high latency

**Uptime percentage:**
- Green: > 99%
- Yellow: 95-99%
- Red: < 95%

**Troubleshoot offline camera:**

1. Verify RTSP URL is reachable: ``ping 192.168.1.100``
2. Check camera firmware is updated
3. Verify network firewall allows port 554
4. In dashboard, click camera → "Reconnect"

Advanced Filtering
==================

Filter incidents by criteria:

**By Zone:**

.. code-block:: bash

   GET /api/v1/incidents?region=zone_1

**By Severity:**

.. code-block:: bash

   GET /api/v1/incidents?severity=HIGH

**By Date Range (Phase 3):**

.. code-block:: bash

   GET /api/v1/incidents?from=2024-01-01&to=2024-01-31

**By Status:**

.. code-block:: bash

   GET /api/v1/incidents?status=OPEN

**Combined:**

.. code-block:: bash

   GET /api/v1/incidents?region=zone_1&severity=HIGH&status=OPEN

Exporting Data
==============

**Export incidents to CSV:**

.. code-block:: bash

   curl "http://localhost:8000/api/v1/incidents" | jq -r \
     '.[] | [.id, .severity, .status, .detected_at] | @csv' \
     > incidents.csv

**Generate PDF report (Phase 4):**

1. Click **"Generate Report"**
2. Select date range
3. Choose zones
4. Download PDF

Shift Management
================

**Handoff to next operator:**

#. Note active incidents in shift summary
#. Mark false positives
#. Update incident descriptions
#. Close resolved incidents
#. Document any escalations

**End-of-shift checklist:**

- [ ] All HIGH severity incidents escalated
- [ ] False positives marked
- [ ] Cameras all reporting healthy
- [ ] System uptime monitored
- [ ] Critical alerts logged

Phone Integration (Phase 3)
===========================

**Emergency escalation (one-tap):**

Click "Escalate" on HIGH incident:

.. code-block:: text

   □ Call police (100)
   □ Call emergency response (112)
   □ Call blood bank (181)
   □ Call women helpline (1098)
   □ Call disaster mgmt (NDMA - 1070)
   □ Custom number

System automatically includes:
- Incident details
- Zone coordinates
- Camera feeds (video link)
- Operator name

**Follow-up actions:**

- Track dispatch unit ETA
- Update incident with officer notes
- Confirm resolution

Keyboard Shortcuts
==================

.. list-table::
   :widths: 20 40
   :header-rows: 1

   * - Shortcut
     - Action
   * - ``R``
     - Open threat queue
   * - ``M``
     - Toggle risk dial
   * - ``C``
     - Open camera grid
   * - ``E``
     - Escalate threat
   * - ``?``
     - Show help

Settings (Phase 4)
==================

Operator preferences:

.. list-table::
   :widths: 20 40
   :header-rows: 1

   * - Setting
     - Options
   * - Theme
     - Dark (default), Light
   * - Notification Sound
     - On, Off
   * - Alert Timeout
     - 5 min, 10 min, 30 min, None
   * - Metrics Refresh
     - 10 sec, 30 sec, 1 min, 5 min

Troubleshooting Common Issues
==============================

**Incident not appearing:**

1. Check camera is online
2. Verify zone is active
3. Review YOLO confidence threshold (increase if too strict)

**False positives too high:**

Adjust in `.env`:

.. code-block:: bash

   YOLO_CONFIDENCE_THRESHOLD=0.7  # Increase threshold
   DEDUP_THRESHOLD=0.80            # Increase dedup similarity

**Camera offline:**

.. code-block:: bash

   # Verify RTSP stream
   ffprobe rtsp://192.168.1.100:554/stream

   # Check network
   ping 192.168.1.100
   telnet 192.168.1.100 554

**Escalation not sending:**

1. Verify phone numbers configured
2. Check SMS credit (Phase 3)
3. Review audit logs

Performance Tips
================

**For high incident volume:**

- Increase zone count (split large areas)
- Reduce ``FRAME_BUFFER_SIZE`` in config
- Enable GPU acceleration
- Use lower resolution streams (720p, not 1080p)

**For better accuracy:**

- Increase ``YOLO_MODEL_PATH`` from nano to small/medium
- Increase ``YOLO_CONFIDENCE_THRESHOLD`` to 0.7+
- Add more cameras for cross-validation

Next Steps
==========

→ See :ref:`api-examples` for programmatic access

→ Refer to :ref:`resources-troubleshooting` if you encounter issues

--------

**Last Updated:** March 29, 2026
