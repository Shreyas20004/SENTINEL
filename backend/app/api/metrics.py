"""
Metrics API endpoints
"""
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Alert, Camera, Incident, Metric as MetricModel
from app.schemas import MetricsResponse, RiskDialResponse, SeverityLevel

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    window: str = Query("1h"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get system metrics.
    
    Window options: 1h, 6h, 24h, 7d
    Returns: uptime %, alerts/hr, response time, incident counts
    """
    # Parse window
    time_delta = _parse_time_window(window)
    cutoff_time = datetime.utcnow() - time_delta
    
    # Get incidents in time window
    incident_result = await db.execute(
        select(func.count(Incident.id)).where(
            Incident.detected_at >= cutoff_time
        )
    )
    total_incidents = incident_result.scalar() or 0
    
    # Get active incidents
    active_result = await db.execute(
        select(func.count(Incident.id)).where(
            and_(
                Incident.status.in_(["OPEN", "INVESTIGATING"]),
                Incident.detected_at >= cutoff_time
            )
        )
    )
    active_incidents = active_result.scalar() or 0
    
    # Get alerts in window
    alert_result = await db.execute(
        select(func.count(Alert.id)).where(
            Alert.created_at >= cutoff_time
        )
    )
    alerts_count = alert_result.scalar() or 0
    
    # Get camera count
    camera_result = await db.execute(
        select(func.count(Camera.id)).where(Camera.is_active == True)
    )
    camera_count = camera_result.scalar() or 0
    
    # Calculate alerts per hour
    hours = max(time_delta.total_seconds() / 3600, 1)
    alerts_per_hour = alerts_count / hours
    
    # Get average uptime (simplified)
    uptime_result = await db.execute(
        select(func.avg(Camera.uptime_percentage)).where(Camera.is_active == True)
    )
    uptime_percentage = uptime_result.scalar() or 100.0
    
    # Get average response time (simplified - placeholder)
    average_response_time = 2.5  # minutes
    
    return MetricsResponse(
        uptime_percentage=uptime_percentage,
        alerts_per_hour=alerts_per_hour,
        average_response_time_minutes=average_response_time,
        total_incidents=total_incidents,
        active_incidents=active_incidents,
        camera_count=camera_count,
        zone_count=1  # Will be updated in Phase 3
    )


@router.get("/metrics/risk-dial", response_model=RiskDialResponse)
async def get_risk_dial(db: AsyncSession = Depends(get_db)):
    """Get real-time risk dial data"""
    
    # Count incidents by severity
    high_result = await db.execute(
        select(func.count(Incident.id)).where(
            and_(
                Incident.severity == "HIGH",
                Incident.status.in_(["OPEN", "INVESTIGATING"])
            )
        )
    )
    high_count = high_result.scalar() or 0
    
    med_result = await db.execute(
        select(func.count(Incident.id)).where(
            and_(
                Incident.severity == "MED",
                Incident.status.in_(["OPEN", "INVESTIGATING"])
            )
        )
    )
    med_count = med_result.scalar() or 0
    
    low_result = await db.execute(
        select(func.count(Incident.id)).where(
            and_(
                Incident.severity == "LOW",
                Incident.status.in_(["OPEN", "INVESTIGATING"])
            )
        )
    )
    low_count = low_result.scalar() or 0
    
    # Get camera count
    camera_result = await db.execute(
        select(func.count(Camera.id)).where(Camera.is_active == True)
    )
    camera_count = camera_result.scalar() or 1
    
    # Calculate risk score: (HIGH×3 + MED×1.5 + LOW×1) / camera_count
    risk_score = (high_count * 3 + med_count * 1.5 + low_count * 1) / camera_count
    
    # Determine severity
    if risk_score < 45:
        severity = SeverityLevel.LOW
    elif risk_score < 70:
        severity = SeverityLevel.MED
    else:
        severity = SeverityLevel.HIGH
    
    return RiskDialResponse(
        risk_score=risk_score,
        severity=severity,
        high_count=high_count,
        med_count=med_count,
        low_count=low_count
    )


def _parse_time_window(window: str) -> timedelta:
    """Parse time window string to timedelta"""
    mapping = {
        "1h": timedelta(hours=1),
        "6h": timedelta(hours=6),
        "24h": timedelta(hours=24),
        "7d": timedelta(days=7),
    }
    return mapping.get(window, timedelta(hours=1))
