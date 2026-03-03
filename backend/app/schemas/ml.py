# ========================================
# Pro-Max AFIS - Machine Learning Schemas
# ========================================
# Pydantic schemas for ML/AI validation
# Author: Pro-Max Development Team

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class ModelType(str, Enum):
    """ML model types"""
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"
    PROPHET = "prophet"
    ENSEMBLE = "ensemble"
    CUSTOM = "custom"


class ForecastRequest(BaseModel):
    """Schema for sales forecast request"""
    horizon_days: int = Field(default=30, ge=1, le=365, description="Forecast horizon in days")
    include_confidence_interval: bool = Field(default=True, description="Include confidence intervals")
    include_seasonality: bool = Field(default=True, description="Include seasonal factors")
    model_type: ModelType = Field(default=ModelType.ENSEMBLE, description="Model to use")


class ForecastResponse(BaseModel):
    """Schema for forecast response"""
    forecast_id: str
    forecast_type: str
    model_type: str
    forecast_horizon_days: int
    forecast_start_date: datetime
    forecast_end_date: datetime
    confidence_level: Optional[float]
    
    # Results
    forecast_data: List[Dict[str, Any]]
    total_forecast: float
    average_daily_forecast: float
    growth_rate: float
    peak_day: Optional[Dict[str, Any]]
    lowest_day: Optional[Dict[str, Any]]
    
    # Confidence Intervals
    confidence_intervals: Optional[List[Dict[str, Any]]]
    
    # Seasonal Factors
    seasonal_factors: Optional[Dict[str, Any]]
    
    # Inventory Suggestions
    inventory_suggestions: Optional[List[Dict[str, Any]]]
    
    # Model Performance
    model_accuracy: Optional[float]
    mean_absolute_error: Optional[float]
    
    generated_at: datetime


class HealthScoreResponse(BaseModel):
    """Schema for financial health score response"""
    score_id: str
    business_id: int
    
    # Overall Score
    overall_score: float
    category: str  # Excellent, Good, Fair, Poor, Critical
    
    # Component Scores
    cash_position_score: Dict[str, Any]
    profitability_score: Dict[str, Any]
    solvency_score: Dict[str, Any]
    efficiency_score: Dict[str, Any]
    growth_score: Dict[str, Any]
    
    # Recommendations
    recommendations: List[str]
    priority_actions: List[Dict[str, Any]]
    
    # Trends
    score_trend: Optional[List[Dict[str, Any]]]
    
    calculated_at: datetime


class AgentChatRequest(BaseModel):
    """Schema for AI agent chat request"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    language: str = Field(default="en", description="Language code (en, hi, gu, mr, etc.)")
    message_type: str = Field(default="text", description="Message type (text or voice)")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class AgentChatResponse(BaseModel):
    """Schema for AI agent chat response"""
    conversation_id: str
    response: Dict[str, Any]
    intent_detected: str
    entities_extracted: Dict[str, Any]
    confidence: Optional[float]
    action_buttons: List[Dict[str, Any]]
    timestamp: datetime


class VoiceInsightRequest(BaseModel):
    """Schema for voice-based insight request"""
    audio_data: str = Field(..., description="Base64 encoded audio data")
    language: str = Field(default="en", description="Language code")
    audio_format: str = Field(default="webm", description="Audio format (webm, mp3, wav)")


class VoiceInsightResponse(BaseModel):
    """Schema for voice-based insight response"""
    transcription: Dict[str, Any]
    insight: Dict[str, Any]
    audio_response: Optional[Dict[str, Any]]
    confidence: Optional[float]
    timestamp: datetime


class CategorizeRequest(BaseModel):
    """Schema for transaction categorization request"""
    description: str = Field(..., min_length=1, max_length=500, description="Transaction description")
    transaction_type: str = Field(default="expense", description="Transaction type")
    amount: Optional[float] = Field(None, gt=0, description="Transaction amount")


class CategorizeResponse(BaseModel):
    """Schema for categorization response"""
    category: str
    subcategory: Optional[str]
    confidence: float
    suggested_tags: List[str]
    reasoning: Optional[str]


class AnomalyResponse(BaseModel):
    """Schema for anomaly detection response"""
    anomalies: List[Dict[str, Any]]
    total_anomalies: int
    severity_breakdown: Dict[str, int]
    time_range: Dict[str, datetime]
    recommendations: List[str]
    detected_at: datetime


class RecommendationResponse(BaseModel):
    """Schema for AI recommendations response"""
    recommendations: List[Dict[str, Any]]
    total_recommendations: int
    priority: str  # high, medium, low
    category: str  # inventory, financial, operational
    generated_at: datetime


class SimulationRequest(BaseModel):
    """Schema for scenario simulation request"""
    scenario_type: str = Field(..., description="Type of simulation (price_change, market_crash, etc.)")
    parameters: Dict[str, Any] = Field(..., description="Simulation parameters")
    duration_days: int = Field(default=30, ge=1, le=365, description="Simulation duration")


class SimulationResponse(BaseModel):
    """Schema for simulation response"""
    simulation_id: str
    scenario_type: str
    parameters: Dict[str, Any]
    
    # Results
    projected_revenue: float
    projected_expenses: float
    projected_profit: float
    profit_change_percentage: float
    
    # Impact Analysis
    revenue_impact: float
    expense_impact: float
    cash_flow_impact: float
    
    # Risk Assessment
    risk_level: str
    risk_factors: List[str]
    mitigation_strategies: List[str]
    
    # Timeline
    projection_data: List[Dict[str, Any]]
    
    simulated_at: datetime


class TrainingDataRequest(BaseModel):
    """Schema for ML model training request"""
    model_type: ModelType
    training_data_start_date: datetime
    training_data_end_date: datetime
    hyperparameters: Optional[Dict[str, Any]] = None


class TrainingResponse(BaseModel):
    """Schema for ML model training response"""
    training_id: str
    model_type: str
    model_version: str
    status: str  # training, completed, failed
    
    # Training Metrics
    training_samples: int
    validation_samples: int
    training_time_seconds: float
    
    # Model Performance
    accuracy: Optional[float]
    mean_absolute_error: Optional[float]
    root_mean_squared_error: Optional[float]
    
    # Model Info
    model_path: Optional[str]
    hyperparameters: Dict[str, Any]
    
    started_at: datetime
    completed_at: Optional[datetime]