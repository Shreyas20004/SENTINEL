"""
Unit Tests for SENTINEL Phase 1 APIs
"""

import pytest
import json
from datetime import datetime
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.core.database import AsyncSession as DBSession
from app.schemas import IncidentCreate, AlertCreate, CameraCreate, ZoneCreate
from app.models import Incident, Alert, Camera, Zone


@pytest.fixture
async def client():
    """Test client"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def db_session():
    """Database session for testing"""
    # In real tests, this would use a test database
    # For now, we mock it
    pass


class TestIncidentsAPI:
    """Test Incidents endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_incidents_empty(self, client):
        """Test GET /incidents when empty"""
        response = await client.get("/api/v1/incidents")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert isinstance(data["items"], list)
    
    @pytest.mark.asyncio
    async def test_create_incident(self, client):
        """Test POST /incidents"""
        payload = {
            "incident_type": "LOITERING",
            "severity": "HIGH",
            "zone_id": "zone_1",
            "description": "Test incident",
            "location": {"type": "Point", "coordinates": [28.6139, 77.2090]}
        }
        response = await client.post("/api/v1/incidents", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["severity"] == "HIGH"
        assert data["status"] == "OPEN"
    
    @pytest.mark.asyncio
    async def test_filter_incidents_by_severity(self, client):
        """Test filtering incidents by severity"""
        response = await client.get("/api/v1/incidents", params={"severity": "HIGH"})
        assert response.status_code == 200
        data = response.json()
        # Items should only contain HIGH severity
        for item in data["items"]:
            assert item["severity"] == "HIGH"
    
    @pytest.mark.asyncio
    async def test_update_incident_status(self, client):
        """Test PATCH /incidents/{id}"""
        # Create incident
        create_response = await client.post(
            "/api/v1/incidents",
            json={
                "incident_type": "CROWD_SURGE",
                "severity": "MEDIUM",
                "zone_id": "zone_2",
                "description": "Test"
            }
        )
        incident_id = create_response.json()["id"]
        
        # Update status
        update_response = await client.patch(
            f"/api/v1/incidents/{incident_id}",
            json={"status": "RESOLVED"}
        )
        assert update_response.status_code == 200
        assert update_response.json()["status"] == "RESOLVED"


class TestAlertsAPI:
    """Test Alerts endpoints"""
    
    @pytest.mark.asyncio
    async def test_create_alert(self, client):
        """Test POST /alerts"""
        payload = {
            "incident_id": "incident_1",
            "camera_id": "cam_1",
            "alert_type": "MOTION",
            "severity": "MEDIUM",
            "confidence": 0.95
        }
        response = await client.post("/api/v1/alerts", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["confidence"] == 0.95
    
    @pytest.mark.asyncio
    async def test_get_alerts(self, client):
        """Test GET /alerts"""
        response = await client.get("/api/v1/alerts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["items"], list)
        assert "total" in data


class TestMetricsAPI:
    """Test Metrics endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_risk_dial(self, client):
        """Test GET /metrics/risk"""
        response = await client.get("/api/v1/metrics/risk")
        assert response.status_code == 200
        data = response.json()
        assert "risk_score" in data
        assert "severity" in data
        assert 0 <= data["risk_score"] <= 100
    
    @pytest.mark.asyncio
    async def test_get_metrics_summary(self, client):
        """Test GET /metrics"""
        response = await client.get("/api/v1/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "risk_score" in data
        assert "active_incidents" in data
        assert "uptime_percentage" in data


class TestCamerasAPI:
    """Test Cameras endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_cameras(self, client):
        """Test GET /cameras"""
        response = await client.get("/api/v1/cameras")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["items"], list)
    
    @pytest.mark.asyncio
    async def test_create_camera(self, client):
        """Test POST /cameras"""
        payload = {
            "name": "Camera 1",
            "zone_id": "zone_1",
            "rtsp_url": "rtsp://example.com/stream",
            "is_active": True
        }
        response = await client.post("/api/v1/cameras", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Camera 1"
        assert data["rtsp_url"] == "rtsp://example.com/stream"


class TestZonesAPI:
    """Test Zones endpoints"""
    
    @pytest.mark.asyncio
    async def test_get_zones(self, client):
        """Test GET /zones"""
        response = await client.get("/api/v1/zones")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["items"], list)
    
    @pytest.mark.asyncio
    async def test_create_zone(self, client):
        """Test POST /zones"""
        payload = {
            "name": "Zone A",
            "description": "Main entrance",
            "polygon": {
                "type": "Polygon",
                "coordinates": [[[77.2, 28.6], [77.3, 28.6], [77.3, 28.7], [77.2, 28.7], [77.2, 28.6]]]
            }
        }
        response = await client.post("/api/v1/zones", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Zone A"


class TestHealthEndpoint:
    """Test health check"""
    
    @pytest.mark.asyncio
    async def test_health_check(self, client):
        """Test GET /health"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestWebSocketHealth:
    """Test WebSocket health endpoint"""
    
    @pytest.mark.asyncio
    async def test_websocket_health(self, client):
        """Test GET /ws/health"""
        response = await client.get("/ws/health")
        assert response.status_code == 200
        data = response.json()
        assert "active_connections" in data
        assert "status" in data


class TestErrorHandling:
    """Test error handling"""
    
    @pytest.mark.asyncio
    async def test_invalid_incident_creation(self, client):
        """Test error on invalid data"""
        payload = {
            "incident_type": "INVALID_TYPE",
            "severity": "INVALID_SEVERITY"
        }
        response = await client.post("/api/v1/incidents", json=payload)
        # Should return 422 Unprocessable Entity or similar
        assert response.status_code in [400, 422]
    
    @pytest.mark.asyncio
    async def test_not_found(self, client):
        """Test 404 on nonexistent resource"""
        response = await client.get("/api/v1/incidents/nonexistent-id")
        assert response.status_code == 404


# Run tests with pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
