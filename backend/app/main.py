# ========================================
# Pro-Max AFIS - Main FastAPI Application
# ========================================
# Application entry point with middleware setup
# Author: Pro-Max Development Team

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
import logging
import time
from typing import Dict

from app.core.config import settings
from app.core.database import init_db
from app.api.v1 import api_router

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file_path),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler
    Manages startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    
    # Initialize database
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
    
    # Yield to application
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Autonomous Financial Intelligence System for MSMEs",
    version=settings.app_version,
    docs_url="/api/docs" if settings.api_docs_enabled else None,
    redoc_url="/api/redoc" if settings.api_redoc_enabled else None,
    openapi_url="/api/openapi.json" if settings.api_docs_enabled else None,
    lifespan=lifespan
)


# ========================================
# Middleware Configuration
# ========================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# GZip Compression Middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Request Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Add processing time to response headers
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Custom Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions
    """
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


# ========================================
# Static Files
# ========================================

# Mount static files directory
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    logger.warning("Static files directory not found")


# ========================================
# API Routes
# ========================================

# Health Check Endpoint
@app.get("/api/v1/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }


# Include API router
app.include_router(api_router, prefix=settings.api_prefix)


# ========================================
# Custom OpenAPI Schema
# ========================================

def custom_openapi() -> Dict:
    """
    Custom OpenAPI schema with additional information
    """
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        ## Pro-Max Autonomous Financial Intelligence System
        
        An enterprise-grade AI-powered financial management platform for MSMEs.
        
        ### Features
        - Real-time financial monitoring
        - AI-powered sales forecasting
        - Voice-based insights (10+ languages)
        - Autonomous alerts and recommendations
        - Scenario simulation and what-if analysis
        
        ### Authentication
        Most endpoints require JWT authentication. Use `/api/v1/auth/login` to obtain tokens.
        
        ### Rate Limiting
        API requests are rate-limited to ensure fair usage.
        
        ### Support
        For support: support@promax-afis.com
        """,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    
    # Add security to all routes (except auth)
    for path, path_item in openapi_schema["paths"].items():
        for method in path_item.values():
            if "security" not in method and "/auth" not in path:
                method.setdefault("security", []).append({"bearerAuth": []})
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# ========================================
# Startup Message
# ========================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting {settings.app_name} server...")
    logger.info(f"API Documentation: http://localhost:8000/api/docs")
    logger.info(f"ReDoc Documentation: http://localhost:8000/api/redoc")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )