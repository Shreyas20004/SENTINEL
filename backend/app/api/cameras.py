"""
Cameras API endpoints
"""
import logging
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models import Camera
from app.schemas import CameraResponse, CameraCreate, CameraUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/cameras", response_model=List[CameraResponse])
async def list_cameras(
    zone: Optional[str] = Query(None),
    active_only: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of cameras.
    
    Query Parameters:
    - zone: Filter by zone ID
    - active_only: Show only active cameras (default: False)
    """
    query = select(Camera)
    
    filters = []
    if zone:
        filters.append(Camera.zone_id == zone)
    if active_only:
        filters.append(Camera.is_active == True)
    
    if filters:
        from sqlalchemy import and_
        query = query.where(and_(*filters))
    
    result = await db.execute(query)
    cameras = result.scalars().all()
    return cameras


@router.get("/cameras/{camera_id}", response_model=CameraResponse)
async def get_camera(camera_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific camera"""
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalars().first()
    
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    return camera


@router.post("/cameras", response_model=CameraResponse)
async def create_camera(
    camera_data: CameraCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new camera RTSP stream"""
    camera = Camera(
        id=f"cam_{uuid4().hex[:12]}",
        name=camera_data.name,
        zone_id=camera_data.zone_id,
        location=camera_data.location,
        rtsp_url=camera_data.rtsp_url,
    )
    
    db.add(camera)
    await db.commit()
    await db.refresh(camera)
    
    logger.info(f"Created camera {camera.id}: {camera.name}")
    return camera


@router.patch("/cameras/{camera_id}", response_model=CameraResponse)
async def update_camera(
    camera_id: str,
    update_data: CameraUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update camera configuration"""
    result = await db.execute(select(Camera).where(Camera.id == camera_id))
    camera = result.scalars().first()
    
    if not camera:
        raise HTTPException(status_code=404, detail="Camera not found")
    
    if update_data.name is not None:
        camera.name = update_data.name
    if update_data.zone_id is not None:
        camera.zone_id = update_data.zone_id
    if update_data.location is not None:
        camera.location = update_data.location
    if update_data.is_active is not None:
        camera.is_active = update_data.is_active
    
    await db.commit()
    await db.refresh(camera)
    
    logger.info(f"Updated camera {camera_id}")
    return camera
