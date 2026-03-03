# ========================================
# Pro-Max AFIS - Financials Endpoints
# ========================================
# Financial transactions, reports, and analytics
# Author: Pro-Max Development Team

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import logging

from app.core.config import settings
from app.core.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models.user import User
from app.models.financial import Transaction
from app.schemas.financial import (
    TransactionCreate,
    TransactionResponse,
    TransactionListResponse,
    FinancialSummary,
    ProfitLossStatement,
    CashFlowData
)
from app.services.financial_service import FinancialService

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Initialize financial service
financial_service = FinancialService()


# ========================================
# Transaction Endpoints
# ========================================

@router.post("/transactions", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new financial transaction
    
    Creates a new income or expense transaction for the business.
    Transactions are automatically categorized using AI.
    
    - **type**: Transaction type ('income' or 'expense')
    - **amount**: Transaction amount (positive number)
    - **category**: Transaction category
    - **description**: Transaction description
    - **payment_method**: Payment method (UPI, Cash, Bank Transfer, etc.)
    - **transaction_date**: Date of transaction
    - **gst_applicable**: Whether GST is applicable
    - **gst_amount**: GST amount if applicable
    """
    
    try:
        # Get business ID
        business_id = current_user.business.id
        
        # Auto-categorize if category not provided
        if not transaction_data.category:
            transaction_data.category = financial_service.auto_categorize(
                transaction_data.description
            )
        
        # Create transaction
        transaction = Transaction(
            business_id=business_id,
            transaction_type=transaction_data.type,
            amount=transaction_data.amount,
            category=transaction_data.category,
            subcategory=transaction_data.subcategory,
            description=transaction_data.description,
            payment_method=transaction_data.payment_method,
            reference_number=transaction_data.reference_number,
            transaction_date=transaction_data.transaction_date or datetime.utcnow(),
            tags=transaction_data.tags,
            gst_applicable=transaction_data.gst_applicable,
            gst_amount=transaction_data.gst_amount,
            tds_applicable=transaction_data.tds_applicable,
            tds_amount=transaction_data.tds_amount,
            created_by=current_user.id
        )
        
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"Transaction created: {transaction.id} by {current_user.email}")
        
        return transaction
        
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction creation failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create transaction"
        )


@router.get("/transactions", response_model=TransactionListResponse)
async def get_transactions(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    type: Optional[str] = Query(None, description="Filter by type (income/expense)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[datetime] = Query(None, description="Filter from date"),
    end_date: Optional[datetime] = Query(None, description="Filter to date"),
    search: Optional[str] = Query(None, description="Search in description"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all transactions with filtering and pagination
    
    Retrieve paginated list of financial transactions with optional filters.
    Supports filtering by type, category, date range, and text search.
    
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 20, max: 100)
    - **type**: Filter by transaction type
    - **category**: Filter by category
    - **start_date**: Filter transactions from this date
    - **end_date**: Filter transactions to this date
    - **search**: Search text in transaction description
    """
    
    try:
        business_id = current_user.business.id
        
        # Build query
        query = db.query(Transaction).filter(Transaction.business_id == business_id)
        
        # Apply filters
        if type:
            query = query.filter(Transaction.transaction_type == type)
        
        if category:
            query = query.filter(Transaction.category == category)
        
        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)
        
        if search:
            query = query.filter(Transaction.description.ilike(f"%{search}%"))
        
        # Order by transaction date (newest first)
        query = query.order_by(desc(Transaction.transaction_date))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        transactions = query.offset(offset).limit(limit).all()
        
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "transactions": transactions
        }
        
    except Exception as e:
        logger.error(f"Failed to get transactions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve transactions"
        )


@router.get("/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get transaction by ID
    
    Retrieve details of a specific transaction.
    """
    
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.business_id == current_user.business.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction


@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: str,
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update transaction
    
    Update an existing transaction's details.
    """
    
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.business_id == current_user.business.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    try:
        # Update transaction fields
        transaction.transaction_type = transaction_data.type
        transaction.amount = transaction_data.amount
        transaction.category = transaction_data.category
        transaction.subcategory = transaction_data.subcategory
        transaction.description = transaction_data.description
        transaction.payment_method = transaction_data.payment_method
        transaction.reference_number = transaction_data.reference_number
        transaction.transaction_date = transaction_data.transaction_date
        transaction.tags = transaction_data.tags
        transaction.gst_applicable = transaction_data.gst_applicable
        transaction.gst_amount = transaction_data.gst_amount
        transaction.tds_applicable = transaction_data.tds_applicable
        transaction.tds_amount = transaction_data.tds_amount
        
        db.commit()
        db.refresh(transaction)
        
        logger.info(f"Transaction updated: {transaction_id} by {current_user.email}")
        
        return transaction
        
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction update failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update transaction"
        )


