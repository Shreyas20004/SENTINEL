# SENTINEL Testing Guide

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx pytest-cov
```

### Run All Tests

```bash
cd backend
pytest tests/
```

### Run With Coverage

```bash
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

### Run Specific Test File

```bash
# Test APIs
pytest tests/test_api.py -v

# Test models
pytest tests/test_models.py -v
```

### Run Specific Test

```bash
pytest tests/test_api.py::TestIncidentsAPI::test_create_incident -v
```

### Run Only Unit Tests

```bash
pytest -m unit tests/
```

### Run Only Integration Tests

```bash
pytest -m integration tests/
```

## Test Structure

### Test Files

- `test_api.py` - REST API endpoint tests
- `test_models.py` - Database model tests  
- `conftest.py` - Shared fixtures and configuration

### Test Categories

1. **Unit Tests** - Test individual components
   - API endpoints
   - Data validation
   - Business logic

2. **Integration Tests** - Test component interactions
   - Database operations
   - Redis pub/sub
   - WebSocket connections

## Coverage Goals

- **Phase 1:** >80% coverage
- **Phase 2:** >85% coverage
- **Phase 3:** >90% coverage

Current coverage can be viewed in `htmlcov/index.html` after running tests with coverage.

## Test Database

Tests use a separate PostgreSQL database configured in `conftest.py`:

```
DATABASE_URL = postgresql+asyncpg://test:test@localhost/sentinel_test
REDIS_URL = redis://localhost:6379/1
```

### Setup Test Database

```bash
# Create test database
psql -U postgres -c "CREATE DATABASE sentinel_test;"
psql -U postgres -c "CREATE USER test WITH PASSWORD 'test';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE sentinel_test TO test;"
```

## Continuous Integration

Tests run automatically on:
- Push to `main` branch
- Pull requests
- Manual trigger via GitHub Actions

See `.github/workflows/tests.yml` for CI configuration.

## Common Issues

### Test Database Connection Error

```
FAILED - could not connect to sentinel_test database
```

**Solution:** Ensure test database exists and PostgreSQL is running.

```bash
psql -l | grep sentinel_test
```

### Redis Connection Error

```
FAILED - could not connect to Redis at localhost:6379/1
```

**Solution:** Start Redis server.

```bash
redis-server
```

### Async Test Errors

```
RuntimeError: Event loop is closed
```

**Solution:** Use `pytest-asyncio` with correct `asyncio_mode`.

Current config: `asyncio_mode = auto` in `pytest.ini`

## Writing New Tests

### Template

```python
class TestNewFeature:
    """Test new feature"""
    
    @pytest.mark.asyncio
    async def test_feature_works(self, async_client):
        """Test that feature works"""
        response = await async_client.post(
            "/api/v1/endpoint",
            json={"key": "value"}
        )
        assert response.status_code == 201
        assert response.json()["id"] is not None
```

### Best Practices

1. ✅ Test one thing per test
2. ✅ Use descriptive names: `test_<thing>_<action>_<result>`
3. ✅ Use fixtures for common setup
4. ✅ Mark async tests with `@pytest.mark.asyncio`
5. ✅ Test both success and error cases
6. ✅ Use `assert` statements, not print statements

### Example Test

```python
@pytest.mark.asyncio
async def test_create_incident_with_high_severity(self, async_client, sample_incident_data):
    """Test creating HIGH severity incident"""
    payload = {**sample_incident_data, "severity": "HIGH"}
    
    response = await async_client.post("/api/v1/incidents", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["severity"] == "HIGH"
    assert data["status"] == "OPEN"
```

## Phase 1 Test Coverage

### Covered

✅ Incidents CRUD - create, read, update, list
✅ Alerts creation and fetching
✅ Metrics calculation (risk dial)
✅ Cameras management
✅ Zones management
✅ Health check endpoint
✅ WebSocket health status
✅ Error handling (400, 404, 422)

### To Cover (Phase 2+)

⏳ YOLOv8 inference latency
⏳ OpenCV frame capture
⏳ WebSocket message flow
⏳ Redis pub/sub broadcasting
⏳ ByteTrack tracking
⏳ Behavioral rules engine
⏳ Alert scoring

## Debugging Tests

### View Test Output

```bash
pytest tests/test_api.py -v -s
```

The `-s` flag shows print statements and logging output.

### Drop into Debugger

```python
import pdb; pdb.set_trace()
```

Or use pytest's built-in debugger:

```bash
pytest --pdb tests/test_api.py::TestIncidentsAPI::test_create_incident
```

### View SQL Queries

Set `echo=True` in SQLAlchemy engine creation:

```python
engine = create_async_engine(DATABASE_URL, echo=True)
```

---

**Happy Testing!** For questions, see `docs/source/developer/testing.rst`
