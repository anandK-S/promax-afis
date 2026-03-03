# ========================================
# Pro-Max AFIS - Inventory Service
# ========================================
# Business logic for inventory operations
# Author: Pro-Max Development Team

from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
import logging

from app.models.inventory import Product, InventoryMovement, MovementType, LowStockAlert
from app.core.redis_client import redis_client

# Configure logging
logger = logging.getLogger(__name__)


class InventoryService:
    """
    Service class for inventory operations
    """
    
    def __init__(self):
        """Initialize inventory service"""
        self.cache_ttl = 300  # 5 minutes
    
    def create_product(
        self,
        db: Session,
        business_id: int,
        product_data: Dict,
        user_id: int
    ) -> Product:
        """
        Create a new product
        
        Args:
            db: Database session
            business_id: Business ID
            product_data: Product data
            user_id: User ID creating the product
            
        Returns:
            Created product
        """
        try:
            # Calculate margin percentage
            margin_percentage = 0
            cost_price = product_data.get('cost_price', 0)
            selling_price = product_data.get('selling_price', 0)
            if cost_price > 0:
                margin_percentage = ((selling_price - cost_price) / cost_price) * 100
            
            # Create product object
            product = Product(
                business_id=business_id,
                product_name=product_data.get('product_name'),
                sku=product_data.get('sku'),
                barcode=product_data.get('barcode'),
                category=product_data.get('category'),
                subcategory=product_data.get('subcategory'),
                brand=product_data.get('brand'),
                cost_price=cost_price,
                selling_price=selling_price,
                margin_percentage=margin_percentage,
                unit=product_data.get('unit', 'pcs'),
                length=product_data.get('length'),
                width=product_data.get('width'),
                height=product_data.get('height'),
                weight=product_data.get('weight'),
                current_stock=product_data.get('current_stock', 0),
                minimum_stock_level=product_data.get('minimum_stock_level', 10),
                maximum_stock_level=product_data.get('maximum_stock_level', 100),
                reorder_point=product_data.get('reorder_point', 20),
                reorder_quantity=product_data.get('reorder_quantity', 50),
                gst_rate=product_data.get('gst_rate', 0),
                hsn_code=product_data.get('hsn_code'),
                gst_applicable=product_data.get('gst_applicable', True),
                description=product_data.get('description'),
                specifications=product_data.get('specifications'),
                manufacturer=product_data.get('manufacturer'),
                country_of_origin=product_data.get('country_of_origin'),
                image_urls=product_data.get('image_urls')
            )
            
            db.add(product)
            db.commit()
            db.refresh(product)
            
            # Create initial inventory movement if stock provided
            if product_data.get('current_stock', 0) > 0:
                self._create_inventory_movement(
                    db=db,
                    product_id=product.id,
                    movement_type=MovementType.PURCHASE,
                    quantity=product_data['current_stock'],
                    unit_cost=cost_price,
                    total_cost=cost_price * product_data['current_stock'],
                    notes="Initial stock entry",
                    user_id=user_id
                )
            
            # Check for low stock
            if product.is_low_stock:
                self._create_low_stock_alert(db, product)
            
            # Clear cache
            self._clear_inventory_cache(business_id)
            
            logger.info(f"Product created: {product.id} for business {business_id}")
            
            return product
            
        except Exception as e:
            db.rollback()
            logger.error(f"Product creation failed: {str(e)}")
            raise
    
    def record_inventory_movement(
        self,
        db: Session,
        business_id: int,
        movement_data: Dict,
        user_id: int
    ) -> InventoryMovement:
        """
        Record inventory movement
        
        Args:
            db: Database session
            business_id: Business ID
            movement_data: Movement data
            user_id: User ID recording the movement
            
        Returns:
            Created inventory movement
        """
        try:
            product_id = movement_data.get('product_id')
            movement_type = movement_data.get('movement_type')
            quantity = movement_data.get('quantity')
            
            # Get product
            product = db.query(Product).filter(
                Product.id == product_id,
                Product.business_id == business_id
            ).first()
            
            if not product:
                raise ValueError("Product not found")
            
            # Calculate costs
            unit_cost = movement_data.get('unit_cost', product.cost_price)
            total_cost = movement_data.get('total_cost', unit_cost * quantity)
            
            # Update product stock based on movement type
            if movement_type == MovementType.PURCHASE:
                product.current_stock += quantity
            elif movement_type == MovementType.SALE:
                product.current_stock -= quantity
            elif movement_type == MovementType.RETURN:
                product.current_stock += quantity
            elif movement_type == MovementType.ADJUSTMENT:
                # Positive adjustment adds, negative subtracts
                product.current_stock += quantity
            elif movement_type == MovementType.DAMAGE:
                product.current_stock -= quantity
            elif movement_type == MovementType.TRANSFER:
                # Transfer doesn't change total stock, just location
                pass
            
            # Create movement
            movement = InventoryMovement(
                product_id=product_id,
                movement_type=movement_type,
                quantity=quantity,
                unit_cost=unit_cost,
                total_cost=total_cost,
                reference_type=movement_data.get('reference_type'),
                reference_id=movement_data.get('reference_id'),
                reference_number=movement_data.get('reference_number'),
                notes=movement_data.get('notes'),
                reason=movement_data.get('reason'),
                from_location=movement_data.get('from_location'),
                to_location=movement_data.get('to_location'),
                movement_date=movement_data.get('movement_date') or datetime.utcnow(),
                created_by=user_id
            )
            
            db.add(movement)
            
            # Check for low stock after movement
            if product.is_low_stock:
                self._create_low_stock_alert(db, product)
            
            db.commit()
            db.refresh(movement)
            
            # Clear cache
            self._clear_inventory_cache(business_id)
            
            logger.info(f"Inventory movement recorded: {movement.id}")
            
            return movement
            
        except Exception as e:
            db.rollback()
            logger.error(f"Inventory movement recording failed: {str(e)}")
            raise
    
    def get_low_stock_alerts(
        self,
        db: Session,
        business_id: int,
        severity: Optional[str] = None,
        include_resolved: bool = False
    ) -> List[LowStockAlert]:
        """
        Get low stock alerts
        
        Args:
            db: Database session
            business_id: Business ID
            severity: Filter by severity
            include_resolved: Include resolved alerts
            
        Returns:
            List of low stock alerts
        """
        try:
            query = db.query(LowStockAlert).filter(
                LowStockAlert.business_id == business_id
            )
            
            if not include_resolved:
                query = query.filter(LowStockAlert.is_resolved == False)
            
            if severity:
                query = query.filter(LowStockAlert.severity == severity)
            
            alerts = query.order_by(
                LowStockAlert.created_at.desc()
            ).all()
            
            return alerts
            
        except Exception as e:
            logger.error(f"Failed to get low stock alerts: {str(e)}")
            raise
    
    def resolve_alert(
        self,
        db: Session,
        alert_id: int,
        user_id: int,
        resolution_notes: Optional[str] = None
    ) -> LowStockAlert:
        """
        Resolve a low stock alert
        
        Args:
            db: Database session
            alert_id: Alert ID
            user_id: User ID resolving the alert
            resolution_notes: Resolution notes
            
        Returns:
            Resolved alert
        """
        try:
            alert = db.query(LowStockAlert).filter(
                LowStockAlert.id == alert_id
            ).first()
            
            if not alert:
                raise ValueError("Alert not found")
            
            alert.is_resolved = True
            alert.resolved_at = datetime.utcnow()
            alert.resolved_by = user_id
            alert.resolution_notes = resolution_notes
            
            db.commit()
            db.refresh(alert)
            
            logger.info(f"Alert resolved: {alert_id}")
            
            return alert
            
        except Exception as e:
            db.rollback()
            logger.error(f"Alert resolution failed: {str(e)}")
            raise
    
    def _create_inventory_movement(
        self,
        db: Session,
        product_id: int,
        movement_type: MovementType,
        quantity: float,
        unit_cost: float,
        total_cost: float,
        notes: str,
        user_id: int
    ) -> InventoryMovement:
        """Create inventory movement helper"""
        movement = InventoryMovement(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity,
            unit_cost=unit_cost,
            total_cost=total_cost,
            notes=notes,
            movement_date=datetime.utcnow(),
            created_by=user_id
        )
        db.add(movement)
        return movement
    
    def _create_low_stock_alert(
        self,
        db: Session,
        product: Product
    ) -> LowStockAlert:
        """Create low stock alert"""
        # Check if alert already exists and is unresolved
        existing_alert = db.query(LowStockAlert).filter(
            and_(
                LowStockAlert.product_id == product.id,
                LowStockAlert.is_resolved == False
            )
        ).first()
        
        if existing_alert:
            # Update existing alert
            existing_alert.current_stock = product.current_stock
            existing_alert.shortage_quantity = product.reorder_point - product.current_stock
            
            # Update severity
            if product.current_stock == 0:
                existing_alert.severity = "critical"
            elif product.current_stock <= product.minimum_stock_level:
                existing_alert.severity = "high"
            else:
                existing_alert.severity = "medium"
        else:
            # Create new alert
            shortage = product.reorder_point - product.current_stock
            
            # Determine severity
            if product.current_stock == 0:
                severity = "critical"
            elif product.current_stock <= product.minimum_stock_level:
                severity = "high"
            else:
                severity = "medium"
            
            alert = LowStockAlert(
                product_id=product.id,
                business_id=product.business_id,
                current_stock=product.current_stock,
                reorder_point=product.reorder_point,
                shortage_quantity=shortage,
                severity=severity
            )
            db.add(alert)
    
    def _clear_inventory_cache(self, business_id: int):
        """Clear inventory cache for business"""
        patterns = [
            f"inventory_summary:{business_id}:*",
            f"products:{business_id}:*"
        ]
        for pattern in patterns:
            redis_client.cache_clear_pattern(pattern)