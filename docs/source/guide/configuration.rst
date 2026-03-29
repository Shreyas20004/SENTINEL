.. _guide-configuration:

=============
Configuration
=============

Comprehensive guide to configuring SENTINEL for your deployment.

Environment Variables
=====================

SENTINEL uses a single ``.env`` file for all configuration. Copy ```.env.example```:

.. code-block:: bash

   cp .env.example .env

Database Configuration
======================

.. code-block:: bash

   # PostgreSQL connection
   DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/sentinel_prod
   
   # Database pool settings
   DB_POOL_SIZE=20              # Connection pool size
   DB_POOL_RECYCLE=3600         # Recycle connections after 1 hour
   DB_ECHO=false                # Log SQL queries (debug only)

Key parameters:

- **asyncpg**: Async Python driver (required)
- **Pool size**: 20 for production, 5 for development
- **Recycle**: Prevents stale connections (recommended 1-2 hours)

Data Retention
==============

.. code-block:: bash

   # Auto-delete raw detections after N days
   RETENTION_DETECTIONS_DAYS=7
   
   # Auto-delete alerts after N days
   RETENTION_ALERTS_DAYS=90
   
   # Auto-delete resolved incidents after N days
   RETENTION_INCIDENTS_DAYS=180
   
   # Keep metrics forever (aggregated)
   RETENTION_METRICS_DAYS=0

Redis Configuration
===================

.. code-block:: bash

   # Redis connection
   REDIS_URL=redis://localhost:6379/0
   
   # Alert cache TTL (seconds)
   REDIS_ALERT_TTL=300
   
   # Metrics cache TTL
   REDIS_METRICS_TTL=300

API Configuration
=================

.. code-block:: bash

   # Server binding
   API_HOST=0.0.0.0
   API_PORT=8000
   
   # Request timeout (seconds)
   API_REQUEST_TIMEOUT=30
   
   # Maximum request body size (MB)
   API_MAX_BODY_SIZE=100
   
   # CORS allowed origins
   CORS_ORIGINS=["http://localhost:5173", "https://sentinel.yourdomain.com"]
   
   # Enable debug mode
   DEBUG=false

AI/ML Configuration
===================

.. code-block:: bash

   # YOLOv8 model
   YOLO_MODEL_PATH=models/yolov8n.pt
   YOLO_CONFIDENCE_THRESHOLD=0.5
   YOLO_IOU_THRESHOLD=0.45
   
   # Batch processing
   YOLO_BATCH_SIZE=4
   
   # GPU acceleration
   GPU_ENABLED=true
   GPU_DEVICE_ID=0  # For multi-GPU: 0, 1, 2, etc.
   
   # Inference optimization
   USE_HALF_PRECISION=false  # FP16 (faster but less accurate)
   USE_ONNX_RUNTIME=true     # Faster than stock PyTorch

Behavioral Rules Configuration
===============================

Detection thresholds (seconds / count):

.. code-block:: bash

   # Loitering (stationary in zone)
   LOITERING_THRESHOLD=600          # 10 minutes
   LOITERING_MIN_CONFIDENCE=0.7
   
   # Crowd surge
   CROWD_SURGE_THRESHOLD=10         # Persons
   CROWD_SURGE_MIN_CONFIDENCE=0.6
   
   # Abandoned object
   ABANDONED_OBJECT_THRESHOLD=300   # 5 minutes
   
   # Perimeter breach time sensitivity
   PERIMETER_DWELL_ALLOWED=5        # Seconds before alert

Alert Scoring Configuration
===========================

Severity thresholds and weights:

.. code-block:: bash

   # Risk dial thresholds
   RISK_SCORE_LOW=45
   RISK_SCORE_MED=70
   
   # Rule weights (for ensemble scoring)
   WEIGHT_LOITERING=1.0
   WEIGHT_CROWD_SURGE=2.5
   WEIGHT_PERIMETER_BREACH=3.0
   WEIGHT_ABANDONED_OBJECT=2.0
   
   # Duplicate detection (MinHash)
   DEDUP_THRESHOLD=0.85            # 85% similarity = duplicate

Alert Deduplication
===================

.. code-block:: bash

   # Time window for duplicate suppression
   DEDUP_TIME_WINDOW=60             # seconds
   
   # Per-camera dedup
   DEDUP_SPATIAL_THRESHOLD=50       # pixels (bounding box distance)

