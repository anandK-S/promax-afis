# ========================================
# Pro-Max AFIS - Notification Tasks
# ========================================
# Background tasks for notifications and alerts
# Author: Pro-Max Development Team

from app.tasks.celery_app import celery_app
from app.services.notification_service import NotificationService
from app.core.database import SessionLocal
from app.models.inventory import LowStockAlert, Product
from app.models.user import User
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.notification_tasks.send_low_stock_alert")
def send_low_stock_alert(self, alert_id: int):
    """
    Send low stock alert notification
    
    Args:
        alert_id: Low stock alert ID
    """
    db = SessionLocal()
    try:
        logger.info(f"Sending low stock alert: {alert_id}")
        
        # Get alert with product
        alert = db.query(LowStockAlert).filter(
            LowStockAlert.id == alert_id
        ).first()
        
        if not alert:
            logger.warning(f"Alert {alert_id} not found")
            return {"status": "failed", "error": "Alert not found"}
        
        product = db.query(Product).filter(Product.id == alert.product_id).first()
        
        # Get business users who should receive alerts
        users = db.query(User).filter(
            User.business_id == alert.business_id,
            User.is_active == True
        ).all()
        
        notification_service = NotificationService()
        
        # Send notifications to all users
        for user in users:
            # Create in-app notification
            notification_service.create_notification(
                db=db,
                user_id=user.id,
                business_id=alert.business_id,
                notification_type="low_stock",
                title=f"Low Stock Alert: {product.product_name}",
                message=f"Product '{product.product_name}' is running low on stock. Current: {alert.current_stock}, Reorder at: {alert.reorder_point}",
                action_url=f"/inventory/products/{product.id}",
                metadata={
                    "product_id": product.id,
                    "product_name": product.product_name,
                    "current_stock": alert.current_stock,
                    "severity": alert.severity
                }
            )
        
        # Mark as notified
        alert.is_notified = True
        alert.notified_at = datetime.utcnow()
        
        db.commit()
        
        logger.info(f"Low stock alert sent: {alert_id}")
        
        return {"status": "success", "notified_users": len(users)}
        
    except Exception as e:
        logger.error(f"Low stock alert sending failed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.notification_tasks.send_financial_alert")
def send_financial_alert(
    self,
    business_id: int,
    alert_type: str,
    title: str,
    message: str,
    metadata: dict = None
):
    """
    Send financial alert notification
    
    Args:
        business_id: Business ID
        alert_type: Type of alert
        title: Alert title
        message: Alert message
        metadata: Additional metadata
    """
    db = SessionLocal()
    try:
        logger.info(f"Sending financial alert for business {business_id}: {alert_type}")
        
        # Get business users
        users = db.query(User).filter(
            User.business_id == business_id,
            User.is_active == True
        ).all()
        
        notification_service = NotificationService()
        
        # Send notifications
        for user in users:
            notification_service.create_notification(
                db=db,
                user_id=user.id,
                business_id=business_id,
                notification_type=alert_type,
                title=title,
                message=message,
                metadata=metadata or {}
            )
            
            # Send email if user has email
            if user.email:
                notification_service.send_email_notification(
                    email=user.email,
                    subject=title,
                    body=message
                )
        
        logger.info(f"Financial alert sent to {len(users)} users")
        
        return {"status": "success", "notified_users": len(users)}
        
    except Exception as e:
        logger.error(f"Financial alert sending failed: {str(e)}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.notification_tasks.send_daily_summary")
def send_daily_summary(self, business_id: int):
    """
    Send daily financial summary
    
    Args:
        business_id: Business ID
    """
    db = SessionLocal()
    try:
        logger.info(f"Sending daily summary for business {business_id}")
        
        # Get business admin users
        users = db.query(User).filter(
            User.business_id == business_id,
            User.is_active == True
        ).all()
        
        notification_service = NotificationService()
        
        # Send daily summary notifications
        for user in users:
            notification_service.create_notification(
                db=db,
                user_id=user.id,
                business_id=business_id,
                notification_type="daily_summary",
                title="Daily Financial Summary",
                message="Your daily financial summary is ready.",
                metadata={"date": datetime.utcnow().isoformat()}
            )
        
        logger.info(f"Daily summary sent for business {business_id}")
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Daily summary sending failed: {str(e)}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.notification_tasks.send_report_email")
def send_report_email(
    self,
    business_id: int,
    report_type: str,
    report_data: dict
):
    """
    Send report via email
    
    Args:
        business_id: Business ID
        report_type: Type of report
        report_data: Report data
    """
    db = SessionLocal()
    try:
        logger.info(f"Sending {report_type} report for business {business_id}")
        
        # Get business admin users
        users = db.query(User).filter(
            User.business_id == business_id,
            User.is_active == True
        ).all()
        
        notification_service = NotificationService()
        
        # Send emails
        sent_count = 0
        for user in users:
            if user.email:
                notification_service.send_email_notification(
                    email=user.email,
                    subject=f"{report_type.replace('_', ' ').title()} Report",
                    body=f"Your {report_type} report is ready.",
                    html_body=f"<h1>{report_type.replace('_', ' ').title()} Report</h1>"
                )
                sent_count += 1
        
        logger.info(f"Report email sent to {sent_count} users")
        
        return {"status": "success", "sent_count": sent_count}
        
    except Exception as e:
        logger.error(f"Report email sending failed: {str(e)}")
        raise
    finally:
        db.close()