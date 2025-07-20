from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user import User
from app.core.security import decode_token
from app.schemas.subscription import SubscriptionStatus
from app.services.stripe_service import create_checkout_session, verify_and_update_subscription
import stripe
import os

router = APIRouter(prefix="/subscription")

# OAuth2 token dependency
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/pro")
def subscribe_pro(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)
    user_id = int(payload["sub"])
    checkout_url = create_checkout_session(user_id)
    return {"checkout_url": checkout_url}

@router.get("/status", response_model=SubscriptionStatus)
def get_subscription_status(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = int(decode_token(token)["sub"])
    user = db.query(User).filter_by(id=user_id).first()
    return {"subscription": user.subscription}

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv("STRIPE_WEBHOOK_SECRET")
        )
        verify_and_update_subscription(event, db, User)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"status": "success"}