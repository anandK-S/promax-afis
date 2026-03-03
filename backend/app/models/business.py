# ========================================
# Pro-Max AFIS - Business Model
# ========================================
# Business profile and settings model
# Author: Pro-Max Development Team

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Business(Base):
    """
    Business model for storing business profile and settings
    """
    
    __tablename__ = "businesses"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic Information
    business_name = Column(String(255), nullable=False, index=True)
    business_type = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    
    # Contact Information
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Address
    address_line_1 = Column(String(255), nullable=True)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), default="India")
    
    # Business Details
    gst_number = Column(String(20), unique=True, nullable=True, index=True)
    pan_number = Column(String(20), unique=True, nullable=True)
    tan_number = Column(String(20), unique=True, nullable=True)
    
    # Financial Settings
    currency = Column(String(10), default="INR", nullable=False)
    tax_rate = Column(Float, default=18.0, nullable=False)
    financial_year_start = Column(String(7), default="04-01", nullable=False)
    
    # Business Logic
    invoice_prefix = Column(String(10), default="INV", nullable=False)
    invoice_sequence = Column(Integer, default=1000, nullable=False)
    
    # Payment Settings
    upi_id = Column(String(100), nullable=True)
    bank_account_number = Column(String(50), nullable=True)
    bank_ifsc = Column(String(20), nullable=True)
    bank_name = Column(String(255), nullable=True)
    
    # Subscription & Limits
    subscription_plan = Column(String(50), default="free", nullable=False)
    max_users = Column(Integer, default=5, nullable=False)
    max_products = Column(Integer, default=100, nullable=False)
    
    # Settings
    timezone = Column(String(50), default="Asia/Kolkata", nullable=False)
    date_format = Column(String(20), default="DD-MM-YYYY", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    
    # Logo & Branding
    logo_url = Column(String(500), nullable=True)
    primary_color = Column(String(20), default="#3B82F6", nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="business", lazy="dynamic")
    transactions = relationship("Transaction", back_populates="business", lazy="dynamic")
    products = relationship("Product", back_populates="business", lazy="dynamic")
    
    def __repr__(self):
        return f"<Business(id={self.id}, name='{self.business_name}', gst='{self.gst_number}')>"
    
    @property
    def full_address(self):
        """Get full address as a string"""
        parts = [
            self.address_line_1,
            self.address_line_2,
            self.city,
            self.state,
            self.postal_code,
            self.country
        ]
        return ", ".join(filter(None, parts))
    
    def generate_invoice_number(self):
        """Generate next invoice number"""
        self.invoice_sequence += 1
        return f"{self.invoice_prefix}-{self.invoice_sequence}"