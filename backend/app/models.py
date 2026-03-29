"""
Database models for SENTINEL
"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Float, Integer, DateTime, Boolean, Enum as SQLEnum, Text, Index, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class SeverityLevel(str, Enum):
    """Alert severity levels"""
    LOW = "LOW"
    MED = "MED"
    HIGH = "HIGH"


class AlertType(str, Enum):
    """Alert types"""
    PERIMETER_BREACH = "PERIMETER_BREACH"
    ABANDONED_OBJECT = "ABANDONED_OBJECT"
    CROWD_SURGE = "CROWD_SURGE"
    LOITERING = "LOITERING"
    UNKNOWN = "UNKNOWN"


class IncidentStatus(str, Enum):
    """Incident status"""
    OPEN = "OPEN"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    FALSE_ALARM = "FALSE_ALARM"


# ============= Core Models =============

class Camera(Base):
    """CCTV Camera Model"""
    __tablename__ = "cameras"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    zone_id = Column(String, nullable=False)
    location = Column(String)
    rtsp_url = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)
    uptime_percentage = Column(Float, default=100.0)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    alerts = relationship("Alert", back_populates="camera")
    detections = relationship("Detection", back_populates="camera")
    
    __table_args__ = (
        Index('idx_camera_zone', 'zone_id'),
        Index('idx_camera_active', 'is_active'),
    )


class Zone(Base):
    """Geographical Zone Model"""
    __tablename__ = "zones"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    geometry = Column(Geometry('POLYGON'), nullable=False)
    risk_score = Column(Float, default=0.0)
    severity = Column(SQLEnum(SeverityLevel), default=SeverityLevel.LOW)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_zone_name', 'name'),
        Index('idx_zone_severity', 'severity'),
    )


class Incident(Base):
    """Incident Model"""
    __tablename__ = "incidents"
    
    id = Column(String, primary_key=True, index=True)
    zone_id = Column(String, nullable=False, index=True)
    incident_type = Column(String, nullable=False)
    severity = Column(SQLEnum(SeverityLevel), default=SeverityLevel.MED, index=True)
    status = Column(SQLEnum(IncidentStatus), default=IncidentStatus.OPEN, index=True)
    description = Column(Text)
    location_lat = Column(Float)
    location_lng = Column(Float)
    geometry = Column(Geometry('POINT'), nullable=True)
    
    alert_count = Column(Integer, default=0)
    confirmation_count = Column(Integer, default=0)
    false_positive = Column(Boolean, default=False)
    
    detected_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    alerts = relationship("Alert", back_populates="incident")
    
    __table_args__ = (
        Index('idx_incident_zone', 'zone_id'),
        Index('idx_incident_severity', 'severity'),
        Index('idx_incident_status', 'status'),
        Index('idx_incident_detected', 'detected_at'),
    )


class Alert(Base):
    """Alert Model"""
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, index=True)
    incident_id = Column(String, ForeignKey('incidents.id'), index=True)
    camera_id = Column(String, ForeignKey('cameras.id'), index=True)
    alert_type = Column(SQLEnum(AlertType), default=AlertType.UNKNOWN, index=True)
    severity = Column(SQLEnum(SeverityLevel), default=SeverityLevel.MED, index=True)
    
    confidence = Column(Float, default=0.0)
    bbox = Column(Text)  # JSON serialized bounding box
    metadata = Column(Text)  # JSON serialized additional data
    
    is_duplicate = Column(Boolean, default=False)
    is_confirmed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now(), index=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    incident = relationship("Incident", back_populates="alerts")
    camera = relationship("Camera", back_populates="alerts")
    
    __table_args__ = (
        Index('idx_alert_incident', 'incident_id'),
        Index('idx_alert_camera', 'camera_id'),
        Index('idx_alert_type', 'alert_type'),
        Index('idx_alert_severity', 'severity'),
        Index('idx_alert_created', 'created_at'),
    )


class Detection(Base):
    """Detection Model - Low-level detections from inference"""
    __tablename__ = "detections"
    
    id = Column(String, primary_key=True, index=True)
    camera_id = Column(String, ForeignKey('cameras.id'), index=True)
    
    class_id = Column(Integer)
    class_name = Column(String, index=True)
    confidence = Column(Float)
    bbox = Column(Text)  # JSON: [x1, y1, x2, y2]
    track_id = Column(Integer, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    # Relationships
    camera = relationship("Camera", back_populates="detections")
    
    __table_args__ = (
        Index('idx_detection_camera', 'camera_id'),
        Index('idx_detection_track', 'track_id'),
    )


# ============= Metrics & Analytics =============

class Metric(Base):
    """System Metrics Model"""
    __tablename__ = "metrics"
    
    id = Column(String, primary_key=True, index=True)
    metric_name = Column(String, nullable=False, index=True)
    metric_value = Column(Float, nullable=False)
    camera_id = Column(String, nullable=True)
    zone_id = Column(String, nullable=True)
    
    created_at = Column(DateTime, server_default=func.now(), index=True)
    
    __table_args__ = (
        Index('idx_metric_name', 'metric_name'),
        Index('idx_metric_created', 'created_at'),
    )
