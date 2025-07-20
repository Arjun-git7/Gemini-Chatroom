import stripe
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from app.models.user import User

load_dotenv()


stripe.api_key = os.getenv("STRIPE_SECRET")

def create_checkout_session(user_id: int) -> str:
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": os.getenv("STRIPE_PRICE_ID"),  # Make sure this exists in your .env
                    "quantity": 1
                }
            ],
            mode="subscription",
            success_url="http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/cancel",
            metadata={"user_id": str(user_id)}
        )
        return session.url
    except Exception as e:
        raise Exception(f"Stripe Checkout Session creation failed: {e}")


def verify_and_update_subscription(event: dict, db: Session):
    try:
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            user_id = session["metadata"]["user_id"]
            user = db.query(User).filter_by(id=int(user_id)).first()

            if user:
                user.subscription = "pro"
                db.commit()
    except Exception as e:
        raise Exception(f"Error handling Stripe webhook: {e}")

def parse_webhook(payload, sig_header):
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        return event
    except stripe.error.SignatureVerificationError as e:
        print("Webhook signature verification failed:", e)
        return None