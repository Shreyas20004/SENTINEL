.. _resources-compliance:

===========
Compliance
===========

Legal, regulatory, and compliance guidelines.

Indian Legal Framework
======================

**IT Act 2000**
   - Primary law governing information security
   - Makes unauthorized access to computer systems illegal
   - SENTINEL complies: No hacking, no unauthorized data access

**PDPB 2023 (Personal Data Protection Bill)**

   Focus areas relevant to SENTINEL:

   1. **Data Collection**
      - SENTINEL collects only behavioral metadata
      - Not personal identification
      - No facial templates, names, or personal identifiers

   2. **Data Processing**
      - Must have lawful purpose (public safety)
      - Must be transparent to operators
      - Must not discriminate

   3. **Data Minimization**
      - Collect only what's needed
      - SENTINEL: Collects bounding boxes + track IDs, nothing more
      - Automatically purges after 7 days

   4. **Consent (if applicable)**
      - Public can't be asked "do you consent to CCTV"
      - But CCTV operators need informed consent
      - Phase 3 adds operator consent UI

   5. **Data Breach Notification**
      - Must inform individuals if personal data breached
      - SENTINEL: No personal data, so simpler compliance
      - Phase 4: Implement audit trail for transparency

**NDMA (National Disaster Management Act) 2005**
   - Requires citizen info during disasters
   - SENTINEL SOS panel provides this
   - Integrates with NDMA hotlines (Phase 3)

**NCRB (National Crime Records Bureau) Guidelines**
   - Defines incident classification standards
   - SENTINEL incident types aligned with NCRB
   - Supports law enforcement workflows

Data Privacy by Design
=======================

**Zero Facial Recognition**

SENTINEL explicitly does NOT:
   - Store facial images
   - Extract facial embeddings
   - Build identity profiles
   - Compare faces across cameras

Why: Violates PDPB's prohibition of profiling without consent.

**Behavioral-Only Detection**

Instead, SENTINEL detects:
   - Loitering (dwell time)
   - Crowd surges (person count)
   - Abandoned objects (stationary items)
   - Perimeter breaches (location)

No identity involved.

**Data Minimization**

.. list-table::
   :widths: 25 50
   :header-rows: 1

   * - What We Store
     - Why
   * - Bounding boxes (pixel coordinates)
     - To show location of detected behavior
   * - Track ID (per-session only)
     - To correlate frames, not identify person
   * - Dwell time (seconds)
     - To detect loitering
   * - Timestamp
     - For time-based queries
   * - Zone ID
     - For geographic context
   * - Incident type
     - For classification

What we DON'T store:
   - Face images
   - Names
   - ID card numbers
   - Phone numbers
   - License plates
   - Vehicle VINs

**Automatic Data Deletion**

.. code-block:: bash

   # In .env
   RETENTION_DETECTIONS_DAYS=7      # Raw frames auto-deleted
   RETENTION_ALERTS_DAYS=90         # Alert details auto-deleted
   RETENTION_INCIDENTS_DAYS=180     # Historical incidents
   RETENTION_LOGS_DAYS=365          # Operational logs

After retention period, data is permanently deleted from all backups.

GDPR Compliance (EU)
====================

If SENTINEL deploys to EU:

**Article 5 (Lawfulness):**
   - ✅ Lawful basis: Public safety (legitimate interest)
   - ✅ Transparent: Users informed CCTV operates with AI
   - ⚠️ Consent: May be required in some jurisdictions

**Article 6 (Lawful Basis):**
   - ✅ Legitimate interest (public safety)
   - ⚠️ Some may require explicit legal basis

**Article 9 (Special Categories):**
   - ✅ Behavioral data is NOT "special category"
   - ❌ Facial recognition IS special category (not used)

**Article 17 (Right to be Forgotten):**
   - ✅ SENTINEL auto-deletes after 7-180 days
   - ✅ Operators can manually purge

**Article 22 (Automated Decisions):**
   - ⚠️ If SENTINEL makes decisions affecting people
   - Solution: Human-in-the-loop (operator approval before action)

**Article 35 (DPIA - Data Protection Impact Assessment):**
   - Recommended annual DPIA
   - Helps identify privacy risks
   - SENTINEL minimizes risks by design

Operator Consent & Transparency
================================

**Phase 3 additions:**

Operator must acknowledge:

.. code-block:: text

   □ I have read the Privacy Policy
   □ I understand that behavior (not identity) is detected
   □ I understand data is retained X days then deleted
   □ I will use SENTINEL legally and ethically
   □ I report any concerns to privacy officer

**Signage Requirements**

Display in monitored areas:

.. code-block:: text

   "THIS AREA IS MONITORED BY AI SURVEILLANCE
   - Purpose: Public Safety
   - No facial recognition used
   - Does not identify individuals
   - Data deleted after 7 days
   - Concerns? Contact: privacy@agency.gov.in"

Incident Logging & Audit Trail
==============================

**What to log (Phase 4):**

.. code-block:: python

   {
     "timestamp": "2024-01-15T10:30:00Z",
     "action": "escalate_incident",
     "operator": "officer_123",
     "incident_id": "incident_abc123",
     "result": "success",
     "ip_address": "192.168.1.100",
     "data_involved": "incident_abc123 (behavioral data only)"
   }

**Retention:**

- Audit logs: 5 years (compliance requirement)
- Access logs: 1 year
- Error logs: 90 days

**Access control:**

- Only audit officer can view audit logs
- No data purging without record
- Tamper-evident logging (cryptographic signing)

Data Breach Response Plan
==========================

**If operational data is exposed:**

#. **Immediate (Hour 0):** Isolate affected system
#. **Assessment (Hour 1-4):** Determine scope & severity
#. **Notification (Hour 6):** Inform privacy officer & leadership
#. **Mitigation (Hour 24):** Begin fixes & patches
#. **Disclosure (Day 3):** Notify affected parties (if required)
#. **Remediation (Week 1-2):** Full incident report

**For SENTINEL specifically:**

Since data is non-personal and auto-deleted:
- Unlikely to require public notification
- Still document incident thoroughly
- Still patch vulnerabilities

Data Portability (GDPR)
=======================

**User right to export data:**

Endpoint (Phase 4):

.. code-block:: bash

   GET /export?format=json&min_date=2024-01-01&max_date=2024-01-31

Returns:

.. code-block:: json

   {
     "incidents": [...],
     "alerts": [...],
     "detections": [...]
   }

Downloadable as JSON, CSV, or PDF.

International Deployments
===========================

**United States (GDPR-free):**
- No specific federal law
- Some states (CA, VA) have privacy laws similar to GDPR
- Recommend: State privacy law compliance

**UK (UK GDPR):**
- Similar to EU GDPR
- Some differences in data transfers

**Australia (Privacy Act):**
- Australian Privacy Principles (APPs)
- Similar to GDPR principles
- Must obtain consent for overseas data transfer

**Singapore (PDPA):**
- Personal Data Protection Act
- Similar to GDPR but more lenient
- No restrictions on AI surveillance

Third-Party Integrations
=========================

**SMS Integration (Phase 3):**

When SENTINEL sends SMS via Twilio:

.. code-block:: python

   # Ensure data minimization
   message = f"Alert: {incident_type} at {zone_name}. Details: {incident_url}"
   # NOT: "Person X at location Y" (no identity)
   
   twilio_client.messages.create(
       to="+91-xxxxxxxxxx",
       from_="+1-xxx-xxxxxx",
       body=message
   )

**Data Processing Agreement (DPA) with Twilio:**
- Required before sending any data
- Ensures Twilio is GDPR/PDPB compliant
- Must be signed by both parties

**WhatsApp Integration (Phase 3):**
- Same DPA requirements
- Message templates must go through approval
- Operator consent required

Open Data Integration
======================

