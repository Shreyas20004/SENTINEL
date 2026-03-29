.. _roadmap-phase3:

==========================
Phase 3: Investigative Tools
==========================

Multi-camera analytics and emergency integration.

Phase 3 Vision
==============

**"Multi-camera Threat Correlation with Emergency Dispatch"**

By end of Phase 3, SENTINEL:

- Correlates same person across multiple cameras
- Provides live geospatial map of threats
- One-tap emergency escalation (police, ambulance, etc.)
- SOS panel showing state emergency hotlines
- Cross-zone incident analysis
- API webhooks for third-party integration
- Audit trail for compliance

Phase 3 Objectives
===================

**High Priority:**

1. **Geospatial Visualization** (Week 1-2)
   - Leaflet.js-based threat map
   - GADM GeoJSON state/district polygons
   - Incident bubble markers (sized by count)
   - Real-time marker updates
   - Click for incident details

2. **Cross-Camera Tracking** (Week 2-3)
   - Inter-zone pedestrian correlation
   - Track_ID linkage when person crosses zones
   - Trajectory reconstruction
   - Historical path analysis

3. **Emergency Dispatch Integration** (Week 3-4)
   - SMS via Twilio
   - WhatsApp via Twilio
   - Emergency call routing (Phase 4 for voice)
   - Status tracking

4. **SOS Emergency Panel** (Week 2)
   - Police (100)
   - Fire (101)
   - Ambulance (108 / 102)
   - Women helpline (1098)
   - Blood bank (181)
   - Custom hotlines per state

5. **Audit & Compliance** (Week 4)
   - Immutable audit logs
   - Operator action tracking
   - Data access logging
   - Compliance reports

6. **API Webhooks** (Week 3)
   - Subscribe to incident.created
   - Subscribe to incident.escalated
   - Subscribe to incident.resolved
   - Custom integrations

**Secondary:**

7. **Advanced Filtering** (Week 2)
   - Date range queries
   - Multiple zone selection
   - Incident type filtering
   - False positive marking

8. **Reporting & Analytics** (Week 3-4)
   - PDF incident report generation
   - CSV export
   - Time-series analytics
   - Response time tracking

New Deployment Model
====================

- **Kubernetes deployment** becomes standard
- Helm charts for easy scaling
- Regional deployment (multiple zones)
- Service mesh for inter-region communication

Architecture Changes
====================

**Layer 3 expansion:**

- Cross-camera ByteTrack correlation
- Zone boundary detection
- Trajectory analysis engine
- Threat cascade detection

New Files (Phase 3)
====================

