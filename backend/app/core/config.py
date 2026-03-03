# ========================================
# Pro-Max AFIS - Core Configuration
# ========================================
# Application configuration management
# Author: Pro-Max Development Team

from pydantic_settings import BaseSettings
from typing import Optional, List
from functools import lru_cache


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Application Information
    app_name: str = "Pro-Max AFIS"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    secret_key: str = "your-secret-key-change-this"
    
    # Database Configuration
    database_url: str = "postgresql://postgres:postgres@localhost:5432/promax_db"
    timescaledb_enabled: bool = True
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    redis_cache_url: str = "redis://localhost:6379/1"
    
    # Security & Authentication
    jwt_secret_key: str = "your-jwt-secret-key"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # Password Hashing
    password_hash_memory: int = 65536
    password_hash_time: int = 3
    password_hash_parallelism: int = 4
    password_hash_length: int = 32
    
    # OAuth2
    oauth2_client_id: str = ""
    oauth2_client_secret: str = ""
    oauth2_redirect_uri: str = "http://localhost:3000/auth/callback"
    oauth2_scopes: str = "openid profile email"
    
    # Email Configuration
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_use_tls: bool = True
    smtp_user: str = ""
    smtp_password: str = ""
    email_from: str = "noreply@promax-afis.com"
    email_from_name: str = "Pro-Max AFIS"
    
    # UPI Integration
    upi_api_key: str = ""
    upi_merchant_id: str = ""
    
    # GST Integration
    gst_api_key: str = ""
    gst_username: str = ""
    gst_password: str = ""
    gst_sandbox: bool = True
    
    # ML Models Configuration
    ml_model_path: str = "./ml-models/trained_models"
    ml_retraining_enabled: bool = True
    ml_retraining_schedule: str = "0 2 * * *"
    ml_model_version: str = "v1.0.0"
    
    # Voice Processing
    whisper_model_size: str = "base"
    whisper_language: str = "en"
    whisper_device: str = "cpu"
    
    # WhatsApp Integration
    whatsapp_api_key: str = ""
    whatsapp_phone_number_id: str = ""
    whatsapp_template_approved: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_file_path: str = "./logs/app.log"
    log_rotation: str = "10 MB"
    log_retention: str = "30 days"
    
    # Rate Limiting
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_period: int = 60
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    
    # API Configuration
    api_prefix: str = "/api/v1"
    api_docs_enabled: bool = True
    api_redoc_enabled: bool = True
    
    # WebSocket
    ws_heartbeat_interval: int = 30
    ws_max_connections: int = 1000
    
    # File Upload
    max_file_size: int = 10485760  # 10MB
    allowed_file_extensions: List[str] = [".csv", ".xlsx", ".xls", ".pdf", ".png", ".jpg", ".jpeg"]
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/2"
    celery_result_backend: str = "redis://localhost:6379/3"
    celery_task_time_limit: int = 300
    celery_task_soft_time_limit: int = 280
    
    # Feature Flags
    enable_voice_features: bool = True
    enable_ml_predictions: bool = True
    enable_auto_categorization: bool = True
    enable_anomaly_detection: bool = True
    enable_scenario_simulator: bool = True
    enable_real_time_alerts: bool = True
    
    # Timezone & Locale
    timezone: str = "Asia/Kolkata"
    locale: str = "en_IN"
    currency: str = "INR"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    """
    return Settings()


# Export settings instance
settings = get_settings()