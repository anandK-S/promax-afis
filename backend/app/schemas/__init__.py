# ========================================
# Pro-Max AFIS - Pydantic Schemas
# ========================================
# Import all schemas for easy access
# Author: Pro-Max Development Team

from app.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from app.schemas.financial import (
    TransactionCreate, TransactionUpdate, TransactionResponse,
    TransactionListResponse, FinancialSummary, ProfitLossStatement,
    CashFlowData, CategoryCreate, CategoryResponse
)
from app.schemas.inventory import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse,
    InventoryMovementCreate, InventoryMovementResponse,
    LowStockAlertResponse, InventorySummary
)
from app.schemas.ml import (
    ForecastRequest, ForecastResponse, HealthScoreResponse,
    AgentChatRequest, AgentChatResponse, VoiceInsightRequest,
    VoiceInsightResponse, CategorizeRequest, CategorizeResponse,
    AnomalyResponse, RecommendationResponse, SimulationRequest,
    SimulationResponse
)

__all__ = [
    "UserCreate",
    "UserLogin",
    "UserResponse",
    "TokenResponse",
    "TransactionCreate",
    "TransactionUpdate",
    "TransactionResponse",
    "TransactionListResponse",
    "FinancialSummary",
    "ProfitLossStatement",
    "CashFlowData",
    "CategoryCreate",
    "CategoryResponse",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse",
    "ProductListResponse",
    "InventoryMovementCreate",
    "InventoryMovementResponse",
    "LowStockAlertResponse",
    "InventorySummary",
    "ForecastRequest",
    "ForecastResponse",
    "HealthScoreResponse",
    "AgentChatRequest",
    "AgentChatResponse",
    "VoiceInsightRequest",
    "VoiceInsightResponse",
    "CategorizeRequest",
    "CategorizeResponse",
    "AnomalyResponse",
    "RecommendationResponse",
    "SimulationRequest",
    "SimulationResponse"
]