# ========================================
# Pro-Max AFIS - Inventory Endpoints
# ========================================
# Inventory management and stock tracking
# Author: Pro-Max Development Team

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import logging

from app.core.config import settings
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.inventory import Product, InventoryMovement, LowStockAlert
from app.schemas.inventory import (
    ProductCreate,
    ProductResponse,
    ProductListResponse,
    InventoryMovementCreate,
    InventoryMovementResponse,
    LowStockAlertResponse
)
from app.services.inventory_service import InventoryService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize inventory service
inventory_service = InventoryService()


# ========================================
# Product Endpoints
# ========================================

@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new product
    
    Add a new product to the inventory with stock management settings.
    
    - **product_name**: Name of the product
    - **sku**: Unique stock keeping unit (optional)
    - **category**: Product category
    - **cost_price**: Purchase cost price
    - **selling_price**: Selling price
    - **current_stock**: Initial stock quantity
    - **minimum_stock_level**: Reorder trigger level
    - **reorder_quantity**: Quantity to reorder
    """
    
    try:
        business_id = current_user.business.id
        
        # Check if SKU already exists
        if product_data.sku:
            existing_sku = db.query(Product).filter(
                Product.business_id == business_id,
                Product.sku == product_data.sku
            ).first()
            
            if existing_sku:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product with this SKU already exists"
                )
        
        # Create product
        product = Product(
            business_id=business_id,
            product_name=product_data.product_name,
            sku=product_data.sku,
            category=product_data.category,
            subcategory=product_data.subcategory,
            brand=product_data.brand,
            cost_price=product_data.cost_price,
            selling_price=product_data.selling_price,
            unit=product_data.unit,
            current_stock=product_data.current_stock or 0,
            minimum_stock_level=product_data.minimum_stock_level or 10,
            maximum_stock_level=product_data.maximum_stock_level or 100,
            reorder_point=product_data.reorder_point or 20,
            reorder_quantity=product_data.reorder_quantity or 50,
            barcode=product_data.barcode,
            gst_rate=product_data.gst_rate,
            hsn_code=product_data.hsn_code
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        # Create initial inventory movement if stock provided
        if product_data.current_stock and product_data.current_stock > 0:
            movement = InventoryMovement(
                product_id=product.id,
                movement_type="purchase",
                quantity=product_data.current_stock,
                unit_cost=product_data.cost_price,
                total_cost=product_data.cost_price * product_data.current_stock,
                notes="Initial stock entry",
                created_by=current_user.id
            )
            db.add(movement)
            db.commit()
        
        logger.info(f"Product created: {product.id} by {current_user.email}")
        
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Product creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product"
        )


@router.get("/products", response_model=ProductListResponse)
async def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in product name/SKU"),
    low_stock_only: bool = Query(False, description="Show only low stock products"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all products with filtering and pagination
    
    Retrieve paginated list of inventory products with optional filters.
    
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    - **category**: Filter by category
    - **search**: Search text in product name or SKU
    - **low_stock_only**: Show only products below minimum stock level
    """
    
    try:
        business_id = current_user.business.id
        
        # Build query
        query = db.query(Product).filter(
            Product.business_id == business_id,
            Product.is_active == True
        )
        
        # Apply filters
        if category:
            query = query.filter(Product.category == category)
        
        if search:
            query = query.filter(
                (Product.product_name.ilike(f"%{search}%")) |
                (Product.sku.ilike(f"%{search}%"))
            )
        
        if low_stock_only:
            query = query.filter(
                Product.current_stock <= Product.minimum_stock_level
            )
        
        # Order by product name
        query = query.order_by(Product.product_name)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        products = query.offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "products": products
        }
        
    except Exception as e:
        logger.error(f"Failed to get products: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve products"
        )


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get product by ID
    
    Retrieve details of a specific product.
    """
    
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.business_id == current_user.business.id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update product
    
    Update an existing product's details.
    """
    
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.business_id == current_user.business.id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    try:
        # Update product fields
        product.product_name = product_data.product_name
        product.sku = product_data.sku
        product.category = product_data.category
        product.subcategory = product_data.subcategory
        product.brand = product_data.brand
        product.cost_price = product_data.cost_price
        product.selling_price = product_data.selling_price
        product.unit = product_data.unit
        product.minimum_stock_level = product_data.minimum_stock_level
        product.maximum_stock_level = product_data.maximum_stock_level
        product.reorder_point = product_data.reorder_point
        product.reorder_quantity = product_data.reorder_quantity
        product.barcode = product_data.barcode
        product.gst_rate = product_data.gst_rate
        product.hsn_code = product_data.hsn_code
        
        db.commit()
        db.refresh(product)
        
        logger.info(f"Product updated: {product_id} by {current_user.email}")
        
        return product
        
    except Exception as e:
        db.rollback()
        logger.error(f"Product update failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product"
        )


