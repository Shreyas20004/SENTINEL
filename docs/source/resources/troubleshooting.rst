.. _resources-troubleshooting:

====================
Troubleshooting
====================

Common issues and solutions.

Backend Issues
==============

**PostgreSQL connection refused**

Error: ``psycopg2.OperationalError: could not connect to server``

Solution:

.. code-block:: bash

   # Check if postgres container is running
   docker-compose ps postgres
   
   # Check logs
   docker-compose logs postgres
   
   # Restart postgres
   docker-compose down postgres
   docker-compose up -d postgres
   
   # Verify connection
   psql postgresql://postgres:postgres@localhost:5432/sentinel

**Database migration error**

Error: ``alembic.util.exc.CommandError: Can't find identifier``

Solution:

.. code-block:: bash

   # Reset database
   docker-compose exec postgres dropdb sentinel_dev
   docker-compose exec postgres createdb sentinel_dev
   
   # Reinitialize
   cd backend && python -c "from app.core.database import init_db; import asyncio; asyncio.run(init_db())"

**API port already in use**

Error: ``Address already in use``

Solution:

.. code-block:: bash

   # Find process using port 8000
   lsof -i :8000
   
   # Kill it
   kill -9 <PID>
   
   # Or use different port
   API_PORT=8001 uvicorn app.main:app --reload

**Out of memory**

Error: ``MemoryError`` or ``OOMKilled``

Solution - Reduce batch sizes:

.. code-block:: bash

   # In .env
   YOLO_BATCH_SIZE=2        # Reduce from 4
   FRAME_BUFFER_SIZE=64     # Reduce from 128

Or increase RAM/add swap:

.. code-block:: bash

   # Add 4GB swap (Linux)
   sudo dd if=/dev/zero of=/swapfile bs=1M count=4096
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile

**High CPU usage**

Check what's consuming CPU:

.. code-block:: bash

   # Monitor in real-time
   docker stats backend
   
   # Profile Python
   python -m cProfile -s cumtime app/main.py

Common causes:
- YOLOv8 inference too frequent → Reduce FPS
- Batch size too large → Reduce YOLO_BATCH_SIZE
- Database queries unoptimized → Add indexes

Frontend Issues
===============

**Cannot connect to API**

Error: ``ERR_CONNECTION_REFUSED`` in browser console

Solution:

.. code-block:: bash

   # Verify backend is running
   curl http://localhost:8000/health
   
   # Check frontend environment
   cat frontend/.env.local | grep VITE_API_URL
   
   # Should be: VITE_API_URL=http://localhost:8000
   
   # Restart frontend
   cd frontend && npm run dev

**CORS error**

Error: ``Access to XMLHttpRequest blocked by CORS policy``

Solution:

Add frontend origin to backend CORS settings (`.env`):

.. code-block:: bash

   CORS_ORIGINS=["http://localhost:5173", "http://192.168.1.100:5173"]

Then restart backend:

.. code-block:: bash

   docker-compose restart backend

**Blank dashboard**

Error: Page loads but no content visible

Solution:

#. Open DevTools (F12)
#. Check Console tab for errors
#. Check Network tab - verify API calls succeed
#. Clear cache: ``Ctrl+Shift+Delete``
#. Hard reload: ``Ctrl+Shift+R``

**WebSocket connection fails**

Error: ``WebSocket is closed before the connection is established``

Solution - Phase 2 has WebSocket stub, full implementation in Phase 2:

.. code-block:: bash

   # For now, use REST polling
   setInterval(() => fetch('/api/v1/incidents'), 5000)

Database Issues
================

**Duplicate key error**

Error: ``psycopg2.IntegrityError: duplicate key value``

Solution:

.. code-block:: bash

   # Check for duplicate
   psql postgresql://postgres:postgres@localhost:5432/sentinel
   
   SELECT COUNT(*) FROM incidents WHERE id = 'incident_xyz';
   
   # Delete duplicate if needed
   DELETE FROM incidents WHERE id = 'incident_xyz' AND created_at < NOW() - INTERVAL '1 hour';

**Slow queries**

Query takes >1 second:

Solution:

.. code-block:: sql

   -- Check query plan
   EXPLAIN ANALYZE
   SELECT * FROM incidents 
   WHERE zone_id = 'zone_1' AND severity = 'HIGH'
   ORDER BY created_at DESC
   LIMIT 100;
   
   -- Should show "Seq Scan" (slow) or "Index Scan" (fast)
   -- If slow, add index:
   CREATE INDEX idx_incidents_zone_severity
   ON incidents (zone_id, severity, created_at DESC);

**Database disk full**

Error: ``disk I/O error`` or ``no space left on device``

Solution:

.. code-block:: bash

   # Check space
   df -h /var/lib/docker
   
   # Clean old data
   docker system prune -a
   
   # Or enable data retention in .env
   RETENTION_DETECTIONS_DAYS=3    # Keep only 3 days
   RETENTION_ALERTS_DAYS=30

**Transaction deadlock**

Error: ``deadlock detected``

Solution - Usually resolves itself. If persistent:

.. code-block:: bash

   # Reduce concurrent connections
   DB_POOL_SIZE=20  # Reduce from 50
   
   # Increase transaction timeout
   DB_STATEMENT_TIMEOUT=60000  # milliseconds

