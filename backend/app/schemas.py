"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


# ============= Enums =============

class SeverityLevel(str, Enum):
    LOW = "LOW"
    MED = "MED"
    HIGH = "HIGH"


class AlertType(str, Enum):
    PERIMETER_BREACH = "PERIMETER_BREACH"
    ABANDONED_OBJECT = "ABANDONED_OBJECT"
    CROWD_SURGE = "CROWD_SURGE"
    LOITERING = "LOITERING"
    UNKNOWN = "UNKNOWN"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    FALSE_ALARM = "FALSE_ALARM"


# ============= Camera Schemas =============

class CameraCreate(BaseModel):
    name: str
    zone_id: str
    location: Optional[str] = None
    rtsp_url: str


class CameraUpdate(BaseModel):
    name: Optional[str] = None
    zone_id: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


class CameraResponse(BaseModel):
    id: str
    name: str
    zone_id: str
    location: Optional[str]
    is_active: bool
    uptime_percentage: float
    last_heartbeat: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Alert Schemas =============

class AlertCreate(BaseModel):
    incident_id: Optional[str] = None
    camera_id: str
    alert_type: AlertType
    severity: SeverityLevel
    confidence: float
    bbox: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


class AlertResponse(BaseModel):
    id: str
    incident_id: Optional[str]
    camera_id: str
    alert_type: AlertType
    severity: SeverityLevel
    confidence: float
    is_confirmed: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Incident Schemas =============

class IncidentCreate(BaseModel):
    zone_id: str
    incident_type: str
    severity: SeverityLevel
    description: Optional[str] = None
    location_lat: Optional[float] = None
    location_lng: Optional[float] = None


class IncidentUpdate(BaseModel):
    severity: Optional[SeverityLevel] = None
    status: Optional[IncidentStatus] = None
    description: Optional[str] = None
    false_positive: Optional[bool] = None


class IncidentResponse(BaseModel):
    id: str
    zone_id: str
    incident_type: str
    severity: SeverityLevel
    status: IncidentStatus
    description: Optional[str]
    location_lat: Optional[float]
    location_lng: Optional[float]
    alert_count: int
    detected_at: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Zone Schemas =============

class ZoneResponse(BaseModel):
    id: str
    name: str
    risk_score: float
    severity: SeverityLevel
    created_at: datetime
    
    class Config:
        from_attributes = True


# ============= Metrics Schemas =============

class MetricPoint(BaseModel):
    timestamp: datetime
    value: float


class MetricsResponse(BaseModel):
    uptime_percentage: float
    alerts_per_hour: float
    average_response_time_minutes: float
    total_incidents: int
    active_incidents: int
    camera_count: int
    zone_count: int


class RiskDialResponse(BaseModel):
    risk_score: float
    severity: SeverityLevel
    high_count: int
    med_count: int
    low_count: int


# ============= Dispatch Schemas =============

class DispatchRequest(BaseModel):
    alert_ids: List[str]
    unit_id: Optional[str] = None
    notes: Optional[str] = None


class DispatchResponse(BaseModel):
    dispatch_id: str
    alert_ids: List[str]
    status: str
    timestamp: datetime


# ============= Report Schemas =============

class ReportRequest(BaseModel):
    from_date: datetime
    to_date: datetime
    zone_id: Optional[str] = None


class ReportResponse(BaseModel):
    report_id: str
    download_url: str
    expires_at: datetime
