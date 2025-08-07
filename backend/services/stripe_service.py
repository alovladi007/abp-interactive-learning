import stripe
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from config.settings import settings
import logging
from pydantic import BaseModel
import json

logger = logging.getLogger(__name__)

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

class PriceConfig(BaseModel):
    credits: int
    price_cents: int
    currency: str = "usd"
    name: str
    description: Optional[str] = None

class PaymentService:
    def __init__(self):
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        
        # Credit packages
        self.credit_packages = {
            "starter": PriceConfig(
                credits=100,
                price_cents=999,  # $9.99
                name="Starter Pack",
                description="100 credits for video generation"
            ),
            "pro": PriceConfig(
                credits=500,
                price_cents=3999,  # $39.99
                name="Pro Pack",
                description="500 credits with 20% savings"
            ),
            "enterprise": PriceConfig(
                credits=2000,
                price_cents=14999,  # $149.99
                name="Enterprise Pack",
                description="2000 credits with 25% savings"
            )
        }
        
        # Credit costs per feature
        self.credit_costs = {
            "video_generation_per_second": 2,
            "voice_generation_per_minute": 5,
            "music_generation_per_minute": 3,
            "upscaling_2x": 10,
            "upscaling_4x": 20,
            "frame_interpolation": 15,
            "quality_check": 1
        }
    
    async def create_checkout_session(
        self,
        user_id: str,
        package_key: str,
        success_url: str,
        cancel_url: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Create Stripe checkout session for credit purchase"""
        
        if package_key not in self.credit_packages:
            raise ValueError(f"Invalid package: {package_key}")
        
        package = self.credit_packages[package_key]
        
        # Create metadata
        session_metadata = {
            "user_id": user_id,
            "package_key": package_key,
            "credits": str(package.credits)
        }
        if metadata:
            session_metadata.update(metadata)
        
        try:
            # Create checkout session
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[{
                    "price_data": {
                        "currency": package.currency,
                        "product_data": {
                            "name": package.name,
                            "description": package.description,
                            "metadata": {
                                "type": "credits",
                                "amount": str(package.credits)
                            }
                        },
                        "unit_amount": package.price_cents,
                    },
                    "quantity": 1,
                }],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=user_id,
                metadata=session_metadata,
                payment_intent_data={
                    "metadata": session_metadata
                }
            )
            
            logger.info(f"Checkout session created: {session.id} for user {user_id}")
            
            return {
                "session_id": session.id,
                "checkout_url": session.url,
                "expires_at": datetime.fromtimestamp(session.expires_at).isoformat()
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error: {e}")
            raise
    
    async def create_subscription(
        self,
        user_id: str,
        price_id: str,
        trial_days: int = 0
    ) -> Dict[str, Any]:
        """Create subscription for recurring credits"""
        
        try:
            # Create or get customer
            customer = await self._get_or_create_customer(user_id)
            
            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{"price": price_id}],
                trial_period_days=trial_days,
                metadata={
                    "user_id": user_id
                }
            )
            
            return {
                "subscription_id": subscription.id,
                "status": subscription.status,
                "current_period_end": datetime.fromtimestamp(
                    subscription.current_period_end
                ).isoformat()
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Subscription creation error: {e}")
            raise
    
    async def handle_webhook(
        self,
        payload: bytes,
        signature: str
    ) -> Dict[str, Any]:
        """Handle Stripe webhook events"""
        
        try:
            # Verify webhook signature
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                self.webhook_secret
            )
            
            logger.info(f"Webhook received: {event['type']}")
            
            # Handle different event types
            if event["type"] == "checkout.session.completed":
                return await self._handle_checkout_completed(event["data"]["object"])
            
            elif event["type"] == "payment_intent.succeeded":
                return await self._handle_payment_succeeded(event["data"]["object"])
            
            elif event["type"] == "invoice.payment_succeeded":
                return await self._handle_invoice_paid(event["data"]["object"])
            
            elif event["type"] == "customer.subscription.deleted":
                return await self._handle_subscription_deleted(event["data"]["object"])
            
            else:
                logger.info(f"Unhandled event type: {event['type']}")
                return {"status": "unhandled"}
            
        except ValueError as e:
            logger.error(f"Invalid payload: {e}")
            raise
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"Invalid signature: {e}")
            raise
    
    async def _handle_checkout_completed(
        self,
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle successful checkout"""
        
        user_id = session["client_reference_id"]
        metadata = session.get("metadata", {})
        credits = int(metadata.get("credits", 0))
        
        logger.info(f"Checkout completed for user {user_id}: {credits} credits")
        
        # Here you would update the user's credit balance in your database
        # For now, returning the result
        return {
            "type": "checkout_completed",
            "user_id": user_id,
            "credits": credits,
            "payment_intent": session.get("payment_intent"),
            "amount_total": session.get("amount_total")
        }
    
    async def _handle_payment_succeeded(
        self,
        payment_intent: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle successful payment"""
        
        metadata = payment_intent.get("metadata", {})
        user_id = metadata.get("user_id")
        
        return {
            "type": "payment_succeeded",
            "user_id": user_id,
            "amount": payment_intent["amount"],
            "currency": payment_intent["currency"]
        }
    
    async def _handle_invoice_paid(
        self,
        invoice: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle paid invoice (subscription renewal)"""
        
        subscription_id = invoice["subscription"]
        customer_id = invoice["customer"]
        
        # Get subscription details
        subscription = stripe.Subscription.retrieve(subscription_id)
        user_id = subscription.metadata.get("user_id")
        
        return {
            "type": "subscription_renewed",
            "user_id": user_id,
            "subscription_id": subscription_id,
            "amount": invoice["amount_paid"],
            "period_end": datetime.fromtimestamp(
                subscription.current_period_end
            ).isoformat()
        }
    
    async def _handle_subscription_deleted(
        self,
        subscription: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle subscription cancellation"""
        
        user_id = subscription["metadata"].get("user_id")
        
        return {
            "type": "subscription_cancelled",
            "user_id": user_id,
            "subscription_id": subscription["id"],
            "cancelled_at": datetime.fromtimestamp(
                subscription["canceled_at"]
            ).isoformat()
        }
    
    async def _get_or_create_customer(
        self,
        user_id: str,
        email: Optional[str] = None,
        name: Optional[str] = None
    ) -> Any:
        """Get or create Stripe customer"""
        
        # Search for existing customer
        customers = stripe.Customer.list(
            limit=1,
            email=email
        ) if email else None
        
        if customers and customers.data:
            return customers.data[0]
        
        # Create new customer
        customer = stripe.Customer.create(
            email=email,
            name=name,
            metadata={"user_id": user_id}
        )
        
        return customer
    
    async def calculate_credit_cost(
        self,
        video_duration: int,
        features: Dict[str, Any]
    ) -> int:
        """Calculate total credit cost for video generation"""
        
        total_cost = 0
        
        # Base video generation cost
        total_cost += video_duration * self.credit_costs["video_generation_per_second"]
        
        # Voice-over cost
        if features.get("voice_enabled"):
            voice_duration = features.get("voice_duration", video_duration)
            voice_minutes = (voice_duration + 59) // 60  # Round up to minutes
            total_cost += voice_minutes * self.credit_costs["voice_generation_per_minute"]
        
        # Music cost
        if features.get("music_enabled"):
            music_duration = features.get("music_duration", video_duration)
            music_minutes = (music_duration + 59) // 60
            total_cost += music_minutes * self.credit_costs["music_generation_per_minute"]
        
        # Post-processing costs
        if features.get("upscale_2x"):
            total_cost += self.credit_costs["upscaling_2x"]
        elif features.get("upscale_4x"):
            total_cost += self.credit_costs["upscaling_4x"]
        
        if features.get("frame_interpolation"):
            total_cost += self.credit_costs["frame_interpolation"]
        
        # Quality check
        if features.get("quality_check", True):
            total_cost += self.credit_costs["quality_check"]
        
        return total_cost
    
    async def create_usage_record(
        self,
        subscription_id: str,
        quantity: int,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Record usage for metered billing"""
        
        try:
            # Get subscription item
            subscription = stripe.Subscription.retrieve(subscription_id)
            subscription_item_id = subscription["items"]["data"][0]["id"]
            
            # Create usage record
            usage_record = stripe.SubscriptionItem.create_usage_record(
                subscription_item_id,
                quantity=quantity,
                timestamp=int((timestamp or datetime.utcnow()).timestamp())
            )
            
            return {
                "id": usage_record.id,
                "quantity": usage_record.quantity,
                "subscription_item": usage_record.subscription_item
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Usage record error: {e}")
            raise
    
    async def get_customer_invoices(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get customer's invoice history"""
        
        try:
            # Get customer
            customers = stripe.Customer.list(
                limit=1,
                query=f'metadata["user_id"]:"{user_id}"'
            )
            
            if not customers.data:
                return []
            
            customer_id = customers.data[0].id
            
            # Get invoices
            invoices = stripe.Invoice.list(
                customer=customer_id,
                limit=limit
            )
            
            return [
                {
                    "id": invoice.id,
                    "amount": invoice.amount_paid,
                    "currency": invoice.currency,
                    "status": invoice.status,
                    "created": datetime.fromtimestamp(invoice.created).isoformat(),
                    "invoice_pdf": invoice.invoice_pdf
                }
                for invoice in invoices.data
            ]
            
        except stripe.error.StripeError as e:
            logger.error(f"Invoice retrieval error: {e}")
            raise
    
    async def create_refund(
        self,
        payment_intent_id: str,
        amount: Optional[int] = None,
        reason: str = "requested_by_customer"
    ) -> Dict[str, Any]:
        """Create refund for a payment"""
        
        try:
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=amount,  # None means full refund
                reason=reason
            )
            
            return {
                "id": refund.id,
                "amount": refund.amount,
                "currency": refund.currency,
                "status": refund.status,
                "created": datetime.fromtimestamp(refund.created).isoformat()
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Refund error: {e}")
            raise
    
    def get_credit_packages(self) -> Dict[str, Dict[str, Any]]:
        """Get available credit packages"""
        
        packages = {}
        for key, package in self.credit_packages.items():
            packages[key] = {
                "name": package.name,
                "credits": package.credits,
                "price": package.price_cents / 100,
                "currency": package.currency,
                "description": package.description,
                "price_per_credit": round(package.price_cents / package.credits / 100, 3)
            }
        
        return packages

# Singleton instance
payment_service = PaymentService()