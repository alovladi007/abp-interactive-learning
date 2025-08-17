"""
Payment, Transaction, and Notification Models for EUREKA Platform
"""

from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .course import Base

class TransactionStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"

class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    PAYPAL = "paypal"
    STRIPE = "stripe"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"
    APPLE_PAY = "apple_pay"
    GOOGLE_PAY = "google_pay"

class Transaction(Base):
    __tablename__ = 'transactions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Transaction Details
    transaction_id = Column(String(100), unique=True, index=True)
    payment_method = Column(Enum(PaymentMethod))
    
    # Amount Information
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    tax_amount = Column(Float, default=0.0)
    discount_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    
    # Items
    items = Column(JSON)  # List of course IDs and prices
    coupon_code = Column(String(50))
    
    # Payment Gateway Information
    gateway = Column(String(50))  # stripe, paypal, etc.
    gateway_transaction_id = Column(String(200))
    gateway_response = Column(JSON)
    
    # Status
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    
    # Billing Information
    billing_name = Column(String(200))
    billing_email = Column(String(255))
    billing_address = Column(Text)
    billing_country = Column(String(100))
    billing_zip = Column(String(20))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    failed_at = Column(DateTime)
    refunded_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
    invoices = relationship("Invoice", back_populates="transaction")

class Invoice(Base):
    __tablename__ = 'invoices'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    
    # Invoice Details
    invoice_number = Column(String(100), unique=True)
    invoice_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    
    # PDF Storage
    pdf_url = Column(String(500))
    
    # Status
    is_paid = Column(Boolean, default=False)
    paid_at = Column(DateTime)
    
    # Relationships
    transaction = relationship("Transaction", back_populates="invoices")

class Coupon(Base):
    __tablename__ = 'coupons'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    
    # Discount Details
    discount_type = Column(String(20))  # percentage or fixed
    discount_value = Column(Float)
    max_discount_amount = Column(Float)  # For percentage discounts
    
    # Validity
    valid_from = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime)
    usage_limit = Column(Integer)  # Total usage limit
    usage_count = Column(Integer, default=0)
    user_usage_limit = Column(Integer, default=1)  # Per user limit
    
    # Restrictions
    minimum_purchase_amount = Column(Float)
    applicable_course_ids = Column(JSON)  # List of course IDs
    applicable_category_ids = Column(JSON)  # List of category IDs
    
    # Status
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class RefundRequest(Base):
    __tablename__ = 'refund_requests'
    
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey('transactions.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    
    # Request Details
    reason = Column(Text, nullable=False)
    additional_comments = Column(Text)
    
    # Status
    status = Column(String(50), default="pending")  # pending, approved, rejected
    admin_notes = Column(Text)
    processed_by = Column(Integer, ForeignKey('users.id'))
    
    # Timestamps
    requested_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    
    # Refund Details
    refund_amount = Column(Float)
    refund_transaction_id = Column(String(200))

class NotificationType(enum.Enum):
    ENROLLMENT = "enrollment"
    COURSE_UPDATE = "course_update"
    ANNOUNCEMENT = "announcement"
    CERTIFICATE = "certificate"
    PAYMENT = "payment"
    REVIEW = "review"
    ACHIEVEMENT = "achievement"
    REMINDER = "reminder"
    PROMOTIONAL = "promotional"
    SYSTEM = "system"

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Notification Content
    type = Column(Enum(NotificationType))
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    
    # Action
    action_url = Column(String(500))
    action_text = Column(String(100))
    
    # Metadata
    metadata = Column(JSON)  # Additional data like course_id, etc.
    
    # Status
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    
    # Delivery
    email_sent = Column(Boolean, default=False)
    push_sent = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)  # Auto-delete old notifications
    
    # Relationships
    user = relationship("User", back_populates="notifications")

class Subscription(Base):
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # Subscription Details
    plan_name = Column(String(100))  # Basic, Pro, Premium
    plan_price = Column(Float)
    billing_cycle = Column(String(20))  # monthly, yearly
    
    # Status
    is_active = Column(Boolean, default=True)
    is_cancelled = Column(Boolean, default=False)
    
    # Dates
    started_at = Column(DateTime, default=datetime.utcnow)
    current_period_start = Column(DateTime)
    current_period_end = Column(DateTime)
    cancelled_at = Column(DateTime)
    
    # Payment
    payment_method_id = Column(String(200))
    stripe_subscription_id = Column(String(200))
    
    # Features
    features = Column(JSON)  # List of features included in plan