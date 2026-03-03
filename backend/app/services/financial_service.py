# ========================================
# Pro-Max AFIS - Financial Service
# ========================================
# Business logic for financial operations
# Author: Pro-Max Development Team

from typing import Dict, List, Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_
import logging

from app.models.financial import Transaction, TransactionType, PaymentMethod
from app.ml.models.categorization import TransactionCategorizer
from app.core.redis_client import redis_client

# Configure logging
logger = logging.getLogger(__name__)

# Initialize categorizer
transaction_categorizer = TransactionCategorizer()


class FinancialService:
    """
    Service class for financial operations
    """
    
    def __init__(self):
        """Initialize financial service"""
        self.categorizer = transaction_categorizer
        self.cache_ttl = 300  # 5 minutes
    
    def create_transaction(
        self,
        db: Session,
        business_id: int,
        transaction_data: Dict,
        user_id: int
    ) -> Transaction:
        """
        Create a new transaction
        
        Args:
            db: Database session
            business_id: Business ID
            transaction_data: Transaction data
            user_id: User ID creating the transaction
            
        Returns:
            Created transaction
        """
        try:
            # Auto-categorize if category not provided
            if not transaction_data.get('category'):
                category_result = self.categorizer.categorize(
                    description=transaction_data.get('description', ''),
                    transaction_type=transaction_data.get('transaction_type', 'expense')
                )
                transaction_data['category'] = category_result['category']
                transaction_data['subcategory'] = category_result.get('subcategory')
            
            # Create transaction object
            transaction = Transaction(
                business_id=business_id,
                transaction_type=transaction_data.get('transaction_type'),
                amount=transaction_data.get('amount'),
                category=transaction_data.get('category'),
                subcategory=transaction_data.get('subcategory'),
                tags=transaction_data.get('tags'),
                description=transaction_data.get('description'),
                notes=transaction_data.get('notes'),
                payment_method=transaction_data.get('payment_method'),
                reference_number=transaction_data.get('reference_number'),
                transaction_date=transaction_data.get('transaction_date') or datetime.utcnow(),
                due_date=transaction_data.get('due_date'),
                gst_applicable=transaction_data.get('gst_applicable', False),
                gst_amount=transaction_data.get('gst_amount', 0),
                gst_rate=transaction_data.get('gst_rate', 0),
                tds_applicable=transaction_data.get('tds_applicable', False),
                tds_amount=transaction_data.get('tds_amount', 0),
                tds_rate=transaction_data.get('tds_rate', 0),
                party_name=transaction_data.get('party_name'),
                party_contact=transaction_data.get('party_contact'),
                party_gst=transaction_data.get('party_gst'),
                invoice_number=transaction_data.get('invoice_number'),
                invoice_date=transaction_data.get('invoice_date'),
                receipt_number=transaction_data.get('receipt_number'),
                attachment_url=transaction_data.get('attachment_url'),
                created_by=user_id
            )
            
            db.add(transaction)
            db.commit()
            db.refresh(transaction)
            
            # Clear cache for this business
            self._clear_financial_cache(business_id)
            
            logger.info(f"Transaction created: {transaction.id} for business {business_id}")
            
            return transaction
            
        except Exception as e:
            db.rollback()
            logger.error(f"Transaction creation failed: {str(e)}")
            raise
    
    def get_transactions(
        self,
        db: Session,
        business_id: int,
        page: int = 1,
        limit: int = 20,
        transaction_type: Optional[str] = None,
        category: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search: Optional[str] = None
    ) -> Dict:
        """
        Get paginated transactions with filters
        
        Args:
            db: Database session
            business_id: Business ID
            page: Page number
            limit: Items per page
            transaction_type: Filter by transaction type
            category: Filter by category
            start_date: Filter by start date
            end_date: Filter by end date
            search: Search in description
            
        Returns:
            Dictionary with transactions and pagination info
        """
        try:
            # Build query
            query = db.query(Transaction).filter(
                Transaction.business_id == business_id
            )
            
            # Apply filters
            if transaction_type:
                query = query.filter(
                    Transaction.transaction_type == TransactionType(transaction_type)
                )
            
            if category:
                query = query.filter(Transaction.category == category)
            
            if start_date:
                query = query.filter(Transaction.transaction_date >= start_date)
            
            if end_date:
                query = query.filter(Transaction.transaction_date <= end_date)
            
            if search:
                query = query.filter(
                    or_(
                        Transaction.description.ilike(f"%{search}%"),
                        Transaction.party_name.ilike(f"%{search}%"),
                        Transaction.reference_number.ilike(f"%{search}%")
                    )
                )
            
            # Order by date descending
            query = query.order_by(desc(Transaction.transaction_date))
            
            # Get total count
            total = query.count()
            
            # Apply pagination
            offset = (page - 1) * limit
            transactions = query.offset(offset).limit(limit).all()
            
            return {
                "items": transactions,
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": (total + limit - 1) // limit
            }
            
        except Exception as e:
            logger.error(f"Failed to get transactions: {str(e)}")
            raise
    
    def get_financial_summary(
        self,
        db: Session,
        business_id: int,
        period: str = "daily"
    ) -> Dict:
        """
        Get financial summary for a period
        
        Args:
            db: Database session
            business_id: Business ID
            period: Period type (daily, weekly, monthly)
            
        Returns:
            Financial summary dictionary
        """
        try:
            # Try to get from cache
            cache_key = f"financial_summary:{business_id}:{period}"
            cached = redis_client.cache_get(cache_key)
            if cached:
                return cached
            
            # Calculate date range
            end_date = datetime.utcnow()
            if period == "daily":
                start_date = end_date - timedelta(days=1)
            elif period == "weekly":
                start_date = end_date - timedelta(weeks=1)
            elif period == "monthly":
                start_date = end_date - timedelta(days=30)
            else:
                start_date = end_date - timedelta(days=1)
            
            # Get income data
            income_data = db.query(
                func.sum(Transaction.amount).label('total'),
                func.count(Transaction.id).label('count')
            ).filter(
                and_(
                    Transaction.business_id == business_id,
                    Transaction.transaction_type == TransactionType.INCOME,
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date
                )
            ).first()
            
            # Get expense data
            expense_data = db.query(
                func.sum(Transaction.amount).label('total'),
                func.count(Transaction.id).label('count')
            ).filter(
                and_(
                    Transaction.business_id == business_id,
                    Transaction.transaction_type == TransactionType.EXPENSE,
                    Transaction.transaction_date >= start_date,
                    Transaction.transaction_date <= end_date
                )
            ).first()
            
            # Extract values
            total_income = float(income_data.total or 0)
            income_count = income_data.count or 0
            total_expenses = float(expense_data.total or 0)
            expense_count = expense_data.count or 0
            
            # Calculate metrics
            net_profit = total_income - total_expenses
            profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0
            average_income = total_income / income_count if income_count > 0 else 0
            average_expense = total_expenses / expense_count if expense_count > 0 else 0
            
            # Get category breakdown
            income_by_category = self._get_category_breakdown(
                db, business_id, TransactionType.INCOME, start_date, end_date
            )
            expenses_by_category = self._get_category_breakdown(
                db, business_id, TransactionType.EXPENSE, start_date, end_date
            )
            
            # Get payment method breakdown
            income_by_payment_method = self._get_payment_method_breakdown(
                db, business_id, TransactionType.INCOME, start_date, end_date
            )
            expenses_by_payment_method = self._get_payment_method_breakdown(
                db, business_id, TransactionType.EXPENSE, start_date, end_date
            )
            
            # Get tax summary
            tax_summary = self._get_tax_summary(
                db, business_id, start_date, end_date
            )
            
            summary = {
                "period": period,
                "start_date": start_date,
                "end_date": end_date,
                "total_income": total_income,
                "income_count": income_count,
                "average_income": average_income,
                "total_expenses": total_expenses,
                "expense_count": expense_count,
                "average_expense": average_expense,
                "net_profit": net_profit,
                "profit_margin": profit_margin,
                "income_by_category": income_by_category,
                "expenses_by_category": expenses_by_category,
                "income_by_payment_method": income_by_payment_method,
                "expenses_by_payment_method": expenses_by_payment_method,
                **tax_summary
            }
            
            # Cache the result
            redis_client.cache_set(cache_key, summary, self.cache_ttl)
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to get financial summary: {str(e)}")
            raise
    
    def auto_categorize(self, description: str) -> str:
        """
        Auto-categorize transaction based on description
        
        Args:
            description: Transaction description
            
        Returns:
            Suggested category
        """
        try:
            result = self.categorizer.categorize(
                description=description,
                transaction_type="expense"
            )
            return result['category']
        except Exception as e:
            logger.error(f"Auto-categorization failed: {str(e)}")
            return "Other"
    
    def _get_category_breakdown(
        self,
        db: Session,
        business_id: int,
        transaction_type: TransactionType,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, float]:
        """Get breakdown by category"""
        results = db.query(
            Transaction.category,
            func.sum(Transaction.amount).label('total')
        ).filter(
            and_(
                Transaction.business_id == business_id,
                Transaction.transaction_type == transaction_type,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )
        ).group_by(Transaction.category).all()
        
        return {category: float(total) for category, total in results}
    
    def _get_payment_method_breakdown(
        self,
        db: Session,
        business_id: int,
        transaction_type: TransactionType,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, float]:
        """Get breakdown by payment method"""
        results = db.query(
            Transaction.payment_method,
            func.sum(Transaction.amount).label('total')
        ).filter(
            and_(
                Transaction.business_id == business_id,
                Transaction.transaction_type == transaction_type,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date,
                Transaction.payment_method.isnot(None)
            )
        ).group_by(Transaction.payment_method).all()
        
        return {str(method): float(total) for method, total in results}
    
    def _get_tax_summary(
        self,
        db: Session,
        business_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, float]:
        """Get tax summary"""
        # Get GST collected (from income)
        gst_collected = db.query(
            func.sum(Transaction.gst_amount)
        ).filter(
            and_(
                Transaction.business_id == business_id,
                Transaction.transaction_type == TransactionType.INCOME,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )
        ).scalar() or 0
        
        # Get GST paid (from expenses)
        gst_paid = db.query(
            func.sum(Transaction.gst_amount)
        ).filter(
            and_(
                Transaction.business_id == business_id,
                Transaction.transaction_type == TransactionType.EXPENSE,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )
        ).scalar() or 0
        
        # Get TDS paid
        tds_paid = db.query(
            func.sum(Transaction.tds_amount)
        ).filter(
            and_(
                Transaction.business_id == business_id,
                Transaction.transaction_date >= start_date,
                Transaction.transaction_date <= end_date
            )
        ).scalar() or 0
        
        return {
            "total_gst_collected": float(gst_collected),
            "total_gst_paid": float(gst_paid),
            "total_tds_paid": float(tds_paid),
            "net_gst_liability": float(gst_collected - gst_paid)
        }
    
    def _clear_financial_cache(self, business_id: int):
        """Clear financial cache for business"""
        patterns = [
            f"financial_summary:{business_id}:*",
            f"transactions:{business_id}:*"
        ]
        for pattern in patterns:
            redis_client.cache_clear_pattern(pattern)