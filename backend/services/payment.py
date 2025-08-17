"""
Payment Processing Service for EUREKA Platform
Integrates Stripe, PayPal, and other payment providers
"""

import stripe
import paypalrestsdk
import hashlib
import hmac
import json
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session

from ..models.payment import Transaction, TransactionStatus, PaymentMethod, Invoice, Coupon, RefundRequest
from ..models.course import Course
from ..models.user import User, Enrollment
from ..config import settings
from ..utils import send_email, generate_invoice_pdf


class PaymentService:
    """
    Unified payment service supporting multiple payment providers
    """
    
    def __init__(self, db: Session):
        self.db = db
        
        # Initialize Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Initialize PayPal
        paypalrestsdk.configure({
            "mode": settings.PAYPAL_MODE,  # sandbox or live
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        
        self.tax_rates = {
            "US": 0.08,
            "EU": 0.20,
            "UK": 0.20,
            "CA": 0.13,
            "AU": 0.10,
            "default": 0.10
        }
    
    def process_payment(
        self,
        user: User,
        courses: List[Course],
        payment_method: str,
        payment_details: Dict[str, Any],
        coupon_code: Optional[str] = None
    ) -> Transaction:
        """
        Process payment for course purchase
        
        Args:
            user: User making the purchase
            courses: List of courses to purchase
            payment_method: Payment method type
            payment_details: Payment method specific details
            coupon_code: Optional coupon code
        
        Returns:
            Transaction object
        """
        # Calculate total amount
        subtotal = sum(course.price for course in courses)
        discount_amount = 0
        
        # Apply coupon if provided
        if coupon_code:
            coupon = self.db.query(Coupon).filter(
                Coupon.code == coupon_code,
                Coupon.is_active == True,
                Coupon.valid_until > datetime.utcnow()
            ).first()
            
            if coupon:
                discount_amount = self._calculate_coupon_discount(coupon, subtotal, courses)
                
                # Update coupon usage
                coupon.usage_count += 1
                if coupon.usage_limit and coupon.usage_count >= coupon.usage_limit:
                    coupon.is_active = False
        
        # Calculate tax
        tax_amount = self._calculate_tax(subtotal - discount_amount, user.country)
        
        # Total amount
        total_amount = subtotal - discount_amount + tax_amount
        
        # Create transaction record
        transaction = Transaction(
            user_id=user.id,
            transaction_id=self._generate_transaction_id(),
            payment_method=PaymentMethod[payment_method.upper()],
            amount=subtotal,
            discount_amount=discount_amount,
            tax_amount=tax_amount,
            total_amount=total_amount,
            currency=payment_details.get("currency", "USD"),
            items=[{"course_id": c.id, "price": c.price} for c in courses],
            coupon_code=coupon_code,
            billing_name=payment_details.get("billing_name", f"{user.first_name} {user.last_name}"),
            billing_email=payment_details.get("billing_email", user.email),
            billing_country=payment_details.get("billing_country", user.country),
            status=TransactionStatus.PENDING
        )
        
        self.db.add(transaction)
        self.db.commit()
        
        # Process payment based on method
        try:
            if payment_method.upper() == "STRIPE":
                result = self._process_stripe_payment(transaction, payment_details)
            elif payment_method.upper() == "PAYPAL":
                result = self._process_paypal_payment(transaction, payment_details)
            elif payment_method.upper() == "CRYPTO":
                result = self._process_crypto_payment(transaction, payment_details)
            else:
                # Default card processing
                result = self._process_card_payment(transaction, payment_details)
            
            if result["success"]:
                transaction.status = TransactionStatus.COMPLETED
                transaction.gateway_transaction_id = result.get("transaction_id")
                transaction.gateway_response = result
                transaction.completed_at = datetime.utcnow()
                
                # Create enrollments
                for course in courses:
                    enrollment = Enrollment(
                        user_id=user.id,
                        course_id=course.id,
                        purchase_price=course.price,
                        purchase_currency=transaction.currency,
                        transaction_id=transaction.id
                    )
                    self.db.add(enrollment)
                    
                    # Update course enrollment count
                    course.enrollment_count += 1
                
                # Generate and send invoice
                self._generate_invoice(transaction)
                
                # Send confirmation email
                self._send_payment_confirmation(user, transaction, courses)
                
            else:
                transaction.status = TransactionStatus.FAILED
                transaction.failed_at = datetime.utcnow()
                transaction.gateway_response = result
                
        except Exception as e:
            transaction.status = TransactionStatus.FAILED
            transaction.failed_at = datetime.utcnow()
            transaction.gateway_response = {"error": str(e)}
            raise
        
        finally:
            self.db.commit()
        
        return transaction
    
    def _process_stripe_payment(
        self,
        transaction: Transaction,
        payment_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process payment through Stripe
        """
        try:
            # Create or retrieve customer
            customer = None
            if payment_details.get("customer_id"):
                customer = stripe.Customer.retrieve(payment_details["customer_id"])
            else:
                customer = stripe.Customer.create(
                    email=transaction.billing_email,
                    name=transaction.billing_name,
                    metadata={"user_id": transaction.user_id}
                )
            
            # Create payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(transaction.total_amount * 100),  # Convert to cents
                currency=transaction.currency.lower(),
                customer=customer.id,
                payment_method=payment_details.get("payment_method_id"),
                confirm=True,
                metadata={
                    "transaction_id": transaction.transaction_id,
                    "user_id": transaction.user_id
                }
            )
            
            if payment_intent.status == "succeeded":
                return {
                    "success": True,
                    "transaction_id": payment_intent.id,
                    "customer_id": customer.id,
                    "payment_intent": payment_intent.to_dict()
                }
            else:
                return {
                    "success": False,
                    "error": "Payment not completed",
                    "status": payment_intent.status
                }
                
        except stripe.error.CardError as e:
            return {
                "success": False,
                "error": e.user_message,
                "code": e.code
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _process_paypal_payment(
        self,
        transaction: Transaction,
        payment_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process payment through PayPal
        """
        try:
            # Create payment
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": payment_details.get("return_url", f"{settings.FRONTEND_URL}/payment/success"),
                    "cancel_url": payment_details.get("cancel_url", f"{settings.FRONTEND_URL}/payment/cancel")
                },
                "transactions": [{
                    "amount": {
                        "total": str(transaction.total_amount),
                        "currency": transaction.currency
                    },
                    "description": f"EUREKA Course Purchase - {transaction.transaction_id}"
                }]
            })
            
            if payment.create():
                # Extract approval URL
                approval_url = None
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        break
                
                return {
                    "success": True,
                    "transaction_id": payment.id,
                    "approval_url": approval_url,
                    "payment": payment.to_dict()
                }
            else:
                return {
                    "success": False,
                    "error": payment.error
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def execute_paypal_payment(
        self,
        payment_id: str,
        payer_id: str
    ) -> Dict[str, Any]:
        """
        Execute approved PayPal payment
        """
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                return {
                    "success": True,
                    "payment": payment.to_dict()
                }
            else:
                return {
                    "success": False,
                    "error": payment.error
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _process_crypto_payment(
        self,
        transaction: Transaction,
        payment_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process cryptocurrency payment
        """
        # This would integrate with a crypto payment processor like Coinbase Commerce
        # For now, returning a mock response
        
        crypto_address = self._generate_crypto_address(transaction.currency)
        
        return {
            "success": True,
            "transaction_id": f"crypto_{uuid.uuid4().hex}",
            "payment_address": crypto_address,
            "amount_crypto": transaction.total_amount / self._get_crypto_rate(transaction.currency),
            "expires_at": (datetime.utcnow() + timedelta(hours=1)).isoformat()
        }
    
    def _process_card_payment(
        self,
        transaction: Transaction,
        payment_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process direct card payment (fallback processor)
        """
        # This would integrate with a payment gateway
        # For demonstration, using a simple validation
        
        card_number = payment_details.get("card_number", "").replace(" ", "")
        
        if not self._validate_card_number(card_number):
            return {
                "success": False,
                "error": "Invalid card number"
            }
        
        # Mock successful payment
        return {
            "success": True,
            "transaction_id": f"card_{uuid.uuid4().hex}",
            "last_four": card_number[-4:],
            "card_brand": self._get_card_brand(card_number)
        }
    
    def process_refund(
        self,
        transaction_id: int,
        reason: str,
        amount: Optional[float] = None
    ) -> RefundRequest:
        """
        Process refund request
        """
        transaction = self.db.query(Transaction).filter(
            Transaction.id == transaction_id
        ).first()
        
        if not transaction:
            raise ValueError("Transaction not found")
        
        if transaction.status != TransactionStatus.COMPLETED:
            raise ValueError("Can only refund completed transactions")
        
        # Create refund request
        refund_request = RefundRequest(
            transaction_id=transaction_id,
            user_id=transaction.user_id,
            reason=reason,
            refund_amount=amount or transaction.total_amount,
            status="pending"
        )
        
        self.db.add(refund_request)
        
        # Process refund based on payment method
        if transaction.payment_method == PaymentMethod.STRIPE:
            result = self._refund_stripe_payment(transaction, amount)
        elif transaction.payment_method == PaymentMethod.PAYPAL:
            result = self._refund_paypal_payment(transaction, amount)
        else:
            result = {"success": False, "error": "Refund not supported for this payment method"}
        
        if result["success"]:
            refund_request.status = "approved"
            refund_request.processed_at = datetime.utcnow()
            refund_request.refund_transaction_id = result.get("refund_id")
            
            transaction.status = TransactionStatus.REFUNDED
            transaction.refunded_at = datetime.utcnow()
            
            # Remove enrollments
            enrollments = self.db.query(Enrollment).filter(
                Enrollment.transaction_id == transaction_id
            ).all()
            
            for enrollment in enrollments:
                enrollment.status = "expired"
                
                # Update course enrollment count
                course = self.db.query(Course).filter(
                    Course.id == enrollment.course_id
                ).first()
                if course:
                    course.enrollment_count = max(0, course.enrollment_count - 1)
        else:
            refund_request.status = "rejected"
            refund_request.admin_notes = result.get("error")
        
        self.db.commit()
        
        return refund_request
    
    def _refund_stripe_payment(
        self,
        transaction: Transaction,
        amount: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Process Stripe refund
        """
        try:
            refund = stripe.Refund.create(
                payment_intent=transaction.gateway_transaction_id,
                amount=int((amount or transaction.total_amount) * 100) if amount else None
            )
            
            return {
                "success": True,
                "refund_id": refund.id
            }
        except stripe.error.StripeError as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _refund_paypal_payment(
        self,
        transaction: Transaction,
        amount: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Process PayPal refund
        """
        try:
            sale = paypalrestsdk.Sale.find(transaction.gateway_transaction_id)
            
            refund = sale.refund({
                "amount": {
                    "total": str(amount or transaction.total_amount),
                    "currency": transaction.currency
                }
            })
            
            if refund.success():
                return {
                    "success": True,
                    "refund_id": refund.id
                }
            else:
                return {
                    "success": False,
                    "error": refund.error
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _calculate_coupon_discount(
        self,
        coupon: Coupon,
        subtotal: float,
        courses: List[Course]
    ) -> float:
        """
        Calculate discount amount based on coupon
        """
        # Check minimum purchase requirement
        if coupon.minimum_purchase_amount and subtotal < coupon.minimum_purchase_amount:
            return 0
        
        # Check course restrictions
        if coupon.applicable_course_ids:
            applicable_ids = set(json.loads(coupon.applicable_course_ids))
            course_ids = set(c.id for c in courses)
            if not course_ids.intersection(applicable_ids):
                return 0
        
        # Calculate discount
        if coupon.discount_type == "percentage":
            discount = subtotal * (coupon.discount_value / 100)
            if coupon.max_discount_amount:
                discount = min(discount, coupon.max_discount_amount)
        else:
            discount = min(coupon.discount_value, subtotal)
        
        return discount
    
    def _calculate_tax(self, amount: float, country: str) -> float:
        """
        Calculate tax based on country
        """
        tax_rate = self.tax_rates.get(country, self.tax_rates["default"])
        return amount * tax_rate
    
    def _generate_invoice(self, transaction: Transaction):
        """
        Generate invoice for transaction
        """
        invoice = Invoice(
            transaction_id=transaction.id,
            invoice_number=f"INV-{transaction.transaction_id}",
            invoice_date=datetime.utcnow()
        )
        
        self.db.add(invoice)
        
        # Generate PDF
        pdf_url = generate_invoice_pdf(transaction, invoice)
        invoice.pdf_url = pdf_url
        
        self.db.commit()
    
    def _send_payment_confirmation(
        self,
        user: User,
        transaction: Transaction,
        courses: List[Course]
    ):
        """
        Send payment confirmation email
        """
        course_list = "\n".join([f"- {c.title}" for c in courses])
        
        email_content = f"""
        Dear {user.first_name},
        
        Thank you for your purchase! Your payment has been successfully processed.
        
        Transaction ID: {transaction.transaction_id}
        Amount Paid: {transaction.currency} {transaction.total_amount:.2f}
        
        Courses Purchased:
        {course_list}
        
        You can now access your courses from your dashboard.
        
        Best regards,
        EUREKA Team
        """
        
        send_email(
            to=user.email,
            subject="Payment Confirmation - EUREKA",
            content=email_content
        )
    
    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID"""
        return f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    def _generate_crypto_address(self, currency: str) -> str:
        """Generate cryptocurrency address"""
        # This would integrate with actual crypto payment processor
        return f"{currency.lower()}:{uuid.uuid4().hex}"
    
    def _get_crypto_rate(self, currency: str) -> float:
        """Get cryptocurrency exchange rate"""
        # This would fetch real exchange rates
        rates = {
            "BTC": 45000,
            "ETH": 3000,
            "USDT": 1
        }
        return rates.get(currency, 1)
    
    def _validate_card_number(self, card_number: str) -> bool:
        """Validate card number using Luhn algorithm"""
        if not card_number.isdigit():
            return False
        
        digits = [int(d) for d in card_number]
        checksum = 0
        
        for i in range(len(digits) - 2, -1, -2):
            digits[i] *= 2
            if digits[i] > 9:
                digits[i] -= 9
        
        return sum(digits) % 10 == 0
    
    def _get_card_brand(self, card_number: str) -> str:
        """Determine card brand from number"""
        if card_number.startswith("4"):
            return "Visa"
        elif card_number.startswith(("51", "52", "53", "54", "55")):
            return "Mastercard"
        elif card_number.startswith(("34", "37")):
            return "Amex"
        else:
            return "Unknown"