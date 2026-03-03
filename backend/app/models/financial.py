# ========================================
# Pro-Max AFIS - Financial Models
# ========================================
# Transaction and category models
# Author: Pro-Max Development Team

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class TransactionType(enum.Enum):
    """Transaction types"""
    INCOME = "income"
    EXPENSE = "expense"


class PaymentMethod(enum.Enum):
    """Payment methods"""
    CASH = "cash"
    UPI = "upi"
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    NET_BANKING = "net_banking"
    OTHER = "other"


class Transaction(Base):
    """
    Transaction model for income and expenses
    """
    
    __tablename__ = "transactions"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Business Foreign Key
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False, index=True)
    
    # Transaction Details
    transaction_type = Column(Enum(TransactionType), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    
    # Categorization
    category = Column(String(100), nullable=False, index=True)
    subcategory = Column(String(100), nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags
    
    # Description
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Payment Information
    payment_method = Column(Enum(PaymentMethod), nullable=True)
    reference_number = Column(String(100), unique=True, nullable=True, index=True)
    
    # Dates
    transaction_date = Column(DateTime(timezone=True), nullable=False, index=True)
    due_date = Column(DateTime(timezone=True), nullable=True)
    
    # Tax Information
    gst_applicable = Column(Boolean, default=False, nullable=False)
    gst_amount = Column(Float, default=0.0, nullable=False)
    gst_rate = Column(Float, default=0.0, nullable=False)
    tds_applicable = Column(Boolean, default=False, nullable=False)
    tds_amount = Column(Float, default=0.0, nullable=False)
    tds_rate = Column(Float, default=0.0, nullable=False)
    
    # Customer/Supplier Information
    party_name = Column(String(255), nullable=True)
    party_contact = Column(String(20), nullable=True)
    party_gst = Column(String(20), nullable=True)
    
    # Invoice/Receipt Information
    invoice_number = Column(String(100), nullable=True)
    invoice_date = Column(DateTime(timezone=True), nullable=True)
    receipt_number = Column(String(100), nullable=True)
    
    # Attachments
    attachment_url = Column(String(500), nullable=True)
    
    # Reconciliation
    is_reconciled = Column(Boolean, default=False, nullable=False)
    reconciled_at = Column(DateTime(timezone=True), nullable=True)
    
    # Audit
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    
    # Relationships
    business = relationship("Business", back_populates="transactions", lazy="select")
    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_transactions",
        lazy="select"
    )
    
    def __repr__(self):
        return f"<Transaction(id={self.id}, type={self.transaction_type.value}, amount={self.amount})>"
    
    @property
    def total_amount(self):
        """Calculate total amount including GST"""
        if self.gst_applicable:
            return self.amount + self.gst_amount
        return self.amount
    
    @property
    def net_amount(self):
        """Calculate net amount after TDS (for income)"""
        if self.tds_applicable and self.transaction_type == TransactionType.INCOME:
            return self.amount - self.tds_amount
        return self.amount


class Category(Base):
    """
    Category model for transaction categorization
    """
    
    __tablename__ = "categories"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Business Foreign Key
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=True, index=True)
    # Null business_id means system-wide default category
    
    # Category Details
    category_type = Column(Enum(TransactionType), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Hierarchy
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    # Color & Icon
    color = Column(String(20), nullable=True)
    icon = Column(String(50), nullable=True)
    
    # Settings
    is_default = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Tax Defaults
    default_gst_rate = Column(Float, nullable=True)
    default_tds_rate = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False)
    
    # Relationships
    parent = relationship("Category", remote_side=[id], backref="children")
    
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}', type={self.category_type.value})>"