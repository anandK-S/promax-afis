# ========================================
# Pro-Max AFIS - Database Models
# ========================================
# Import all models for easy access
# Author: Pro-Max Development Team

from app.models.user import User
from app.models.business import Business
from app.models.financial import Transaction, Category
from app.models.inventory import Product, InventoryMovement, LowStockAlert
from app.models.ml_predictions import MLPrediction, AnomalyDetection

__all__ = [
    "User",
    "Business",
    "Transaction",
    "Category",
    "Product",
    "InventoryMovement",
    "LowStockAlert",
    "MLPrediction",
    "AnomalyDetection"
]