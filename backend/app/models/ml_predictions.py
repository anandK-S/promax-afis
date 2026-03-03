# ========================================
# Pro-Max AFIS - ML Predictions Model
# ========================================
# ML prediction and anomaly detection models
# Author: Pro-Max Development Team

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class PredictionType(enum.Enum):
    """ML prediction types"""
    SALES_FORECAST = "sales_forecast"
    CASH_FLOW_FORECAST = "cash_flow_forecast"
    DEMAND_FORECAST = "demand_forecast"
    INVENTORY_OPTIMIZATION = "inventory_optimization"
    RECOMMENDATION = "recommendation"


class ModelType(enum.Enum):
    """ML model types"""
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    PROPHET = "prophet"
    ENSEMBLE = "ensemble"
    CUSTOM = "custom"


class AnomalyType(enum.Enum):
    """Anomaly types"""
    UNUSUAL_EXPENSE = "unusual_expense"
    UNUSUAL_INCOME = "unusual_income"
    SPIKE_IN_SALES = "spike_in_sales"
    DROP_IN_SALES = "drop_in_sales"
    UNUSUAL_INVENTORY = "unusual_inventory"
    POTENTIAL_FRAUD = "potential_fraud"


class MLPrediction(Base):
    """
    ML prediction model for storing forecast results
    """
    
    __tablename__ = "ml_predictions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Business Foreign Key
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Prediction Details
    prediction_type = Column(Enum(PredictionType), nullable=False, index=True)
    model_type = Column(Enum(ModelType), nullable=False)
    model_version = Column(String(50), nullable=True)
    
    # Input Parameters
    input_parameters = Column(JSON, nullable=True)  # Training data parameters
    
    # Prediction Results
    prediction_results = Column(JSON, nullable=False)  # Main results
    confidence_score = Column(Float, nullable=True)
    prediction_horizon_days = Column(Integer, nullable=True)
    
    # Additional Metrics
    accuracy_score = Column(Float, nullable=True)
    mean_absolute_error = Column(Float, nullable=True)
    mean_squared_error = Column(Float, nullable=True)
    
    # Seasonal Factors
    seasonal_factors = Column(JSON, nullable=True)
    trend_analysis = Column(JSON, nullable=True)
    
    # Recommendations
    recommendations = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    prediction_date = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<MLPrediction(id={self.id}, type={self.prediction_type.value}, date={self.prediction_date})>"
    
    @property
    def prediction_summary(self):
        """Get summary of prediction"""
        if not self.prediction_results:
            return None
        
        results = self.prediction_results
        
        return {
            "type": self.prediction_type.value,
            "model": self.model_type.value,
            "date": self.prediction_date.isoformat(),
            "horizon": self.prediction_horizon_days,
            "confidence": self.confidence_score,
            "total_forecast": results.get("total_forecast"),
            "growth_rate": results.get("growth_rate")
        }


class AnomalyDetection(Base):
    """
    Anomaly detection model for identifying unusual patterns
    """
    
    __tablename__ = "anomaly_detections"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Business Foreign Key
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Anomaly Details
    anomaly_type = Column(Enum(AnomalyType), nullable=False, index=True)
    severity = Column(String(20), nullable=False)  # low, medium, high, critical
    
    # Reference Information
    reference_type = Column(String(50), nullable=True)  # transaction, inventory, etc.
    reference_id = Column(Integer, nullable=True)
    
    # Anomaly Data
    anomaly_value = Column(Float, nullable=True)
    expected_value = Column(Float, nullable=True)
    deviation_percentage = Column(Float, nullable=True)
    
    # Time Window
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    
    # Description
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Root Cause Analysis
    root_cause = Column(Text, nullable=True)
    affected_entities = Column(JSON, nullable=True)  # List of affected items
    
    # Recommendations
    recommendations = Column(JSON, nullable=True)
    
    # Status
    is_resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # Notification
    is_notified = Column(Boolean, default=False, nullable=False)
    notified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    detected_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<AnomalyDetection(id={self.id}, type={self.anomaly_type.value}, severity={self.severity})>"
    
    @property
    def age_hours(self):
        """Get anomaly age in hours"""
        delta = datetime.utcnow() - self.detected_at
        return delta.total_seconds() / 3600
    
    @property
    def is_critical(self):
        """Check if anomaly is critical"""
        return self.severity in ["high", "critical"] and not self.is_resolved