@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete product (soft delete)
    
    Soft delete a product by marking it as inactive.
    """
    
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.business_id == current_user.business.id
    ).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    try:
        product.is_active = False
        db.commit()
        
        logger.info(f"Product soft deleted: {product_id} by {current_user.email}")
        
        return None
        
    except Exception as e:
        db.rollback()
        logger.error(f"Product deletion failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product"
        )


# ========================================
# Inventory Movement Endpoints
# ========================================

@router.post("/movements", response_model=InventoryMovementResponse, status_code=status.HTTP_201_CREATED)
async def create_inventory_movement(
    movement_data: InventoryMovementCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create inventory movement
    
    Record inventory movements such as purchases, sales, returns, adjustments, or losses.
    Automatically updates product stock levels.
    
    - **product_id**: ID of the product
    - **movement_type**: Type of movement (purchase, sale, return, adjustment, loss)
    - **quantity**: Quantity of movement
    - **notes**: Optional notes
    """
    
    try:
        business_id = current_user.business.id
        
        # Verify product exists and belongs to business
        product = db.query(Product).filter(
            Product.id == movement_data.product_id,
            Product.business_id == business_id
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )
        
        # Calculate total cost
        unit_cost = movement_data.unit_cost or product.cost_price
        total_cost = unit_cost * movement_data.quantity
        
        # Create inventory movement
        movement = InventoryMovement(
            product_id=movement_data.product_id,
            movement_type=movement_data.movement_type,
            quantity=movement_data.quantity,
            unit_cost=unit_cost,
            total_cost=total_cost,
            reference_type=movement_data.reference_type,
            reference_id=movement_data.reference_id,
            notes=movement_data.notes,
            created_by=current_user.id
        )
        
        db.add(movement)
        
        # Update product stock based on movement type
        if movement_data.movement_type in ["purchase", "return"]:
            product.current_stock += movement_data.quantity
        elif movement_data.movement_type in ["sale", "loss", "adjustment"]:
            product.current_stock -= movement_data.quantity
            
            # Check if stock goes negative
            if product.current_stock < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Insufficient stock. Current stock: {product.current_stock + movement_data.quantity}"
                )
        
        db.commit()
        db.refresh(movement)
        db.refresh(product)
        
        # Check for low stock alert
        if product.current_stock <= product.minimum_stock_level:
            inventory_service.create_low_stock_alert(product, current_user.business.id, db)
        
        logger.info(f"Inventory movement created: {movement.id} by {current_user.email}")
        
        return movement
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Inventory movement creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create inventory movement"
        )


