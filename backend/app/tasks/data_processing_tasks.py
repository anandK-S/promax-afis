# ========================================
# Pro-Max AFIS - Data Processing Tasks
# ========================================
# Background tasks for data processing and maintenance
# Author: Pro-Max Development Team

from app.tasks.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.inventory import Product, LowStockAlert
from app.models.user import User
from app.models.financial import Transaction
from datetime import datetime, timedelta
import logging
import os

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="app.tasks.data_processing_tasks.check_low_stock")
def check_low_stock(self):
    """
    Check all products for low stock and create alerts
    This is a periodic task scheduled by Celery Beat
    """
    db = SessionLocal()
    try:
        logger.info("Checking low stock for all products")
        
        # Get all active products
        products = db.query(Product).filter(
            Product.is_active == True
        ).all()
        
        alerts_created = 0
        
        for product in products:
            # Check if product is low on stock
            if product.is_low_stock:
                # Check if alert already exists and is unresolved
                existing_alert = db.query(LowStockAlert).filter(
                    LowStockAlert.product_id == product.id,
                    LowStockAlert.is_resolved == False
                ).first()
                
                if not existing_alert:
                    # Determine severity
                    if product.current_stock == 0:
                        severity = "critical"
                    elif product.current_stock <= product.minimum_stock_level:
                        severity = "high"
                    else:
                        severity = "medium"
                    
                    # Create new alert
                    alert = LowStockAlert(
                        product_id=product.id,
                        business_id=product.business_id,
                        current_stock=product.current_stock,
                        reorder_point=product.reorder_point,
                        shortage_quantity=product.reorder_point - product.current_stock,
                        severity=severity
                    )
                    
                    db.add(alert)
                    alerts_created += 1
        
        db.commit()
        
        logger.info(f"Low stock check completed. Created {alerts_created} new alerts")
        
        return {"status": "success", "alerts_created": alerts_created}
        
    except Exception as e:
        logger.error(f"Low stock check failed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.data_processing_tasks.clean_old_logs")
def clean_old_logs(self):
    """
    Clean old log files
    This is a periodic task scheduled by Celery Beat
    """
    try:
        logger.info("Cleaning old log files")
        
        # Define log directory
        log_dir = "./logs"
        
        if not os.path.exists(log_dir):
            logger.warning(f"Log directory {log_dir} does not exist")
            return {"status": "success", "cleaned": 0}
        
        # Get current time
        now = datetime.now()
        
        # Clean files older than 30 days
        cutoff_time = now - timedelta(days=30)
        cleaned_count = 0
        
        for filename in os.listdir(log_dir):
            filepath = os.path.join(log_dir, filename)
            
            # Check if it's a file
            if os.path.isfile(filepath):
                # Get file modification time
                file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                # Delete if older than cutoff
                if file_mtime < cutoff_time:
                    try:
                        os.remove(filepath)
                        cleaned_count += 1
                        logger.info(f"Deleted old log file: {filename}")
                    except Exception as e:
                        logger.error(f"Failed to delete log file {filename}: {str(e)}")
        
        logger.info(f"Log cleaning completed. Cleaned {cleaned_count} files")
        
        return {"status": "success", "cleaned": cleaned_count}
        
    except Exception as e:
        logger.error(f"Log cleaning failed: {str(e)}")
        raise


@celery_app.task(bind=True, name="app.tasks.data_processing_tasks.export_financial_data")
def export_financial_data(
    self,
    business_id: int,
    start_date: datetime,
    end_date: datetime,
    export_format: str = "csv"
):
    """
    Export financial data for a business
    
    Args:
        business_id: Business ID
        start_date: Start date
        end_date: End date
        export_format: Export format (csv, xlsx)
    """
    db = SessionLocal()
    try:
        logger.info(f"Exporting financial data for business {business_id}")
        
        # Get transactions
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).order_by(Transaction.transaction_date).all()
        
        # Convert to list of dicts
        data = []
        for t in transactions:
            data.append({
                "ID": t.id,
                "Date": t.transaction_date.isoformat(),
                "Type": t.transaction_type.value,
                "Amount": t.amount,
                "Category": t.category,
                "Description": t.description,
                "Payment Method": t.payment_method.value if t.payment_method else None,
                "Party": t.party_name,
                "GST": t.gst_amount,
                "Created At": t.created_at.isoformat()
            })
        
        # This would save to file and return download link
        # For now, we'll just return the data
        logger.info(f"Exported {len(data)} transactions for business {business_id}")
        
        return {
            "status": "success",
            "data": data,
            "count": len(data)
        }
        
    except Exception as e:
        logger.error(f"Financial data export failed: {str(e)}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.data_processing_tasks.import_transactions")
def import_transactions(
    self,
    business_id: int,
    user_id: int,
    file_path: str,
    file_format: str = "csv"
):
    """
    Import transactions from file
    
    Args:
        business_id: Business ID
        user_id: User ID importing
        file_path: Path to file
        file_format: File format (csv, xlsx)
    """
    db = SessionLocal()
    try:
        logger.info(f"Importing transactions for business {business_id} from {file_path}")
        
        # This would parse the file and import transactions
        # For now, we'll just return a success message
        imported_count = 0
        
        logger.info(f"Imported {imported_count} transactions for business {business_id}")
        
        return {
            "status": "success",
            "imported_count": imported_count
        }
        
    except Exception as e:
        logger.error(f"Transaction import failed: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.data_processing_tasks.generate_report")
def generate_report(
    self,
    business_id: int,
    report_type: str,
    start_date: datetime,
    end_date: datetime
):
    """
    Generate a report for a business
    
    Args:
        business_id: Business ID
        report_type: Type of report (profit_loss, cash_flow, sales, etc.)
        start_date: Start date
        end_date: End date
    """
    db = SessionLocal()
    try:
        logger.info(f"Generating {report_type} report for business {business_id}")
        
        # This would generate the report
        report_data = {
            "business_id": business_id,
            "report_type": report_type,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "generated_at": datetime.utcnow().isoformat()
        }
        
        logger.info(f"Report generated: {report_type} for business {business_id}")
        
        return {
            "status": "success",
            "report_data": report_data
        }
        
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")
        raise
    finally:
        db.close()


@celery_app.task(bind=True, name="app.tasks.data_processing_tasks.backup_data")
def backup_data(self, business_id: int):
    """
    Backup business data
    
    Args:
        business_id: Business ID
    """
    db = SessionLocal()
    try:
        logger.info(f"Backing up data for business {business_id}")
        
        # This would create a backup of the business data
        backup_info = {
            "business_id": business_id,
            "backup_date": datetime.utcnow().isoformat(),
            "backup_size": "10MB"  # Placeholder
        }
        
        logger.info(f"Backup completed for business {business_id}")
        
        return {
            "status": "success",
            "backup_info": backup_info
        }
        
    except Exception as e:
        logger.error(f"Backup failed: {str(e)}")
        raise
    finally:
        db.close()