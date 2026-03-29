"""
Zones API endpoints
"""
import logging
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Zone  # Will be used in Phase 3
from app.schemas import ZoneResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/zones", response_model=List[ZoneResponse])
async def list_zones(db: AsyncSession = Depends(get_db)):
    """
    Get all zones with risk scores.
    Note: Zones are integrated in Phase 3 with GADM GeoJSON
    """
    result = await db.execute(select(Zone))
    zones = result.scalars().all()
    return zones


@router.get("/zones/{zone_id}", response_model=ZoneResponse)
async def get_zone(zone_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific zone with its risk score"""
    result = await db.execute(select(Zone).where(Zone.id == zone_id))
    zone = result.scalars().first()
    
    if not zone:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Zone not found")
    
    return zone
