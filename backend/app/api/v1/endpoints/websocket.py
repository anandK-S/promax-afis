# ========================================
# Pro-Max AFIS - WebSocket Endpoints
# ========================================
# Real-time data synchronization and live updates
# Author: Pro-Max Development Team

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from typing import Dict, List
import json
import logging
from datetime import datetime

from app.core.config import settings
from app.api.v1.endpoints.auth import get_current_user
from app.core.redis_client import redis_client

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Active WebSocket connections manager
class ConnectionManager:
    """
    WebSocket connection manager for handling real-time connections
    """
    
    def __init__(self):
        # Dictionary to store active connections: {user_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # Dictionary to store business connections: {business_id: [user_ids]}
        self.business_connections: Dict[str, List[str]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, business_id: str):
        """
        Accept WebSocket connection and register user
        """
        await websocket.accept()
        self.active_connections[user_id] = websocket
        
        # Add to business connections
        if business_id not in self.business_connections:
            self.business_connections[business_id] = []
        if user_id not in self.business_connections[business_id]:
            self.business_connections[business_id].append(user_id)
        
        logger.info(f"WebSocket connected: user_id={user_id}, business_id={business_id}")
        
        # Send welcome message
        await self.send_personal_message({
            "event": "connected",
            "message": "WebSocket connection established",
            "timestamp": datetime.utcnow().isoformat()
        }, user_id)
    
    def disconnect(self, user_id: str, business_id: str):
        """
        Remove WebSocket connection
        """
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Remove from business connections
        if business_id in self.business_connections:
            if user_id in self.business_connections[business_id]:
                self.business_connections[business_id].remove(user_id)
            # Clean up empty lists
            if not self.business_connections[business_id]:
                del self.business_connections[business_id]
        
        logger.info(f"WebSocket disconnected: user_id={user_id}, business_id={business_id}")
    
    async def send_personal_message(self, message: dict, user_id: str):
        """
        Send message to specific user
        """
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception as e:
                logger.error(f"Failed to send message to user {user_id}: {str(e)}")
                # Remove connection if it's broken
                self.disconnect(user_id, "")
    
    async def broadcast_to_business(self, message: dict, business_id: str):
        """
        Broadcast message to all users in a business
        """
        if business_id in self.business_connections:
            disconnected_users = []
            for user_id in self.business_connections[business_id]:
                try:
                    await self.active_connections[user_id].send_json(message)
                except Exception as e:
                    logger.error(f"Failed to broadcast to user {user_id}: {str(e)}")
                    disconnected_users.append(user_id)
            
            # Remove disconnected users
            for user_id in disconnected_users:
                self.disconnect(user_id, business_id)
    
    async def broadcast_to_all(self, message: dict):
        """
        Broadcast message to all connected users
        """
        disconnected_users = []
        for user_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Failed to broadcast to user {user_id}: {str(e)}")
                disconnected_users.append(user_id)
        
        # Remove disconnected users
        for user_id in disconnected_users:
            self.disconnect(user_id, "")


# Global connection manager instance
manager = ConnectionManager()


# ========================================
# WebSocket Endpoints
# ========================================

@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(..., description="JWT authentication token")
):
    """
    WebSocket endpoint for real-time updates
    
    Connects clients for real-time financial data, alerts, and notifications.
    Requires valid JWT token for authentication.
    
    Events:
    - connected: Connection established
    - transaction_created: New transaction created
    - transaction_updated: Transaction updated
    - transaction_deleted: Transaction deleted
    - financial_alert: Financial alert triggered
    - inventory_alert: Inventory alert triggered
    - dashboard_update: Dashboard data update
    - health_score_update: Financial health score update
    """
    
    try:
        # Verify JWT token
        from app.core.security import verify_token
        try:
            payload = verify_token(token)
            user_id: str = payload.get("sub")
            if not user_id:
                await websocket.close(code=4001, reason="Invalid token")
                return
        except Exception as e:
            logger.error(f"WebSocket authentication failed: {str(e)}")
            await websocket.close(code=4001, reason="Authentication failed")
            return
        
        # Get user and business ID from database
        from app.core.database import SessionLocal
        from app.models.user import User
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                await websocket.close(code=4003, reason="User not found or inactive")
                return
            
            business_id = str(user.business.id)
        finally:
            db.close()
        
        # Connect WebSocket
        await manager.connect(websocket, user_id, business_id)
        
        try:
            # Keep connection alive and handle incoming messages
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                message = json.loads(data)
                
                # Process incoming message
                await handle_websocket_message(websocket, user_id, business_id, message)
                
        except WebSocketDisconnect:
            manager.disconnect(user_id, business_id)
            logger.info(f"WebSocket disconnected: user_id={user_id}")
        except Exception as e:
            logger.error(f"WebSocket error for user {user_id}: {str(e)}")
            manager.disconnect(user_id, business_id)
    
    except Exception as e:
        logger.error(f"WebSocket connection failed: {str(e)}")
        await websocket.close(code=4000, reason="Connection failed")


