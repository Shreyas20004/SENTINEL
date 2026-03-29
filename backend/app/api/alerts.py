"""
Alerts API endpoints
"""
import logging
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.redis_client import redis_client
from app.models import Alert, Incident
from app.schemas import AlertResponse, AlertCreate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/alerts", response_model=AlertResponse)
async def create_alert(
    alert_data: AlertCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new alert from inference engine.
    
    The alert is:
    1. Stored in PostgreSQL
    2. Published to Redis for real-time broadcast
    3. Linked to incident if exists
    """
    alert = Alert(
        id=f"alert_{uuid4().hex[:12]}",
        incident_id=alert_data.incident_id,
        camera_id=alert_data.camera_id,
        alert_type=alert_data.alert_type,
        severity=alert_data.severity,
        confidence=alert_data.confidence,
        bbox=str(alert_data.bbox) if alert_data.bbox else None,
        metadata=str(alert_data.metadata) if alert_data.metadata else None,
    )
    
    db.add(alert)
    
    # Link to incident and update alert count
    if alert_data.incident_id:
        result = await db.execute(
            select(Incident).where(Incident.id == alert_data.incident_id)
        )
        incident = result.scalars().first()
        if incident:
            incident.alert_count += 1
    
    await db.commit()
    await db.refresh(alert)
    
    # Publish to Redis for real-time updates
    await redis_client.publish(
        "sentinel:alerts",
        {
            "id": alert.id,
            "incident_id": alert.incident_id,
            "camera_id": alert.camera_id,
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "confidence": alert.confidence,
            "created_at": alert.created_at.isoformat()
        }
    )
    
    logger.info(f"Created alert {alert.id} for camera {alert.camera_id}")
    return alert


@router.get("/alerts", response_model=List[AlertResponse])
async def list_alerts(
    incident_id: Optional[str] = Query(None),
    camera_id: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db)
):
    """List recent alerts with optional filtering"""
    query = select(Alert).order_by(desc(Alert.created_at))
    
    filters = []
    if incident_id:
        filters.append(Alert.incident_id == incident_id)
    if camera_id:
        filters.append(Alert.camera_id == camera_id)
    
    if filters:
        from sqlalchemy import and_
        query = query.where(and_(*filters))
    
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    alerts = result.scalars().all()
    return alerts
