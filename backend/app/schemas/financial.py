# ========================================
# Pro-Max AFIS - Financial Schemas
# ========================================
# Pydantic schemas for financial data validation
# Author: Pro-Max Development Team

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class TransactionType(str, Enum):
    """Transaction types"""
    INCOME = "income"
    EXPENSE = "expense"


class PaymentMethod(str, Enum):
    """Payment methods"""
    CASH = "cash"
    UPI = "upi"
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    NET_BANKING = "net_banking"
    OTHER = "other"


class TransactionCreate(BaseModel):
    """Schema for creating a transaction"""
    type: TransactionType = Field(..., description="Transaction type")
    amount: float = Field(..., gt=0, description="Transaction amount")
    category: Optional[str] = Field(None, max_length=100, description="Transaction category")
    subcategory: Optional[str] = Field(None, max_length=100, description="Transaction subcategory")
    tags: Optional[List[str]] = Field(None, description="List of tags")
    description: Optional[str] = Field(None, max_length=500, description="Transaction description")
    notes: Optional[str] = Field(None, description="Additional notes")
    payment_method: Optional[PaymentMethod] = Field(None, description="Payment method")
    reference_number: Optional[str] = Field(None, max_length=100, description="Reference number")
    transaction_date: Optional[datetime] = Field(None, description="Transaction date")
    due_date: Optional[datetime] = Field(None, description="Due date")
    gst_applicable: bool = Field(default=False, description="Whether GST is applicable")
    gst_amount: float = Field(default=0.0, ge=0, description="GST amount")
    gst_rate: float = Field(default=0.0, ge=0, le=100, description="GST rate percentage")
    tds_applicable: bool = Field(default=False, description="Whether TDS is applicable")
    tds_amount: float = Field(default=0.0, ge=0, description="TDS amount")
    tds_rate: float = Field(default=0.0, ge=0, le=100, description="TDS rate percentage")
    party_name: Optional[str] = Field(None, max_length=255, description="Customer/Supplier name")
    party_contact: Optional[str] = Field(None, max_length=20, description="Customer/Supplier contact")
    party_gst: Optional[str] = Field(None, max_length=20, description="Customer/Supplier GST")
    invoice_number: Optional[str] = Field(None, max_length=100, description="Invoice number")
    invoice_date: Optional[datetime] = Field(None, description="Invoice date")
    receipt_number: Optional[str] = Field(None, max_length=100, description="Receipt number")


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction"""
    type: Optional[TransactionType] = None
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, max_length=100)
    subcategory: Optional[str] = Field(None, max_length=100)
    tags: Optional[List[str]] = None
    description: Optional[str] = Field(None, max_length=500)
    notes: Optional[str] = None
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = Field(None, max_length=100)
    transaction_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    gst_applicable: Optional[bool] = None
    gst_amount: Optional[float] = Field(None, ge=0)
    gst_rate: Optional[float] = Field(None, ge=0, le=100)
    tds_applicable: Optional[bool] = None
    tds_amount: Optional[float] = Field(None, ge=0)
    tds_rate: Optional[float] = Field(None, ge=0, le=100)
    party_name: Optional[str] = Field(None, max_length=255)
    party_contact: Optional[str] = Field(None, max_length=20)
    party_gst: Optional[str] = Field(None, max_length=20)
    invoice_number: Optional[str] = Field(None, max_length=100)
    invoice_date: Optional[datetime] = None
    receipt_number: Optional[str] = Field(None, max_length=100)
    is_reconciled: Optional[bool] = None


class TransactionResponse(BaseModel):
    """Schema for transaction response"""
    id: int
    business_id: int
    transaction_type: str
    amount: float
    category: str
    subcategory: Optional[str]
    tags: Optional[List[str]]
    description: Optional[str]
    notes: Optional[str]
    payment_method: Optional[str]
    reference_number: Optional[str]
    transaction_date: datetime
    due_date: Optional[datetime]
    gst_applicable: bool
    gst_amount: float
    gst_rate: float
    tds_applicable: bool
    tds_amount: float
    tds_rate: float
    party_name: Optional[str]
    party_contact: Optional[str]
    party_gst: Optional[str]
    invoice_number: Optional[str]
    invoice_date: Optional[datetime]
    receipt_number: Optional[str]
    attachment_url: Optional[str]
    is_reconciled: bool
    created_by: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    
    @property
    def total_amount(self) -> float:
        """Calculate total amount including GST"""
        if self.gst_applicable:
            return self.amount + self.gst_amount
        return self.amount


class TransactionListResponse(BaseModel):
    """Schema for paginated transaction list"""
    items: List[TransactionResponse]
    total: int
    page: int
    limit: int
    total_pages: int


class FinancialSummary(BaseModel):
    """Schema for financial summary"""
    period: str  # daily, weekly, monthly
    start_date: datetime
    end_date: datetime
    
    # Income
    total_income: float
    income_count: int
    average_income: float
    
    # Expenses
    total_expenses: float
    expense_count: int
    average_expense: float
    
    # Net
    net_profit: float
    profit_margin: float
    
    # Breakdown by category
    income_by_category: Dict[str, float]
    expenses_by_category: Dict[str, float]
    
    # Payment methods
    income_by_payment_method: Dict[str, float]
    expenses_by_payment_method: Dict[str, float]
    
    # Tax
    total_gst_collected: float
    total_gst_paid: float
    total_tds_paid: float
    net_gst_liability: float


class ProfitLossStatement(BaseModel):
    """Schema for profit & loss statement"""
    period: str
    start_date: datetime
    end_date: datetime
    
    # Revenue
    gross_revenue: float
    discounts: float
    returns: float
    net_revenue: float
    
    # Cost of Goods Sold (COGS)
    opening_inventory_value: float
    purchases: float
    closing_inventory_value: float
    cost_of_goods_sold: float
    
    # Gross Profit
    gross_profit: float
    gross_profit_percentage: float
    
    # Operating Expenses
    operating_expenses: float
    operating_expenses_breakdown: Dict[str, float]
    
    # Operating Profit
    operating_profit: float
    operating_profit_percentage: float
    
    # Other Income/Expenses
    other_income: float
    other_expenses: float
    
    # Net Profit
    net_profit_before_tax: float
    tax_provision: float
    net_profit_after_tax: float
    net_profit_percentage: float


class CashFlowData(BaseModel):
    """Schema for cash flow data"""
    period: str
    start_date: datetime
    end_date: datetime
    
    # Opening Balance
    opening_balance: float
    
    # Cash Inflows
    cash_from_sales: float
    cash_from_debtors: float
    other_cash_inflows: float
    total_cash_inflows: float
    
    # Cash Outflows
    cash_to_suppliers: float
    cash_for_expenses: float
    cash_for_assets: float
    tax_payments: float
    other_cash_outflows: float
    total_cash_outflows: float
    
    # Net Cash Flow
    net_cash_flow: float
    
    # Closing Balance
    closing_balance: float
    
    # Cash Flow Trends
    daily_cash_flow: List[Dict[str, Any]]
    cash_runway_days: int
    burn_rate: float


class CategoryCreate(BaseModel):
    """Schema for creating a category"""
    category_type: TransactionType
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    parent_id: Optional[int] = None
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    icon: Optional[str] = Field(None, max_length=50)
    default_gst_rate: Optional[float] = Field(None, ge=0, le=100)
    default_tds_rate: Optional[float] = Field(None, ge=0, le=100)


class CategoryResponse(BaseModel):
    """Schema for category response"""
    id: int
    business_id: Optional[int]
    category_type: str
    name: str
    description: Optional[str]
    parent_id: Optional[int]
    color: Optional[str]
    icon: Optional[str]
    is_default: bool
    is_active: bool
    default_gst_rate: Optional[float]
    default_tds_rate: Optional[float]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True