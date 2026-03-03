# ========================================
# Pro-Max AFIS - Inventory Models
# ========================================
# Product, inventory movement, and alert models
# Author: Pro-Max Development Team

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class MovementType(enum.Enum):
    """Inventory movement types"""
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    DAMAGE = "damage"
    TRANSFER = "transfer"


class Product(Base):
    """
    Product model for inventory management
    """
    
    __tablename__ = "products"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Business Foreign Key
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Product Information
    product_name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, nullable=True, index=True)
    barcode = Column(String(100), unique=True, nullable=True, index=True)
    
    # Categorization
    category = Column(String(100), nullable=True, index=True)
    subcategory = Column(String(100), nullable=True)
    brand = Column(String(100), nullable=True)
    
    # Pricing
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    margin_percentage = Column(Float, nullable=True)
    
    # Unit & Dimensions
    unit = Column(String(20), default="pcs", nullable=False)
    length = Column(Float, nullable=True)
    width = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    
    # Stock Levels
    current_stock = Column(Float, default=0.0, nullable=False)
    minimum_stock_level = Column(Float, default=10.0, nullable=False)
    maximum_stock_level = Column(Float, default=100.0, nullable=False)
    reorder_point = Column(Float, default=20.0, nullable=False)
    reorder_quantity = Column(Float, default=50.0, nullable=False)
    
    # Tax Information
    gst_rate = Column(Float, default=0.0, nullable=False)
    hsn_code = Column(String(20), nullable=True)
    gst_applicable = Column(Boolean, default=True, nullable=False)
    
    # Product Details
    description = Column(Text, nullable=True)
    specifications = Column(JSON, nullable=True)  # Key-value pairs
    manufacturer = Column(String(255), nullable=True)
    country_of_origin = Column(String(100), nullable=True)
    
    # Images
    image_urls = Column(JSON, nullable=True)  # List of image URLs
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_discontinued = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="products", lazy="select")
    movements = relationship("InventoryMovement", back_populates="product", lazy="dynamic", cascade="all, delete-orphan")
    low_stock_alerts = relationship("LowStockAlert", back_populates="product", lazy="dynamic", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.product_name}', stock={self.current_stock})>"
    
    @property
    def is_low_stock(self):
        """Check if product is low on stock"""
        return self.current_stock <= self.reorder_point
    
    @property
    def stock_status(self):
        """Get stock status"""
        if self.current_stock <= 0:
            return "out_of_stock"
        elif self.current_stock <= self.reorder_point:
            return "low_stock"
        elif self.current_stock >= self.maximum_stock_level:
            return "overstocked"
        else:
            return "in_stock"


class InventoryMovement(Base):
    """
    Inventory movement model for tracking stock changes
    """
    
    __tablename__ = "inventory_movements"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Product Foreign Key
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    # Movement Details
    movement_type = Column(Enum(MovementType), nullable=False, index=True)
    quantity = Column(Float, nullable=False)
    
    # Financial Details
    unit_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)
    
    # Reference Information
    reference_type = Column(String(50), nullable=True)  # invoice, receipt, etc.
    reference_id = Column(Integer, nullable=True)
    reference_number = Column(String(100), nullable=True)
    
    # Additional Information
    notes = Column(Text, nullable=True)
    reason = Column(String(255), nullable=True)
    
    # Location
    from_location = Column(String(100), nullable=True)
    to_location = Column(String(100), nullable=True)
    
    # Audit
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    movement_date = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="movements", lazy="select")
    
    def __repr__(self):
        return f"<InventoryMovement(id={self.id}, type={self.movement_type.value}, quantity={self.quantity})>"


class LowStockAlert(Base):
    """
    Low stock alert model for inventory notifications
    """
    
    __tablename__ = "low_stock_alerts"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Product Foreign Key
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    
    # Business Foreign Key
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Alert Details
    current_stock = Column(Float, nullable=False)
    reorder_point = Column(Float, nullable=False)
    shortage_quantity = Column(Float, nullable=False)
    
    # Severity
    severity = Column(String(20), default="medium", nullable=False)  # low, medium, high, critical
    
    # Notification
    is_notified = Column(Boolean, default=False, nullable=False)
    notified_at = Column(DateTime(timezone=True), nullable=True)
    
    # Resolution
    is_resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    product = relationship("Product", back_populates="low_stock_alerts", lazy="select")
    
    def __repr__(self):
        return f"<LowStockAlert(id={self.id}, product_id={self.product_id}, severity={self.severity})>"