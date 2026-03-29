# SENTINEL API Examples

Collection of cURL examples for testing SENTINEL API endpoints.

## Health Check

```bash
curl -X GET http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "SENTINEL"
}
```

---

## Cameras

### Register Camera
```bash
curl -X POST http://localhost:8000/api/v1/cameras \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CAM-01",
    "zone_id": "zone_1",
    "location": "Main Gate",
    "rtsp_url": "rtsp://192.168.1.100:554/stream"
  }'
```

### List Cameras
```bash
curl -X GET http://localhost:8000/api/v1/cameras
```

### Get Specific Camera
```bash
curl -X GET http://localhost:8000/api/v1/cameras/{camera_id}
```

### Update Camera
```bash
curl -X PATCH http://localhost:8000/api/v1/cameras/{camera_id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Name",
    "is_active": true
  }'
```

---

## Incidents

### Create Incident
```bash
curl -X POST http://localhost:8000/api/v1/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "zone_id": "zone_1",
    "incident_type": "PERIMETER_BREACH",
    "severity": "HIGH",
    "description": "Unauthorized entry detected",
    "location_lat": 28.6139,
    "location_lng": 77.2090
  }'
```

### List Incidents
```bash
# All incidents
curl -X GET http://localhost:8000/api/v1/incidents

# Filter by zone
curl -X GET "http://localhost:8000/api/v1/incidents?region=zone_1"

# Filter by severity
curl -X GET "http://localhost:8000/api/v1/incidents?severity=HIGH"

# With pagination
curl -X GET "http://localhost:8000/api/v1/incidents?limit=50&offset=0"
```

### Get Specific Incident
```bash
curl -X GET http://localhost:8000/api/v1/incidents/{incident_id}
```

### Update Incident
```bash
curl -X PATCH http://localhost:8000/api/v1/incidents/{incident_id} \
  -H "Content-Type: application/json" \
  -d '{
    "status": "RESOLVED",
    "severity": "MED",
    "false_positive": false
  }'
```

---

## Alerts

### Create Alert (from AI/ML inference)
```bash
curl -X POST http://localhost:8000/api/v1/alerts \
  -H "Content-Type: application/json" \
  -d '{
    "camera_id": "cam_001",
    "alert_type": "LOITERING",
    "severity": "MED",
    "confidence": 0.87,
    "bbox": {"x": 100, "y": 150, "width": 50, "height": 60},
    "metadata": {"track_id": 5, "dwell_time": 120}
  }'
```

### List Alerts
```bash
# Recent alerts
curl -X GET "http://localhost:8000/api/v1/alerts?limit=50"

# Filter by incident
curl -X GET "http://localhost:8000/api/v1/alerts?incident_id={incident_id}"

# Filter by camera
curl -X GET "http://localhost:8000/api/v1/alerts?camera_id={camera_id}"
```

---

## Metrics

### Get System Metrics
```bash
# Last 1 hour
curl -X GET "http://localhost:8000/api/v1/metrics?window=1h"

# Last 24 hours
curl -X GET "http://localhost:8000/api/v1/metrics?window=24h"

# Last 7 days
curl -X GET "http://localhost:8000/api/v1/metrics?window=7d"
```

**Response:**
```json
{
  "uptime_percentage": 99.8,
  "alerts_per_hour": 2.3,
  "average_response_time_minutes": 2.5,
  "total_incidents": 156,
  "active_incidents": 3,
  "camera_count": 12,
  "zone_count": 5
}
```

### Get Risk Dial
```bash
curl -X GET http://localhost:8000/api/v1/metrics/risk-dial
```

**Response:**
```json
{
  "risk_score": 62,
  "severity": "MED",
  "high_count": 1,
  "med_count": 3,
  "low_count": 5
}
```

---

## Zones

### List Zones
```bash
curl -X GET http://localhost:8000/api/v1/zones
```

### Get Specific Zone
```bash
curl -X GET http://localhost:8000/api/v1/zones/{zone_id}
```

---

## Dispatch

### Escalate Alert
```bash
curl -X POST http://localhost:8000/api/v1/dispatch/escalate \
  -H "Content-Type: application/json" \
  -d '{
    "alert_ids": ["alert_001", "alert_002"],
    "unit_id": "unit_123",
    "notes": "Perimeter breach at main gate"
  }'
```

---

## Reports

### Generate Report
```bash
curl -X POST http://localhost:8000/api/v1/reports/generate \
  -H "Content-Type: application/json" \
  -d '{
    "from_date": "2024-01-01T00:00:00Z",
    "to_date": "2024-01-31T23:59:59Z",
    "zone_id": "zone_1"
  }'
```

---

## WebSocket Events

Connect to WebSocket for real-time alert streaming:

```javascript
// JavaScript example
const ws = new WebSocket('ws://localhost:8000/ws/alerts');

ws.onmessage = (event) => {
  const alert = JSON.parse(event.data);
  console.log('New alert:', alert);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

---

## Batch Testing Script

```bash
#!/bin/bash

API_URL="http://localhost:8000/api/v1"

# Create multiple cameras
for i in {1..5}; do
  curl -X POST $API_URL/cameras \
    -H "Content-Type: application/json" \
    -d "{
      \"name\": \"CAM-0$i\",
      \"zone_id\": \"zone_1\",
      \"location\": \"Gate $i\",
      \"rtsp_url\": \"rtsp://192.168.1.$((100+i)):554/stream\"
    }" \
    -s | jq .
done

# Create incidents
for i in {1..3}; do
  curl -X POST $API_URL/incidents \
    -H "Content-Type: application/json" \
    -d "{
      \"zone_id\": \"zone_1\",
      \"incident_type\": \"LOITERING\",
      \"severity\": \"MED\",
      \"description\": \"Test incident $i\"
    }" \
    -s | jq .
done

# Get metrics
curl -X GET "$API_URL/metrics?window=1h" -s | jq .
```

Save as `test.sh` and run: `bash test.sh`

---

## Testing with Postman

1. Import endpoints into Postman
2. Set base URL: `{{base_url}}/api/v1`
3. Create environment variable: `base_url = http://localhost:8000`
4. Use pre-request scripts for authentication (Phase 4)

---

**Last Updated:** March 29, 2026
