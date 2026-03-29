# SENTINEL Deployment & Configuration Guide

## Prerequisites

- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)
- **Docker Compose** 2.0+
- **Git**
- Optional: GPU support (NVIDIA CUDA 11.8+)

## Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-org/sentinel.git
cd sentinel
```

### 2. Configure Environment
```bash
# Copy template
cp backend/.env.example backend/.env

# Edit for your environment
nano backend/.env
```

### 3. Start Services
```bash
# Build and start all containers
docker-compose up --build -d

# View logs
docker-compose logs -f

# Verify health
curl http://localhost:8000/health
```

### 4. Initialize Database (First Run)
```bash
# Automatically runs on first startup
# Database migrations happen via SQLAlchemy
# PostGIS extension is enabled automatically
```

### 5. Access UI
Open browser: **http://localhost:5173**

---

## Docker Compose Services

### Backend (FastAPI)
- **Port:** 8000
- **Health:** GET /health
- **Docs:** GET /docs (OpenAPI)
- **Env:** `DATABASE_URL`, `REDIS_URL`

### PostgreSQL
- **Port:** 5432
- **Database:** sentinel_db
- **User:** sentinel
- **Extensions:** PostGIS enabled

### Redis
- **Port:** 6379
- **For:** Alert pub/sub, caching

### Frontend (React + Vite)
- **Port:** 5173
- **Dev Server:** Hot reload enabled
- **Build:** `npm run build`

---

## Development Workflow

### Backend Development
```bash
# Start just backend
docker-compose up postgres redis backend -d

# View backend logs
docker-compose logs -f backend

# Run tests
docker-compose exec backend pytest

# Format code
docker-compose exec backend black app/
docker-compose exec backend isort app/
```

### Frontend Development
```bash
# Start frontend with hot reload
docker-compose up frontend -d

# Or run locally
cd frontend
npm install
npm run dev
```

### Database Migrations
```bash
# Create migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migration
docker-compose exec backend alembic upgrade head

# Rollback
docker-compose exec backend alembic downgrade -1
```

---

## Testing

### Unit Tests
```bash
docker-compose exec backend pytest app/tests/ -v
```

### Integration Tests
```bash
docker-compose exec backend pytest app/tests/integration/ -v
```

### API Tests
```bash
# Using httpx client
docker-compose exec backend python -m pytest app/tests/test_api/ -v
```

---

## Monitoring

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f postgres
```

### Health Status
```bash
# Backend health
curl http://localhost:8000/health

# Database connection
curl http://localhost:8000/api/v1/cameras | head

# Redis connection
docker-compose exec redis redis-cli ping
```

### Metrics (Phase 4)
Prometheus + Grafana endpoints will be added in Phase 4.

---

## Troubleshooting

### Port Already in Use
```bash
# Change ports in docker-compose.yml and restart
docker-compose restart
```

### Database Connection Error
```bash
# Check PostgreSQL health
docker-compose ps postgres

# View postgres logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres

# Verify connection
docker-compose exec postgres psql -U sentinel -d sentinel_db -c "\dt"
```

### Redis Connection Error
```bash
# Check Redis health
docker-compose exec redis redis-cli ping

# Restart Redis
docker-compose restart redis
```

### Frontend Can't Connect to Backend
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS configuration in backend/.env
# CORS_ORIGINS should include http://localhost:5173
```

### Memory Issues
```bash
# Reduce memory limit in docker-compose.yml
# Or increase Docker Desktop memory allocation
```

---

## Production Deployment

### Pre-Deployment Checklist
- [ ] Change JWT_SECRET_KEY in .env
- [ ] Set DEBUG=False
- [ ] Enable SSL/TLS
- [ ] Configure production database (RDS, CloudSQL)
- [ ] Set up monitoring (Prometheus, Grafana)
- [ ] Review security headers
- [ ] Load test (25 cameras, 25 FPS)
- [ ] Compliance review (PDPB 2023)

### Kubernetes Deployment (Phase 4)
Helm charts coming in Phase 4.

### Cloud Deployment (Phase 4)
AWS ECS, GCP GKE, Azure ACS guides coming in Phase 4.

---

## Data Backup & Recovery

### Backup PostgreSQL
```bash
# Full backup
docker-compose exec postgres pg_dump -U sentinel sentinel_db > backup.sql

# With compression
docker-compose exec postgres pg_dump -U sentinel sentinel_db | gzip > backup.sql.gz
```

### Restore PostgreSQL
```bash
# From SQL file
docker-compose exec -T postgres psql -U sentinel sentinel_db < backup.sql

# From compressed file
gunzip -c backup.sql.gz | docker-compose exec -T postgres psql -U sentinel sentinel_db
```

### Volume Backups
```bash
# Backup PostgreSQL volume
docker run --rm -v sentinel_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data

# Restore PostgreSQL volume
docker run --rm -v sentinel_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /data
```

---

## Scaling

### Horizontal Scaling (Phase 4)
- Multiple backend instances behind load balancer
- Read replicas for PostgreSQL
- Redis cluster for high availability

### Vertical Scaling
```bash
# Increase container resources in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

---

## Performance Tuning

### PostgreSQL
```sql
-- Increase cache
ALTER SYSTEM SET shared_buffers = '4GB';

-- Increase work memory
ALTER SYSTEM SET work_mem = '256MB';

-- Enable parallel queries
ALTER SYSTEM SET max_parallel_workers_per_gather = 4;

-- Restart PostgreSQL
SELECT pg_reload_conf();
```

### Redis
```bash
# Increase maxmemory policy
docker-compose exec redis redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

---

## Cleanup

### Remove All Containers
```bash
docker-compose down
```

### Remove Volumes (⚠️ DATA LOSS)
```bash
docker-compose down -v
```

### Remove Everything
```bash
docker-compose down -v --rmi all
```

---

## Support

- **Issues:** GitHub Issues
- **Documentation:** See README.md
- **Development:** See DEVELOPMENT.md

---

**Last Updated:** March 29, 2026