Camera Configuration
====================

.. code-block:: bash

   # Frame capture rate
   CAMERA_FPS=25                    # Frames per second
   
   # RTSP connection timeout
   CAMERA_CONNECT_TIMEOUT=10        # seconds
   
   # Heartbeat interval
   CAMERA_HEARTBEAT_INTERVAL=30     # seconds
   
   # Offline detection threshold
   CAMERA_OFFLINE_THRESHOLD=90      # seconds

Stream Processing
=================

.. code-block:: bash

   # Frame buffer size (ring buffer)
   FRAME_BUFFER_SIZE=128
   
   # Processing workers
   NUM_WORKERS=4
   
   # Frame resize for inference
   INFERENCE_WIDTH=640
   INFERENCE_HEIGHT=480

Logging Configuration
=====================

.. code-block:: bash

   # Log level
   LOG_LEVEL=INFO                   # DEBUG | INFO | WARNING | ERROR | CRITICAL
   
   # Log file
   LOG_FILE=/var/log/sentinel/api.log
   
   # Log rotation size (MB)
   LOG_ROTATE_SIZE=100
   
   # Structured logging (JSON)
   LOG_FORMAT=json                  # json | text

Security Configuration (Phase 4)
=================================

.. code-block:: bash

   # JWT authentication
   JWT_SECRET_KEY=your-secret-key-change-me
   JWT_ALGORITHM=HS256
   JWT_EXPIRATION_HOURS=24
   
   # API key for service-to-service
   API_KEY=your-api-key-here
   
   # HTTPS/TLS
   SSL_CERTFILE=/etc/sentinel/cert.pem
   SSL_KEYFILE=/etc/sentinel/key.pem

Deployment Configuration
========================

.. code-block:: bash

   # Environment name
   ENVIRONMENT=production          # development | staging | production
   
   # Service name
   SERVICE_NAME=sentinel-api
   
   # Version
   VERSION=1.0.0

Example Production .env
======================

Complete example for production deployment:

.. code-block:: bash

   # Database
   DATABASE_URL=postgresql+asyncpg://sentinel_user:strongpassword@db.internal:5432/sentinel_prod
   DB_POOL_SIZE=50
   DB_POOL_RECYCLE=3600
   
   # Redis
   REDIS_URL=redis://redis.internal:6379/0
   REDIS_ALERT_TTL=300
   REDIS_METRICS_TTL=300
   
   # API
   API_HOST=0.0.0.0
   API_PORT=8000
   API_REQUEST_TIMEOUT=30
   CORS_ORIGINS=["https://sentinel.yourdomain.com", "https://operator.yourdomain.com"]
   DEBUG=false
   
   # AI/ML
   YOLO_MODEL_PATH=models/yolov8m.pt
   YOLO_CONFIDENCE_THRESHOLD=0.6
   YOLO_BATCH_SIZE=8
   GPU_ENABLED=true
   GPU_DEVICE_ID=0
   USE_ONNX_RUNTIME=true
   
   # Rules
   LOITERING_THRESHOLD=600
   CROWD_SURGE_THRESHOLD=10
   
   # Logging
   LOG_LEVEL=WARNING
   LOG_FILE=/var/log/sentinel/api.log
   
   # Security
   JWT_SECRET_KEY=your-very-long-random-secret-key-here
   API_KEY=your-api-key-here
   SSL_CERTFILE=/etc/sentinel/cert.pem
   SSL_KEYFILE=/etc/sentinel/key.pem
   
   # Deployment
   ENVIRONMENT=production
   SERVICE_NAME=sentinel-api-prod
   VERSION=1.0.0

Configuration via ConfigMap (Kubernetes)
=========================================

For Kubernetes deployments (Phase 4):

.. code-block:: yaml

   apiVersion: v1
   kind: ConfigMap
   metadata:
     name: sentinel-config
   data:
     YOLO_CONFIDENCE_THRESHOLD: "0.6"
     LOITERING_THRESHOLD: "600"
     CROWD_SURGE_THRESHOLD: "10"
     LOG_LEVEL: "INFO"

Next Steps
==========

→ Continue to :ref:`guide-usage` to start operating SENTINEL

--------

**Last Updated:** March 29, 2026
