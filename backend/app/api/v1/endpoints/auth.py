# ========================================
# Pro-Max AFIS - Authentication Endpoints
# ========================================
# JWT-based authentication with OAuth2 support
# Author: Pro-Max Development Team

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import logging

from app.core.config import settings
from app.core.database import get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    verify_token
)
from app.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse
)
from app.models.user import User
from app.models.business import Business

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")


# ========================================
# Helper Functions
# ========================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Args:
        token: JWT access token
        db: Database session
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


# ========================================
# Endpoints
# ========================================

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user account
    
    Creates a new user account and automatically creates a business profile.
    Password is securely hashed using Argon2.
    
    - **email**: Unique email address
    - **password**: Strong password (min 12 characters)
    - **first_name**: User's first name
    - **last_name**: User's last name
    - **phone**: Phone number (optional)
    """
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check phone number uniqueness if provided
    if user_data.phone:
        existing_phone = db.query(User).filter(User.phone == user_data.phone).first()
        if existing_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number already registered"
            )
    
    try:
        # Hash password
        hashed_password = get_password_hash(user_data.password)
        
        # Create user
        user = User(
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone=user_data.phone,
            role="admin"  # First user is admin
        )
        
        db.add(user)
        db.flush()  # Get user ID without committing
        
        # Create business profile for user
        business = Business(
            user_id=user.id,
            business_name=f"{user_data.first_name}'s Business",
            currency=settings.currency,
            timezone=settings.timezone,
            language=settings.locale
        )
        
        db.add(business)
        db.commit()
        db.refresh(user)
        db.refresh(business)
        
        logger.info(f"New user registered: {user.email}")
        
        return user
        
    except Exception as e:
        db.rollback()
        logger.error(f"Registration failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticate user and generate JWT tokens
    
    Returns access token and refresh token for authentication.
    Access token expires in 30 minutes, refresh token in 7 days.
    
    - **username**: User's email address
    - **password**: User's password
    """
    
    # Find user by email
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact support."
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Generate tokens
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )
    
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    logger.info(f"User logged in: {user.email}")
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user,
        "business": user.business
    }


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    Use this endpoint to get a new access token when the current one expires.
    The refresh token is also rotated for security.
    
    - **refresh_token**: Valid refresh token from login
    """
    
    try:
        # Verify refresh token
        payload = verify_token(refresh_token)
        user_id: str = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Generate new tokens
        new_access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email, "role": user.role}
        )
        
        new_refresh_token = create_refresh_token(
            data={"sub": str(user.id)}
        )
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "user": user,
            "business": user.business
        }
        
    except Exception as e:
        logger.error(f"Token refresh failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information
    
    Returns the authenticated user's profile information.
    Requires valid JWT access token.
    """
    
    return current_user


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout user (invalidate tokens on client)
    
    Note: In a production environment, you may want to implement
    token blacklisting in Redis for proper token invalidation.
    """
    
    logger.info(f"User logged out: {current_user.email}")
    
    return {
        "message": "Logged out successfully",
        "detail": "Please clear tokens from client storage"
    }


@router.get("/verify-token")
async def verify_token_endpoint(
    current_user: User = Depends(get_current_user)
):
    """
    Verify if current access token is valid
    
    Returns user information if token is valid.
    """
    
    return {
        "valid": True,
        "user": current_user,
        "business": current_user.business
    }