**NCRB Data**
- Public domain
- Aggregated (no individual names)
- Used for context only

**GADM Boundaries**
- CC-BY license (attribution required)
- Used for geographic queries
- No personal data involved

**OSM/Nominatim**
- ODbL license (open database license)
- Used for reverse geocoding
- Attribution required

**NWP (Weather)**
- Public data from IMD
- No personal data

All third-party data is: Licensed, attributed, anonymized.

Employee/Operator Training
===========================

**Required training topics:**

1. System capabilities & limitations
2. Valid use cases (public safety only)
3. Privacy implications
4. Incident response procedures
5. Legal consequences of misuse
6. How to report concerns

**Training certification:**

.. code-block:: text

   NAME: Officer Smith
   CERTIFICATION: SENTINEL Privacy & Ethics
   DATE: 2024-01-15
   EXPIRES: 2025-01-15

Recertification required annually.

Incident Response Procedures
=============================

**On detection of suspicious operator activity:**

#. Disable operator access immediately
#. Audit all actions by that operator (past 90 days)
#. Report to Privacy Officer
#. Determine if data breach occurred
#. Notify affected parties (if required)
#. Legal proceedings (if criminal)

**Acceptable use cases:**

✅ Law enforcement investigating crime
✅ Security responding to urgent threats
✅ Emergency services during disaster
✅ System maintenance & testing

**Unacceptable use cases:**

❌ Tracking political opponents
❌ Stalking ex-partners
❌ Profiling by religion/caste/gender
❌ Commercial surveillance not authorized
❌ Any discriminatory purpose

Compliance Checklist (For Deployment)
======================================

.. list-table::
   :widths: 40 20
   :header-rows: 1

   * - Requirement
     - Status
   * - No facial recognition enabled
     - ✅
   * - Data retention set to auto-delete
     - ✅ (env var)
   * - Audit trail implemented
     - ⏳ Phase 4
   * - Operator consent obtained
     - ⏳ Phase 3
   * - Privacy policy published
     - ⏳ Phase 3
   * - Signage posted
     - ⏳ Deployment
   * - Training completed
     - ⏳ Deployment
   * - Data Processing Agreement signed
     - ⏳ (if using SMS/cloud)
   * - DPIA conducted
     - ⏳ Annual

Privacy Policy Template
=======================

**For publication (Phase 3):**

.. code-block:: text

   SENTINEL PRIVACY POLICY
   
   1. What data do we collect?
      - Behavioral metadata only (no identification)
      - Bounding boxes, dwell times, incident types
   
   2. How is data used?
      - Public safety and emergency response
      - No commercial use
      - No profiling
   
   3. How long is data kept?
      - Detection frames: 7 days
      - Alerts: 90 days
      - Incidents: 180 days
      Then automatically deleted.
   
   4. Who has access?
      - Authorized law enforcement only
      - Audit trail maintained
   
   5. Your rights
      - Right to know if your behavior was flagged
      - Right to correct false incident records
      - Right to lodge complaints
   
   6. Questions?
      privacy@sentinel-project.org

Legal Advisory
==============

**Disclaimer:**

SENTINEL is provided AS-IS. While designed with privacy principles, deployment must comply with local laws.

Consult local privacy officer / legal counsel before deployment:

- India: Privacy Officer qualified under PDPB
- EU: Data Protection Officer (DPO)
- US: Privacy director
- Australia: Complaints officer

Each jurisdiction has different requirements.

Resources
===========

- `PDPB 2023 Text <https://www.meity.gov.in/>`_
- `GDPR Text <https://gdpr-info.eu/>`_
- `India's IT Act 2000 <https://www.meity.gov.in/>`_
- `Privacy International <https://privacyinternational.org/>`_

Next Steps
==========

→ Before deployment, consult local privacy officer

--------

**Last Updated:** March 29, 2026

**Disclaimer:** This doc is informational only, not legal advice. Consult lawyers for deployment.