async def handle_websocket_message(
    websocket: WebSocket,
    user_id: str,
    business_id: str,
    message: dict
):
    """
    Handle incoming WebSocket messages from clients
    
    Supported message types:
    - ping: Keep-alive ping
    - subscribe: Subscribe to specific events
    - unsubscribe: Unsubscribe from events
    """
    
    message_type = message.get("type")
    
    if message_type == "ping":
        # Respond to ping with pong
        await websocket.send_json({
            "type": "pong",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    elif message_type == "subscribe":
        # Subscribe to specific events
        events = message.get("events", [])
        logger.info(f"User {user_id} subscribed to events: {events}")
        
        # Store subscription in Redis
        subscription_key = f"ws:subscription:{user_id}"
        redis_client.session_set(subscription_key, json.dumps(events), expire_seconds=3600)
        
        await websocket.send_json({
            "type": "subscribed",
            "events": events,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    elif message_type == "unsubscribe":
        # Unsubscribe from events
        redis_client.session_delete(f"ws:subscription:{user_id}")
        
        await websocket.send_json({
            "type": "unsubscribed",
            "timestamp": datetime.utcnow().isoformat()
        })
    
    else:
        # Unknown message type
        await websocket.send_json({
            "type": "error",
            "message": f"Unknown message type: {message_type}",
            "timestamp": datetime.utcnow().isoformat()
        })


# ========================================
# Helper Functions for Broadcasting Events
# ========================================

async def broadcast_transaction_created(
    transaction_data: dict,
    business_id: str
):
    """
    Broadcast transaction creation event
    """
    await manager.broadcast_to_business({
        "event": "transaction_created",
        "data": transaction_data,
        "timestamp": datetime.utcnow().isoformat()
    }, business_id)


async def broadcast_financial_alert(
    alert_data: dict,
    business_id: str
):
    """
    Broadcast financial alert event
    """
    await manager.broadcast_to_business({
        "event": "financial_alert",
        "data": alert_data,
        "timestamp": datetime.utcnow().isoformat()
    }, business_id)


async def broadcast_inventory_alert(
    alert_data: dict,
    business_id: str
):
    """
    Broadcast inventory alert event
    """
    await manager.broadcast_to_business({
        "event": "inventory_alert",
        "data": alert_data,
        "timestamp": datetime.utcnow().isoformat()
    }, business_id)


async def broadcast_dashboard_update(
    dashboard_data: dict,
    business_id: str
):
    """
    Broadcast dashboard data update event
    """
    await manager.broadcast_to_business({
        "event": "dashboard_update",
        "data": dashboard_data,
        "timestamp": datetime.utcnow().isoformat()
    }, business_id)


async def broadcast_health_score_update(
    health_score_data: dict,
    business_id: str
):
    """
    Broadcast financial health score update event
    """
    await manager.broadcast_to_business({
        "event": "health_score_update",
        "data": health_score_data,
        "timestamp": datetime.utcnow().isoformat()
    }, business_id)


# Export functions for use in other modules
__all__ = [
    "manager",
    "broadcast_transaction_created",
    "broadcast_financial_alert",
    "broadcast_inventory_alert",
    "broadcast_dashboard_update",
    "broadcast_health_score_update"
]