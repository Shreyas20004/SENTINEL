"""
Incidents API endpoints
"""
import logging
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models import Incident, Alert
from app.schemas import IncidentResponse, IncidentCreate, IncidentUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/incidents", response_model=List[IncidentResponse])
async def list_incidents(
    region: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db)
):
    """
    Get incidents with optional filtering.
    
    Query Parameters:
    - region: Filter by zone/region ID
    - severity: Filter by severity (LOW, MED, HIGH)
    - status: Filter by status (OPEN, INVESTIGATING, RESOLVED, FALSE_ALARM)
    - limit: Maximum results (default: 100, max: 1000)
    - offset: Pagination offset (default: 0)
    """
    query = select(Incident).order_by(desc(Incident.detected_at))
    
    # Apply filters
    filters = []
    if region:
        filters.append(Incident.zone_id == region)
    if severity:
        filters.append(Incident.severity == severity)
    if status:
        filters.append(Incident.status == status)
    
    if filters:
        query = query.where(and_(*filters))
    
    # Apply pagination
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    incidents = result.scalars().all()
    return incidents


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
async def get_incident(
    incident_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific incident"""
    query = select(Incident).where(Incident.id == incident_id)
    query = query.options(selectinload(Incident.alerts))
    
    result = await db.execute(query)
    incident = result.scalars().first()
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return incident


@router.post("/incidents", response_model=IncidentResponse)
async def create_incident(
    incident_data: IncidentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new incident"""
    incident = Incident(
        id=f"incident_{uuid4().hex[:12]}",
        zone_id=incident_data.zone_id,
        incident_type=incident_data.incident_type,
        severity=incident_data.severity,
        description=incident_data.description,
        location_lat=incident_data.location_lat,
        location_lng=incident_data.location_lng,
    )
    
    db.add(incident)
    await db.commit()
    await db.refresh(incident)
    
    logger.info(f"Created incident {incident.id}")
    return incident


@router.patch("/incidents/{incident_id}", response_model=IncidentResponse)
async def update_incident(
    incident_id: str,
    update_data: IncidentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an incident"""
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    incident = result.scalars().first()
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Update fields
    if update_data.severity is not None:
        incident.severity = update_data.severity
    if update_data.status is not None:
        incident.status = update_data.status
    if update_data.description is not None:
        incident.description = update_data.description
    if update_data.false_positive is not None:
        incident.false_positive = update_data.false_positive
    
    await db.commit()
    await db.refresh(incident)
    
    logger.info(f"Updated incident {incident_id}")
    return incident