@router.delete("/transactions/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete transaction
    
    Permanently delete a transaction.
    """
    
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.business_id == current_user.business.id
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    try:
        db.delete(transaction)
        db.commit()
        
        logger.info(f"Transaction deleted: {transaction_id} by {current_user.email}")
        
        return None
        
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction deletion failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete transaction"
        )


# ========================================
# Financial Summary Endpoints
# ========================================

@router.get("/summary", response_model=FinancialSummary)
async def get_financial_summary(
    period: str = Query("today", description="Time period: today, week, month, quarter, year"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get financial summary
    
    Retrieve key financial metrics for the specified period including:
    - Total income
    - Total expenses
    - Net profit
    - Profit margin
    - Transaction counts
    """
    
    try:
        business_id = current_user.business.id
        
        # Calculate date range based on period
        end_date = datetime.utcnow()
        if period == "today":
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "week":
            start_date = end_date - timedelta(days=7)
        elif period == "month":
            start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "quarter":
            quarter = (end_date.month - 1) // 3 + 1
            start_date = end_date.replace(month=(quarter - 1) * 3 + 1, day=1, hour=0, minute=0, second=0, microsecond=0)
        elif period == "year":
            start_date = end_date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Query transactions
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()
        
        # Calculate totals
        total_income = sum(t.amount for t in transactions if t.transaction_type == "income")
        total_expenses = sum(t.amount for t in transactions if t.transaction_type == "expense")
        net_profit = total_income - total_expenses
        profit_margin = (net_profit / total_income * 100) if total_income > 0 else 0
        
        # Count transactions
        income_count = len([t for t in transactions if t.transaction_type == "income"])
        expense_count = len([t for t in transactions if t.transaction_type == "expense"])
        
        return {
            "period": period,
            "start_date": start_date,
            "end_date": end_date,
            "total_income": total_income,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "profit_margin": round(profit_margin, 2),
            "transaction_count": len(transactions),
            "income_count": income_count,
            "expense_count": expense_count
        }
        
    except Exception as e:
        logger.error(f"Failed to get financial summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve financial summary"
        )


@router.get("/profit-loss", response_model=ProfitLossStatement)
async def get_profit_loss_statement(
    start_date: datetime = Query(..., description="Start date for P&L statement"),
    end_date: datetime = Query(..., description="End date for P&L statement"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate Profit & Loss statement
    
    Generate a detailed P&L statement for the specified date range.
    Includes income breakdown by category and expense breakdown.
    """
    
    try:
        business_id = current_user.business.id
        
        # Query transactions
        transactions = db.query(Transaction).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).all()
        
        # Separate income and expenses
        income_transactions = [t for t in transactions if t.transaction_type == "income"]
        expense_transactions = [t for t in transactions if t.transaction_type == "expense"]
        
        # Calculate totals
        total_income = sum(t.amount for t in income_transactions)
        total_expenses = sum(t.amount for t in expense_transactions)
        gross_profit = total_income - total_expenses
        net_profit = gross_profit  # Simplified, in real scenario include taxes, interest, etc.
        
        # Breakdown by category
        income_by_category = {}
        for t in income_transactions:
            category = t.category or "Uncategorized"
            income_by_category[category] = income_by_category.get(category, 0) + t.amount
        
        expense_by_category = {}
        for t in expense_transactions:
            category = t.category or "Uncategorized"
            expense_by_category[category] = expense_by_category.get(category, 0) + t.amount
        
        return {
            "period": {
                "start_date": start_date,
                "end_date": end_date
            },
            "income": {
                "total": total_income,
                "by_category": [
                    {"category": cat, "amount": amount}
                    for cat, amount in income_by_category.items()
                ]
            },
            "expenses": {
                "total": total_expenses,
                "by_category": [
                    {"category": cat, "amount": amount}
                    for cat, amount in expense_by_category.items()
                ]
            },
            "gross_profit": gross_profit,
            "net_profit": net_profit,
            "profit_margin": round((net_profit / total_income * 100) if total_income > 0 else 0, 2)
        }
        
    except Exception as e:
        logger.error(f"Failed to generate P&L statement: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate P&L statement"
        )


@router.get("/cash-flow")
async def get_cash_flow_data(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get cash flow data
    
    Retrieve cash flow data for the specified number of days.
    Useful for cash flow charts and runway calculations.
    """
    
    try:
        business_id = current_user.business.id
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Query daily cash flow
        cash_flow = db.query(
            func.date(Transaction.transaction_date).label('date'),
            func.sum(
                func.case(
                    (Transaction.transaction_type == 'income', Transaction.amount),
                    else_=0
                )
            ).label('income'),
            func.sum(
                func.case(
                    (Transaction.transaction_type == 'expense', Transaction.amount),
                    else_=0
                )
            ).label('expenses')
        ).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_date >= start_date,
            Transaction.transaction_date <= end_date
        ).group_by(
            func.date(Transaction.transaction_date)
        ).order_by(
            func.date(Transaction.transaction_date)
        ).all()
        
        # Format data
        data = [
            {
                "date": str(row.date),
                "income": float(row.income) if row.income else 0,
                "expenses": float(row.expenses) if row.expenses else 0,
                "net": float(row.income - row.expenses) if row.income and row.expenses else 0
            }
            for row in cash_flow
        ]
        
        return {
            "period_days": days,
            "start_date": start_date,
            "end_date": end_date,
            "data": data
        }
        
    except Exception as e:
        logger.error(f"Failed to get cash flow data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve cash flow data"
        )


@router.get("/categories")
async def get_transaction_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all transaction categories
    
    Retrieve list of all unique transaction categories used by the business.
    """
    
    try:
        business_id = current_user.business.id
        
        # Get unique categories
        income_categories = db.query(Transaction.category).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_type == "income",
            Transaction.category.isnot(None)
        ).distinct().all()
        
        expense_categories = db.query(Transaction.category).filter(
            Transaction.business_id == business_id,
            Transaction.transaction_type == "expense",
            Transaction.category.isnot(None)
        ).distinct().all()
        
        return {
            "income_categories": [cat[0] for cat in income_categories],
            "expense_categories": [cat[0] for cat in expense_categories]
        }
        
    except Exception as e:
        logger.error(f"Failed to get categories: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve categories"
        )