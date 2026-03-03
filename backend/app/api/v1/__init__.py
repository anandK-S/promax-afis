# ========================================
# Pro-Max AFIS - API v1 Router
# ========================================
# Main API router for version 1 endpoints
# Author: Pro-Max Development Team

from fastapi import APIRouter
from .endpoints import auth, financials, inventory, ml, websocket

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    financials.router,
    prefix="/financials",
    tags=["Financials"]
)

api_router.include_router(
    inventory.router,
    prefix="/inventory",
    tags=["Inventory"]
)

api_router.include_router(
    ml.router,
    prefix="/ml",
    tags=["Machine Learning"]
)

api_router.include_router(
    websocket.router,
    prefix="/websocket",
    tags=["WebSocket"]
)