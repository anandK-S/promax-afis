# ========================================
# Pro-Max AFIS - Inventory Schemas
# ========================================
# Pydantic schemas for inventory data validation
# Author: Pro-Max Development Team

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class MovementType(str, Enum):
    """Inventory movement types"""
    PURCHASE = "purchase"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"
    DAMAGE = "damage"
    TRANSFER = "transfer"


class ProductCreate(BaseModel):
    """Schema for creating a product"""
    product_name: str = Field(..., min_length=2, max_length=255, description="Product name")
    sku: Optional[str] = Field(None, max_length=100, description="Stock keeping unit")
    barcode: Optional[str] = Field(None, max_length=100, description="Product barcode")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    subcategory: Optional[str] = Field(None, max_length=100, description="Product subcategory")
    brand: Optional[str] = Field(None, max_length=100, description="Product brand")
    cost_price: float = Field(..., gt=0, description="Purchase cost price")
    selling_price: float = Field(..., gt=0, description="Selling price")
    unit: str = Field(default="pcs", max_length=20, description="Unit of measurement")
    length: Optional[float] = Field(None, gt=0, description="Length in cm")
    width: Optional[float] = Field(None, gt=0, description="Width in cm")
    height: Optional[float] = Field(None, gt=0, description="Height in cm")
    weight: Optional[float] = Field(None, gt=0, description="Weight in kg")
    current_stock: Optional[float] = Field(0, ge=0, description="Initial stock quantity")
    minimum_stock_level: float = Field(default=10, ge=0, description="Minimum stock level")
    maximum_stock_level: float = Field(default=100, ge=0, description="Maximum stock level")
    reorder_point: float = Field(default=20, ge=0, description="Reorder point")
    reorder_quantity: float = Field(default=50, gt=0, description="Reorder quantity")
    gst_rate: float = Field(default=0.0, ge=0, le=100, description="GST rate percentage")
    hsn_code: Optional[str] = Field(None, max_length=20, description="HSN code")
    gst_applicable: bool = Field(default=True, description="Whether GST is applicable")
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    specifications: Optional[Dict[str, Any]] = Field(None, description="Product specifications")
    manufacturer: Optional[str] = Field(None, max_length=255, description="Manufacturer name")
    country_of_origin: Optional[str] = Field(None, max_length=100, description="Country of origin")
    image_urls: Optional[List[str]] = Field(None, description="List of image URLs")
    
    @validator('selling_price')
    def selling_price_must_be_greater_than_cost(cls, v, values):
        """Validate that selling price is greater than cost price"""
        if 'cost_price' in values and v <= values['cost_price']:
            raise ValueError('Selling price must be greater than cost price')
        return v


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    product_name: Optional[str] = Field(None, min_length=2, max_length=255)
    sku: Optional[str] = Field(None, max_length=100)
    barcode: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    brand: Optional[str] = Field(None, max_length=100)
    cost_price: Optional[float] = Field(None, gt=0)
    selling_price: Optional[float] = Field(None, gt=0)
    unit: Optional[str] = Field(None, max_length=20)
    length: Optional[float] = Field(None, gt=0)
    width: Optional[float] = Field(None, gt=0)
    height: Optional[float] = Field(None, gt=0)
    weight: Optional[float] = Field(None, gt=0)
    minimum_stock_level: Optional[float] = Field(None, ge=0)
    maximum_stock_level: Optional[float] = Field(None, ge=0)
    reorder_point: Optional[float] = Field(None, ge=0)
    reorder_quantity: Optional[float] = Field(None, gt=0)
    gst_rate: Optional[float] = Field(None, ge=0, le=100)
    hsn_code: Optional[str] = Field(None, max_length=20)
    gst_applicable: Optional[bool] = None
    description: Optional[str] = Field(None, max_length=1000)
    specifications: Optional[Dict[str, Any]] = None
    manufacturer: Optional[str] = Field(None, max_length=255)
    country_of_origin: Optional[str] = Field(None, max_length=100)
    image_urls: Optional[List[str]] = None
    is_active: Optional[bool] = None
    is_discontinued: Optional[bool] = None