.. list-table::
   :widths: 35 40
   :header-rows: 1

   * - File
     - Purpose
   * - **backend/app/analytics/correlation.py**
     - Cross-camera tracking
   * - **backend/app/integrations/sms.py**
     - Twilio SMS integration
   * - **backend/app/integrations/webhooks.py**
     - Webhook dispatcher
   * - **backend/app/api/map.py**
     - Geospatial API endpoints
   * - **frontend/src/components/LiveMap.tsx**
     - Leaflet.js map component
   * - **frontend/src/components/SOSPanel.tsx**
     - Emergency hotline panel
   * - **backend/app/audit/**
     - Audit logging module

Key Features (Phase 3)
======================

**Live Geospatial Map**

.. code-block:: typescript

   // Component renders:
   // - GADM state boundaries (GeoJSON)
   // - District boundaries (GeoJSON)
   // - Incident bubble markers (colored by severity)
   // - Marker size = number of incidents in zone
   // - Click marker = incident details panel
   // - Real-time updates via WebSocket

**Cross-Camera Tracking**

When same person appears in zone_1 then zone_2:

.. code-block:: text

   Timeline:
   T=10:30 - Person detected in zone_1 (Track ID = 5)
   T=10:35 - Person detected in zone_2 (Track ID = 12)
   
   Correlation Engine:
   - Compare bounding box sizes (same person?)
   - Compare appearance features (clothing colors)
   - Compare timestamps + zone proximity
   - If high confidence: Link Track 5 → Track 12
   
   Result: Continuous trajectory across cameras

**Escalation Workflow**

.. code-block:: text

   Operator clicks "ESCALATE" on HIGH incident
       ↓
   System shows options:
   - [ ] Call Police (100)
   - [ ] Call Ambulance (108)
   - [ ] Send SMS
   - [ ] Send WhatsApp
   - [ ] Custom number
       ↓
   Operator selects option
       ↓
   System prepares message:
   "ALERT: Possible perimeter breach at Gate #1
    Zone: Main Entrance
    Time: 10:35 AM est
    Coordinates: 28.6139°N, 77.2090°E
    Camera feed: [link to live stream]"
       ↓
   Operator confirms
       ↓
   Message sent + logged in audit trail

**Webhook Integration**

.. code-block:: bash

   # Operator subscribes to events
   curl -X POST http://localhost:8000/api/v1/webhooks \
     -d '{
       "event": "incident.created",
       "url": "https://custom-system.org/webhooks/incidents"
     }'
   
   # SENTINEL POSTs whenever incident created:
   POST https://custom-system.org/webhooks/incidents
   {
     "event": "incident.created",
     "timestamp": "2024-01-15T10:30:00Z",
     "incident": {
       "id": "incident_abc123",
       "zone_id": "zone_1",
       "severity": "HIGH",
       "...": "..."
     }
   }

Testing Strategy (Phase 3)
===========================

**Geo-fencing tests:**

.. code-block:: python

   def test_cross_zone_tracking():
       # Simulate person walking from zone_1 to zone_2_
       # Assert: Same track ID or linked track IDs

**Map rendering tests:**

.. code-block:: typescript

   test('renders incident markers on map', async () => {
       // Mock Leaflet map
       // Create incidents
       // Assert markers appear
       // Assert colors match severity
   });

**SMS delivery tests:**

.. code-block:: python

   @patch('twilio.rest.Client.messages.create')
   def test_escalate_sends_sms(mock_send):
       escalate_incident(incident_id, phone_number)
       mock_send.assert_called_once()
       assert "Alert" in mock_send.call_args[0][0]

Performance Goals (Phase 3)
===========================

- Cross-camera tracking latency: < 5 minutes
- Map load time: < 2 seconds
- SMS delivery: < 30 seconds
- Webhook delivery: < 5 seconds
- Query across 50 zones: < 1 second

Deliverables (Phase 3)
======================

✅ Live geospatial map (Leaflet + GADM)

✅ Cross-camera pedestrian tracking

✅ Emergency SMS/WhatsApp integration

✅ SOS emergency hotline panel

✅ Audit logging & compliance

✅ Webhook API for custom integrations

✅ Advanced reporting & analytics

✅ Regional Kubernetes deployment

✅ Full unit tests

✅ Documentation updated

Success Criteria (Phase 3)
==========================

- [ ] Map displays all incidents with correct colors/sizes
- [ ] Cross-zone tracking accurately links same persons
- [ ] SMS sent within 30 seconds of escalation
- [ ] Webhooks deliver events reliably
- [ ] Audit logs immutable and timestamped
- [ ] System runs on Kubernetes with auto-scaling
- [ ] All unit tests passing

Challenges & Mitigations
=========================

**Challenge:** Appearance features unreliable for matching
   - Solution: Use gait recognition (how they walk)
   - Fallback: Time + distance heuristics

**Challenge:** Network latency (SMS, webhooks)
   - Solution: Queue messages in Redis
   - Retry logic with exponential backoff

**Challenge:** Geospatial queries expensive at scale
   - Solution: PostGIS spatial indexing
   - Cache zone boundaries in memory

**Challenge:** Privacy (tracking person across cameras)
   - Solution: No storage of identity
   - Only behavioral correlation
   - Auto-delete after 7 days

Next Steps
==========

→ See :ref:`roadmap-phase4` for final phase

--------

**Last Updated:** March 29, 2026
