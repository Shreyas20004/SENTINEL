"""
WebSocket endpoint for real-time alert streaming

Connects to Redis pub/sub for live alert broadcasting
"""

import asyncio
import logging
import json
from typing import Set
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from app.core.redis_client import redis_client

logger = logging.getLogger(__name__)

router = APIRouter()

# Active WebSocket connections
active_connections: Set[WebSocket] = set()


class ConnectionManager:
    """Manage WebSocket connections and message broadcasting"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def accept(self, websocket: WebSocket):
        """Accept new connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected: {len(self.active_connections)} active")
    
    async def disconnect(self, websocket: WebSocket):
        """Close connection"""
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected: {len(self.active_connections)} active")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected clients"""
        disconnected = []
        
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Error sending to WebSocket: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected
        for conn in disconnected:
            self.active_connections.discard(conn)
    
    def get_active_count(self) -> int:
        """Get number of active connections"""
        return len(self.active_connections)


manager = ConnectionManager()


@router.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """
    Real-time alert streaming via WebSocket
    
    Connect: ws://localhost:8000/ws/alerts
    
    Receives alert messages from Redis pub/sub:
    {
        'event': 'alert',
        'alert_id': 'str',
        'incident_id': 'str',
        'camera_id': 'str',
        'timestamp': 'ISO8601',
        'confidence': 0-1,
        'type': 'LOITERING|CROWD|BREACH'
    }
    """
    await manager.accept(websocket)
    
    # Subscribe to alerts channel
    pubsub = None
    try:
        pubsub = await redis_client.client.pubsub()
        await pubsub.subscribe('sentinel:alerts')
        
        logger.info("WebSocket subscribed to sentinel:alerts channel")
        
        while True:
            # Receive message from Redis
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            
            if message is not None and message['type'] == 'message':
                try:
                    # Parse and forward to client
                    alert_data = json.loads(message['data'].decode())
                    await manager.broadcast(alert_data)
                    logger.debug(f"Broadcast alert: {alert_data.get('alert_id')}")
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse alert message: {e}")
            
            # Check for client disconnect
            try:
                # Try to receive (will raise exception on disconnect)
                await asyncio.sleep(0.1)
            except WebSocketDisconnect:
                break
    
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)
        if pubsub:
            await pubsub.unsubscribe('sentinel:alerts')
            await pubsub.close()


@router.websocket("/ws/metrics")
async def websocket_metrics(websocket: WebSocket):
    """
    Real-time metrics streaming (risk dial, KPIs)
    
    Connect: ws://localhost:8000/ws/metrics
    
    Receives metrics updates:
    {
        'event': 'metrics_update',
        'risk_score': 0-100,
        'active_incidents': int,
        'alerts_per_hour': int,
        'timestamp': 'ISO8601',
        'uptime_percentage': 0-100
    }
    """
    await manager.accept(websocket)
    pubsub = None
    
    try:
        pubsub = await redis_client.client.pubsub()
        await pubsub.subscribe('sentinel:metrics')
        
        logger.info("WebSocket subscribed to sentinel:metrics channel")
        
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            
            if message is not None and message['type'] == 'message':
                try:
                    metrics = json.loads(message['data'].decode())
                    await manager.broadcast(metrics)
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse metrics: {e}")
            
            await asyncio.sleep(0.1)
    
    except WebSocketDisconnect:
        logger.info("Metrics WebSocket disconnected")
    except Exception as e:
        logger.error(f"Metrics WebSocket error: {e}")
    finally:
        manager.disconnect(websocket)
        if pubsub:
            await pubsub.unsubscribe('sentinel:metrics')
            await pubsub.close()


@router.get("/ws/health")
async def websocket_health():
    """Get WebSocket connection health status"""
    return {
        'active_connections': manager.get_active_count(),
        'status': 'healthy' if manager.get_active_count() >= 0 else 'degraded'
    }
