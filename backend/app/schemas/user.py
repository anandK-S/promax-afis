# ========================================
# Pro-Max AFIS - User Schemas
# ========================================
# Pydantic schemas for user validation
# Author: Pro-Max Development Team

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema"""
    first_name: str = Field(..., min_length=2, max_length=100, description="User's first name")
    last_name: str = Field(..., min_length=2, max_length=100, description="User's last name")
    phone: Optional[str] = Field(None, pattern=r'^[0-9]{10}$', description="10-digit phone number")


class UserCreate(UserBase):
    """Schema for user registration"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ...,
        min_length=12,
        max_length=128,
        description="Password (minimum 12 characters)"
    )
    
    @validator('password')
    def password_strength(cls, v):
        """Validate password strength"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str]
    avatar_url: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    business_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"


class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Seconds until expiry
    user: UserResponse


class TokenRefreshRequest(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str = Field(..., description="Refresh token")


class PasswordChangeRequest(BaseModel):
    """Schema for password change"""
    old_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ...,
        min_length=12,
        max_length=128,
        description="New password (minimum 12 characters)"
    )


class UserUpdate(BaseModel):
    """Schema for user profile update"""
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^[0-9]{10}$')
    avatar_url: Optional[str] = None