Docker Issues
==============

**Container won't start**

Check logs:

.. code-block:: bash

   docker-compose logs -f <service-name>

Examples:

**Backend won't start:**

.. code-block:: bash

   docker-compose logs -f backend
   # Common: "ModuleNotFoundError: No module named 'fastapi'"
   # Solution: npm rebuild backend/requirements.txt

**Postgres won't start:**

.. code-block:: bash

   docker-compose logs -f postgres
   # Common: "FATAL: could not create semaphores"
   # Solution: Increase VM.max_map_count
   sudo sysctl -w vm.max_map_count=262144

**All containers exiting**

Restart with clean state:

.. code-block:: bash

   docker-compose down -v        # Delete volumes
   docker-compose up --build     # Rebuild images

**Permissions denied**

Error: ``permission denied while trying to connect to Docker daemon``

Solution:

.. code-block:: bash

   sudo usermod -aG docker $USER
   newgrp docker
   docker ps  # Verify

Performance Issues
===================

**Inference too slow (>100ms)**

Cause: CPU inference or large model

Solution:

#. Use GPU:

.. code-block:: bash

   GPU_ENABLED=true
   # Should reduce to <20ms

#. Use smaller model:

.. code-block:: bash

   YOLO_MODEL_PATH=models/yolov8n.pt  # nano (15ms)
   # vs
   YOLO_MODEL_PATH=models/yolov8m.pt  # medium (50ms)

#. Use quantization:

.. code-block:: bash

   USE_ONNX_RUNTIME=true
   USE_HALF_PRECISION=true  # INT8 quantization

**Dashboard updates lag**

Cause: Inefficient polling interval

Solution:

Update polling in `frontend/src/components/ThreatQueue.tsx`:

.. code-block:: bash

   POLLING_INTERVAL=5000  # Increase from 2000
   API_BATCH_SIZE=50      # Get more in one request

**Redis connection timeout**

Error: ``redis.exceptions.ConnectionError: Connection refused``

Solution:

.. code-block:: bash

   # Check redis is running
   docker-compose ps redis
   
   # Check logs
   docker-compose logs redis
   
   # Verify port
   redis-cli ping

Network Issues
==============

**Camera can't connect**

Error: RTSP stream unreachable

Solution:

.. code-block:: bash

   # Test RTSP URL
   ffprobe rtsp://192.168.1.100:554/stream
   
   # Check connectivity
   ping 192.168.1.100
   
   # Check firewall
   telnet 192.168.1.100 554
   
   # Verify auth (if needed)
   # RTSP URL format: rtsp://user:password@ip:port/stream

**Latency too high**

Solution:

#. Reduce stream resolution (720p vs 1080p)
#. Reduce FPS (15 vs 25): ``CAMERA_FPS=15``
#. Use UDP instead of TCP (Phase 4)
#. Deploy closer to cameras (Phase 3)

**Packet loss**

Check stream quality:

.. code-block:: bash

   # Monitor stream
   ffmpeg -rtsp_transport tcp -i rtsp://camera/stream -f null - 2>&1 | grep -i "dropped\|lost"

Solutions:

#. Switch to TCP: ``RTSP_TRANSPORT=tcp``
#. Increase buffer: ``FRAME_BUFFER_SIZE=256``
#. Upgrade network to 10Gbps

Monitoring & Logging
====================

**Enable debug logging:**

.. code-block:: bash

   # In .env
   LOG_LEVEL=DEBUG
   DEBUG=true
   
   # Restart backend
   docker-compose restart backend

**View logs in real-time:**

.. code-block:: bash

   docker-compose logs -f backend

**Search logs for errors:**

.. code-block:: bash

   docker-compose logs backend | grep ERROR

**Export logs for analysis:**

.. code-block:: bash

   docker-compose logs backend > api.log

Testing Diagnosis
==================

**API endpoint test:**

.. code-block:: bash

   # Test health
   curl http://localhost:8000/health
   
   # Test incidents
   curl http://localhost:8000/api/v1/incidents | jq '.'
   
   # Test with verbose output
   curl -v http://localhost:8000/health

**Database test:**

.. code-block:: bash

   psql postgresql://postgres:postgres@localhost:5432/sentinel \
     -c "SELECT COUNT(*) FROM incidents;"

**Redis test:**

.. code-block:: bash

   redis-cli

**Full system health check:**

.. code-block:: bash

   bash backend/test_api.sh

Support Resources
==================

**GitHub Issues:** https://github.com/yourorg/sentinel/issues

**Email:** support@sentinel-project.org

**Documentation:** https://sentinel.readthedocs.io

**Stack Overflow:** Tag: ``sentinel-ai``

Getting Help
=============

When reporting issues, include:

1. Error message (exact text)
2. Steps to reproduce
3. Expected vs actual behavior
4. Environment details:

.. code-block:: bash

   docker --version
   docker-compose --version
   python --version
   node --version
   
   # Docker resource usage
   docker stats --no-stream

5. Relevant logs (``docker-compose logs``)

--------

**Last Updated:** March 29, 2026

**Couldn't find your issue?** Create a GitHub issue with above details.
