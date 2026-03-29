.. _guide-deployment:

==========
Deployment
==========

Production deployment guide for SENTINEL.

Pre-Deployment Checklist
=========================

**Infrastructure:**

- [ ] Server has 8+ cores, 32GB RAM, 500GB SSD (or equivalent cloud instance)
- [ ] GPU available (NVIDIA T4 or better)
- [ ] Network: 10Gbps for camera ingestion
- [ ] Static IP address assigned
- [ ] Firewall rules: Allow 8000 (API), 5173 (Frontend), 5432 (DB), 6379 (Redis)
- [ ] SSL/TLS certificates obtained (Phase 4)
- [ ] Backup storage configured

**Software:**

- [ ] Docker 20.10+ installed
- [ ] Docker Compose 2.0+ installed
- [ ] Python 3.11 available
- [ ] Node.js 20+ available

**Operational:**

- [ ] Operator training completed
- [ ] SOS phone numbers verified (112, 100, 181, 1098, etc.)
- [ ] Incident response procedures documented
- [ ] On-call support scheduled

Deployment Methods
===================

**Method 1: Docker Compose (For single server)**

Recommended for Phase 1-2 (up to 25 cameras)

#. Clone repository:

.. code-block:: bash

   git clone https://github.com/yourorg/sentinel.git
   cd SENTINEL

#. Create production `.env`:

.. code-block:: bash

   cp .env.example .env.prod
   # Edit with production values

#. Build and start:

.. code-block:: bash

   docker-compose -f docker-compose.prod.yml build
   docker-compose -f docker-compose.prod.yml up -d

#. Verify:

.. code-block:: bash

   curl http://localhost:8000/health

**Method 2: Kubernetes (For multi-server cluster)**

Recommended for Phase 3+ (50+ cameras)

#. Install Helm:

.. code-block:: bash

   curl https://get.helm.sh/helm-v3.13.0-linux-amd64.tar.gz | tar xz
   sudo mv linux-amd64/helm /usr/local/bin/

#. Add SENTINEL Helm repo:

.. code-block:: bash

   helm repo add sentinel https://charts.sentinel-project.org
   helm repo update

#. Create values file:

.. code-block:: yaml

   # values-prod.yaml
   image:
     tag: 1.0.0
   
   replicas:
     backend: 3
     frontend: 2
   
   resources:
     backend:
       requests:
         memory: "8Gi"
         cpu: "4"
       limits:
         memory: "16Gi"
         cpu: "8"
   
   database:
     host: postgres.internal
     pool_size: 50
   
   redis:
     host: redis.internal

#. Deploy:

.. code-block:: bash

   helm install sentinel sentinel/sentinel \
     -f values-prod.yaml \
     --namespace sentinel \
     --create-namespace

Database Backup Strategy
=======================

**Automated Backups:**

.. code-block:: bash

   # Daily backup script (backup.sh)
   #!/bin/bash
   
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   BACKUP_FILE="sentinel_backup_$TIMESTAMP.sql"
   
   docker-compose exec -T postgres pg_dump -U postgres sentinel > $BACKUP_FILE
   
   # Compress
   gzip $BACKUP_FILE
   
   # Upload to S3
   aws s3 cp $BACKUP_FILE.gz s3://my-bucket/backups/

Schedule with cron:

.. code-block:: bash

   0 2 * * * /home/sentinel/backup.sh  # Daily at 2am

**Retention Policy:**

- Daily backups: 7 days
- Weekly backups: 4 weeks
- Monthly backups: 12 months
- Archival: S3 Glacier

Monitoring & Alerting
=====================

**Key Metrics to Monitor:**

.. list-table::
   :widths: 25 40
   :header-rows: 1

   * - Metric
     - Alert Threshold
   * - CPU Usage
     - > 80% for 5 min
   * - Memory Usage
     - > 85%
   * - Disk Usage
     - > 90%
   * - API Response Time
     - > 1 second
   * - Database Connections
     - > 80% of pool
   * - Inference Latency
     - > 100ms
   * - WebSocket Connections
     - > 1000 (scale up)

**Prometheus Metrics (Phase 4):**

.. code-block:: bash

   # Expose metrics at /metrics
   curl http://localhost:8000/metrics | head -20

**Set up Grafana Dashboard:**

1. Add Prometheus data source
2. Import SENTINEL dashboard template
3. Configure alerting rules

Log Aggregation
================

**Centralized Logging:**

Using ELK Stack (Elasticsearch, Logstash, Kibana):

.. code-block:: yaml

   # docker-compose.prod.yml additions
   elasticsearch:
     image: docker.elastic.co/elasticsearch/elasticsearch:8.0.0
     environment:
       - discovery.type=single-node

   logstash:
     image: docker.elastic.co/logstash/logstash:8.0.0
     volumes:
       - ./logstash.conf:/usr/share/logstash/pipeline/logstash.conf

   kibana:
     image: docker.elastic.co/kibana/kibana:8.0.0
     ports:
       - "5601:5601"

Configure FastAPI to send structur logs:

.. code-block:: python

   import json
   import logging
   
   # JSON structured logging
   logging.basicConfig(format='%(message)s')
   logger = logging.getLogger(__name__)
   
   @app.post("/incidents")
   async def create_incident(...):
     logger.info(json.dumps({
       'action': 'create_incident',
       'zone_id': zone_id,
       'severity': severity,
       'timestamp': datetime.utcnow().isoformat()
     }))

