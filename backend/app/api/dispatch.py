"""
Dispatch API endpoints
"""
import logging
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas import DispatchRequest, DispatchResponse

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/dispatch/escalate", response_model=DispatchResponse)
async def escalate_dispatch(
    dispatch_data: DispatchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Escalate HIGH alerts to supervisor via WhatsApp/SMS.
    
    Phase 1: Basic dispatch endpoint
    Phase 3: Integration with emergency helplines (112, 181, 100, 108, 1098)
    
    In production:
    - Send SMS/WhatsApp to on-duty supervisor
    - Log dispatch action to incidents table
    - Return tel: URI for one-tap calling
    """
    dispatch_id = f"dispatch_{uuid4().hex[:12]}"
    
    logger.info(
        f"Escalating dispatch {dispatch_id} for alerts: {dispatch_data.alert_ids}"
    )
    
    # TODO: Implement actual dispatch (Phase 3)
    # - Get operator geolocation
    # - Match emergency number based on state
    # - Send WhatsApp/SMS notification
    # - Log to database
    
    from datetime import datetime, timedelta
    
    return DispatchResponse(
        dispatch_id=dispatch_id,
        alert_ids=dispatch_data.alert_ids,
        status="DISPATCHED",
        timestamp=datetime.utcnow()
    )
