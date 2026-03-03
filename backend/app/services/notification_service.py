# ========================================
# Pro-Max AFIS - Notification Service
# ========================================
# Business logic for notifications and alerts
# Author: Pro-Max Development Team

from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from app.core.redis_client import redis_client

# Configure logging
logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service class for notifications and alerts
    """
    
    def __init__(self):
        """Initialize notification service"""
        self.cache_ttl = 3600  # 1 hour
    
    async def send_websocket_notification(
        self,
        connection_manager,
        business_id: str,
        event_type: str,
        data: Dict
    ):
        """
        Send WebSocket notification to business users
        
        Args:
            connection_manager: WebSocket connection manager
            business_id: Business ID
            event_type: Type of event
            data: Notification data
        """
        try:
            message = {
                "event": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            await connection_manager.broadcast_to_business(message, business_id)
            
            logger.info(f"WebSocket notification sent: {event_type} to business {business_id}")
            
        except Exception as e:
            logger.error(f"WebSocket notification failed: {str(e)}")
    
    def create_notification(
        self,
        db: Session,
        user_id: int,
        business_id: int,
        notification_type: str,
        title: str,
        message: str,
        action_url: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Create a notification for a user
        
        Args:
            db: Database session
            user_id: User ID
            business_id: Business ID
            notification_type: Type of notification
            title: Notification title
            message: Notification message
            action_url: Optional action URL
            metadata: Optional metadata
        """
        try:
            # This would create a notification record in the database
            # For now, we'll just log it
            logger.info(f"Notification created for user {user_id}: {title}")
            
            # Cache notification count
            cache_key = f"notification_count:{user_id}"
            current_count = redis_client.cache_get(cache_key) or 0
            redis_client.cache_set(cache_key, current_count + 1, self.cache_ttl)
            
        except Exception as e:
            logger.error(f"Notification creation failed: {str(e)}")
    
    def get_notification_count(
        self,
        user_id: int
    ) -> int:
        """
        Get unread notification count for user
        
        Args:
            user_id: User ID
            
        Returns:
            Notification count
        """
        try:
            cache_key = f"notification_count:{user_id}"
            count = redis_client.cache_get(cache_key)
            return count or 0
        except Exception as e:
            logger.error(f"Failed to get notification count: {str(e)}")
            return 0
    
    def mark_notifications_as_read(
        self,
        user_id: int
    ):
        """
        Mark all notifications as read for user
        
        Args:
            user_id: User ID
        """
        try:
            cache_key = f"notification_count:{user_id}"
            redis_client.cache_delete(cache_key)
            
            logger.info(f"Notifications marked as read for user {user_id}")
            
        except Exception as e:
            logger.error(f"Failed to mark notifications as read: {str(e)}")
    
    def send_email_notification(
        self,
        email: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ):
        """
        Send email notification
        
        Args:
            email: Recipient email
            subject: Email subject
            body: Email body (plain text)
            html_body: Email body (HTML, optional)
        """
        try:
            # This would integrate with an email service like SendGrid, AWS SES, etc.
            # For now, we'll just log it
            logger.info(f"Email notification sent to {email}: {subject}")
            
        except Exception as e:
            logger.error(f"Email notification failed: {str(e)}")
    
    def send_sms_notification(
        self,
        phone: str,
        message: str
    ):
        """
        Send SMS notification
        
        Args:
            phone: Recipient phone number
            message: SMS message
        """
        try:
            # This would integrate with an SMS service like Twilio, etc.
            # For now, we'll just log it
            logger.info(f"SMS notification sent to {phone}: {message[:50]}...")
            
        except Exception as e:
            logger.error(f"SMS notification failed: {str(e)}")