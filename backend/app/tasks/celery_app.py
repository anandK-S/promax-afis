# ========================================
# Pro-Max AFIS - Celery Application Setup
# ========================================
# Celery configuration and task registration
# Author: Pro-Max Development Team

from celery import Celery
from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "promax_afis",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.tasks.ml_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.data_processing_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task settings
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.timezone,
    enable_utc=True,
    
    # Task execution
    task_time_limit=settings.celery_task_time_limit,
    task_soft_time_limit=settings.celery_task_soft_time_limit,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    
    # Result backend
    result_expires=3600,  # 1 hour
    
    # Task routing
    task_routes={
        "app.tasks.ml_tasks.*": {"queue": "ml"},
        "app.tasks.notification_tasks.*": {"queue": "notifications"},
        "app.tasks.data_processing_tasks.*": {"queue": "data_processing"},
    },
    
    # Beat scheduler (for periodic tasks)
    beat_schedule={
        # Retrain ML models daily at 2 AM
        "retrain-ml-models": {
            "task": "app.tasks.ml_tasks.retrain_models",
            "schedule": settings.ml_retraining_schedule,
        },
        # Generate financial health scores every 6 hours
        "generate-health-scores": {
            "task": "app.tasks.ml_tasks.generate_health_scores",
            "schedule": "0 */6 * * *",
        },
        # Check for low stock alerts every hour
        "check-low-stock": {
            "task": "app.tasks.data_processing_tasks.check_low_stock",
            "schedule": "0 * * * *",
        },
        # Clean old logs daily at 3 AM
        "clean-logs": {
            "task": "app.tasks.data_processing_tasks.clean_old_logs",
            "schedule": "0 3 * * *",
        },
    },
)

# Optional: Use sentry for error tracking
if settings.environment == "production":
    celery_app.conf.update(
        worker_send_task_events=True,
        task_send_sent_event=True,
    )

if __name__ == "__main__":
    celery_app.start()