@router.get("/movements")
async def get_inventory_movements(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    product_id: Optional[str] = Query(None, description="Filter by product"),
    movement_type: Optional[str] = Query(None, description="Filter by movement type"),
    start_date: Optional[datetime] = Query(None, description="Filter from date"),
    end_date: Optional[datetime] = Query(None, description="Filter to date"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get inventory movements with filtering and pagination
    
    Retrieve paginated list of inventory movements with optional filters.
    """
    
    try:
        business_id = current_user.business.id
        
        # Get product IDs for this business
        product_ids = db.query(Product.id).filter(
            Product.business_id == business_id
        ).all()
        product_ids = [pid[0] for pid in product_ids]
        
        # Build query
        query = db.query(InventoryMovement).filter(
            InventoryMovement.product_id.in_(product_ids)
        )
        
        # Apply filters
        if product_id:
            query = query.filter(InventoryMovement.product_id == product_id)
        
        if movement_type:
            query = query.filter(InventoryMovement.movement_type == movement_type)
        
        if start_date:
            query = query.filter(InventoryMovement.movement_date >= start_date)
        
        if end_date:
            query = query.filter(InventoryMovement.movement_date <= end_date)
        
        # Order by movement date (newest first)
        query = query.order_by(desc(InventoryMovement.movement_date))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        movements = query.offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "movements": movements
        }
        
    except Exception as e:
        logger.error(f"Failed to get inventory movements: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve inventory movements"
        )


# ========================================
# Low Stock Alerts Endpoints
# ========================================

@router.get("/alerts/low-stock", response_model=List[LowStockAlertResponse])
async def get_low_stock_alerts(
    unresolved_only: bool = Query(True, description="Show only unresolved alerts"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get low stock alerts
    
    Retrieve list of low stock alerts for the business.
    """
    
    try:
        business_id = current_user.business.id
        
        # Build query
        query = db.query(LowStockAlert).filter(
            LowStockAlert.business_id == business_id
        )
        
        if unresolved_only:
            query = query.filter(LowStockAlert.is_resolved == False)
        
        # Order by alert level (critical first)
        priority_order = {
            "out_of_stock": 1,
            "critical": 2,
            "low": 3
        }
        
        alerts = query.order_by(
            LowStockAlert.created_at.desc()
        ).all()
        
        # Sort by priority
        alerts_sorted = sorted(alerts, key=lambda x: priority_order.get(x.alert_level, 4))
        
        return alerts_sorted
        
    except Exception as e:
        logger.error(f"Failed to get low stock alerts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve low stock alerts"
        )


@router.put("/alerts/{alert_id}/resolve")
async def resolve_low_stock_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Resolve low stock alert
    
    Mark a low stock alert as resolved.
    """
    
    alert = db.query(LowStockAlert).filter(
        LowStockAlert.id == alert_id,
        LowStockAlert.business_id == current_user.business.id
    ).first()
    
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alert not found"
        )
    
    try:
        alert.is_resolved = True
        alert.resolved_at = datetime.utcnow()
        alert.resolved_by = current_user.id
        
        db.commit()
        
        logger.info(f"Low stock alert resolved: {alert_id} by {current_user.email}")
        
        return {
            "message": "Alert resolved successfully"
        }
        
    except Exception as e:
        db.rollback()
        logger.error(f"Alert resolution failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resolve alert"
        )


# ========================================
# Inventory Summary Endpoints
# ========================================

@router.get("/summary")
async def get_inventory_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get inventory summary
    
    Retrieve key inventory metrics including:
    - Total products
    - Low stock items count
    - Total stock value
    - Total inventory value (at cost)
    - Potential revenue (at selling price)
    """
    
    try:
        business_id = current_user.business.id
        
        # Get all active products
        products = db.query(Product).filter(
            Product.business_id == business_id,
            Product.is_active == True
        ).all()
        
        # Calculate metrics
        total_products = len(products)
        low_stock_count = len([p for p in products if p.current_stock <= p.minimum_stock_level])
        total_stock_value = sum(p.cost_price * p.current_stock for p in products)
        potential_revenue = sum(p.selling_price * p.current_stock for p in products)
        
        return {
            "total_products": total_products,
            "low_stock_count": low_stock_count,
            "total_stock_value": total_stock_value,
            "potential_revenue": potential_revenue,
            "potential_profit": potential_revenue - total_stock_value
        }
        
    except Exception as e:
        logger.error(f"Failed to get inventory summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve inventory summary"
        )