Rolling Updates
================

**Updating SENTINEL without downtime:**

.. code-block:: bash

   # 1. Build new image
   docker build -t sentinel:1.0.1 backend/

   # 2. Push to registry
   docker push myregistry.azurecr.io/sentinel:1.0.1

   # 3. Update Kubernetes deployment
   kubectl set image deployment/sentinel-backend \
     sentinel=myregistry.azurecr.io/sentinel:1.0.1

   # 4. Monitor rollout
   kubectl rollout status deployment/sentinel-backend

   # 5. Rollback if needed
   kubectl rollout undo deployment/sentinel-backend

Health Checks
=============

**API Health Endpoint:**

.. code-block:: bash

   GET /health
   
   Response:
   {
     "status": "healthy",
     "version": "1.0.0",
     "uptime_seconds": 86400,
     "database": "connected",
     "redis": "connected",
     "gpu": "available"
   }

**Configure in Kubernetes:**

.. code-block:: yaml

   livenessProbe:
     httpGet:
       path: /health
       port: 8000
     initialDelaySeconds: 30
     periodSeconds: 10
   
   readinessProbe:
     httpGet:
       path: /health
       port: 8000
     initialDelaySeconds: 5
     periodSeconds: 5

Security Configuration (Phase 4)
================================

**HTTPS/TLS Setup:**

.. code-block:: bash

   # Obtain certificate (Let's Encrypt)
   sudo certbot certonly --standalone -d sentinel.yourdomain.com

   # Update nginx config
   # ... ssl_certificate, ssl_certificate_key

**API Authentication:**

.. code-block:: python

   # In .env
   JWT_SECRET_KEY=your-very-long-random-secret
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24

**Database Access Control:**

.. code-block:: sql

   -- Create readonly user
   CREATE USER sentinel_readonly WITH PASSWORD 'password';
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO sentinel_readonly;

Scaling Strategies
===================

**Vertical Scaling (bigger machine):**

1. Increase CPU cores (2 → 4 → 8)
2. Increase RAM (32GB → 64GB → 128GB)
3. Use faster GPU (T4 → A100)
4. Requires downtime

**Horizontal Scaling (more machines):**

1. Add inference workers (Celery)
2. Add API replicas (load balance)
3. Add cache replicas (Redis cluster)
4. No downtime during scaling

**Recommended approach:**

- Phase 1: Vertical (single machine sufficient for 10 cameras)
- Phase 2: Mix (add GPU, stay single machine for 25 cameras)
- Phase 3: Horizontal (Kubernetes for 50+ cameras)
- Phase 4: Distributed (geo-deployed clusters)

Cost Optimization
===================

**GCP Example:**

.. list-table::
   :widths: 25 15 15
   :header-rows: 1

   * - Component
     - Spec
     - Cost/month
   * - **Compute**
     - n1-standard-8 VM
     - $300
   * - **GPU**
     - 1 × T4 GPU
     - $100
   * - **Storage**
     - 500GB SSD
     - $50
   * - **Egress**
     - 1TB bandwidth
     - $100
   * - **Total**
     - 
     - **$550/month**

**Cost reduction tips:**

- Use preemptible/spot instances (30-70% discount)
- Downscale during off-peak hours
- Use local SSD for frame buffer
- Archive old data to cold storage

Disaster Recovery
==================

**RTO (Recovery Time Objective):** < 1 hour

**RPO (Recovery Point Objective):** < 5 minutes

**Procedures:**

#. **Database Failure:**
   - Restore from latest backup
   - Verify data integrity
   - Known data loss: < 5 minutes

#. **Disk Failure:**
   - Boot from alternate disk
   - Mount backup storage
   - Restore database

#. **Network Outage:**
   - System continues local analysis
   - Alerts queued in Redis
   - Resume publishing when network restored

#. **Complete System Failure:**
   - Spin up new VM from image
   - Restore database backup
   - Restore configuration
   - ETA: 30-45 minutes

Compliance & Audit
==================

**Audit Logging (Phase 4):**

Log all sensitive operations:

.. code-block:: json

   {
     "timestamp": "2024-01-15T10:30:00Z",
     "user": "operator_123",
     "action": "escalate_incident",
     "resource": "incident_abc123",
     "result": "success",
     "ip_address": "192.168.1.100"
   }

**Data Retention:**

Managed via `.env`:

.. code-block:: bash

   RETENTION_DETECTIONS_DAYS=7
   RETENTION_ALERTS_DAYS=90
   RETENTION_INCIDENTS_DAYS=180
   RETENTION_LOGS_DAYS=365
   RETENTION_AUDIT_DAYS=1825  # 5 years (compliance)

**Access Control:**

- Operators: Read/write incidents
- Admins: Configure system, view logs
- Service accounts: API access only

Post-Deployment
================

**Day 1:**

- [ ] Verify all services healthy
- [ ] Test incident creation
- [ ] Monitor resource usage

**Week 1:**

- [ ] Operator training
- [ ] Integration testing
- [ ] Backup verification
- [ ] Performance baseline

**Month 1:**

- [ ] Monitor stability
- [ ] Tune thresholds
- [ ] Collect feedback for Phase 2

Next Steps
==========

→ Return to :ref:`guide-usage` for operational procedures

→ See :ref:`resources-troubleshooting` if you encounter deployment issues

--------

**Last Updated:** March 29, 2026