class ProductResponse(BaseModel):
    """Schema for product response"""
    id: int
    business_id: int
    product_name: str
    sku: Optional[str]
    barcode: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    brand: Optional[str]
    cost_price: float
    selling_price: float
    margin_percentage: Optional[float]
    unit: str
    length: Optional[float]
    width: Optional[float]
    height: Optional[float]
    weight: Optional[float]
    current_stock: float
    minimum_stock_level: float
    maximum_stock_level: float
    reorder_point: float
    reorder_quantity: float
    gst_rate: float
    hsn_code: Optional[str]
    gst_applicable: bool
    description: Optional[str]
    specifications: Optional[Dict[str, Any]]
    manufacturer: Optional[str]
    country_of_origin: Optional[str]
    image_urls: Optional[List[str]]
    is_active: bool
    is_discontinued: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    
    @property
    def is_low_stock(self) -> bool:
        """Check if product is low on stock"""
        return self.current_stock <= self.reorder_point
    
    @property
    def stock_status(self) -> str:
        """Get stock status"""
        if self.current_stock <= 0:
            return "out_of_stock"
        elif self.current_stock <= self.reorder_point:
            return "low_stock"
        elif self.current_stock >= self.maximum_stock_level:
            return "overstocked"
        else:
            return "in_stock"


class ProductListResponse(BaseModel):
    """Schema for paginated product list"""
    items: List[ProductResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class InventoryMovementCreate(BaseModel):
    """Schema for creating inventory movement"""
    product_id: int = Field(..., description="Product ID")
    movement_type: MovementType = Field(..., description="Movement type")
    quantity: float = Field(..., gt=0, description="Quantity moved")
    unit_cost: Optional[float] = Field(None, ge=0, description="Unit cost")
    total_cost: Optional[float] = Field(None, ge=0, description="Total cost")
    reference_type: Optional[str] = Field(None, max_length=50, description="Reference type")
    reference_id: Optional[int] = Field(None, description="Reference ID")
    reference_number: Optional[str] = Field(None, max_length=100, description="Reference number")
    notes: Optional[str] = Field(None, description="Additional notes")
    reason: Optional[str] = Field(None, max_length=255, description="Reason for movement")
    from_location: Optional[str] = Field(None, max_length=100, description="From location")
    to_location: Optional[str] = Field(None, max_length=100, description="To location")
    movement_date: Optional[datetime] = Field(None, description="Movement date")


class InventoryMovementResponse(BaseModel):
    """Schema for inventory movement response"""
    id: int
    product_id: int
    movement_type: str
    quantity: float
    unit_cost: Optional[float]
    total_cost: Optional[float]
    reference_type: Optional[str]
    reference_id: Optional[int]
    reference_number: Optional[str]
    notes: Optional[str]
    reason: Optional[str]
    from_location: Optional[str]
    to_location: Optional[str]
    created_by: int
    movement_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class LowStockAlertResponse(BaseModel):
    """Schema for low stock alert response"""
    id: int
    product_id: int
    business_id: int
    current_stock: float
    reorder_point: float
    shortage_quantity: float
    severity: str
    is_notified: bool
    notified_at: Optional[datetime]
    is_resolved: bool
    resolved_at: Optional[datetime]
    resolved_by: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class InventorySummary(BaseModel):
    """Schema for inventory summary"""
    total_products: int
    active_products: int
    inactive_products: int
    total_stock_value: float
    total_cost_value: float
    potential_revenue: float
    
    # Stock Status
    in_stock_count: int
    low_stock_count: int
    out_of_stock_count: int
    overstocked_count: int
    
    # Categories
    products_by_category: Dict[str, int]
    stock_value_by_category: Dict[str, float]
    
    # Alerts
    low_stock_alerts_count: int
    critical_low_stock_count: int
    
    # Movements
    recent_movements: List[InventoryMovementResponse]
    total_movements_this_month: int