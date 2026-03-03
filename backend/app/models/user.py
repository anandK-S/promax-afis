# ========================================
# Pro-Max AFIS - User Model
# ========================================
# User account and authentication model
# Author: Pro-Max Development Team

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class UserRole(enum.Enum):
    """User roles for access control"""
    ADMIN = "admin"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"
    VIEWER = "viewer"


class User(Base):
    """
    User model for authentication and authorization
    """
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=True, index=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Role & Permissions
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Foreign Keys
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    business = relationship("Business", back_populates="users", lazy="select")
    created_transactions = relationship(
        "Transaction",
        foreign_keys="Transaction.created_by",
        back_populates="creator",
        lazy="dynamic"
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role={self.role.value})>"
    
    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def has_permission(self, required_role: UserRole) -> bool:
        """
        Check if user has required permission
        
        Args:
            required_role: Required role level
            
        Returns:
            True if user has sufficient permissions
        """
        role_hierarchy = {
            UserRole.VIEWER: 1,
            UserRole.ACCOUNTANT: 2,
            UserRole.MANAGER: 3,
            UserRole.ADMIN: 4
        }
        
        return role_hierarchy.get(self.role, 0) >= role_hierarchy.get(required_role, 0)