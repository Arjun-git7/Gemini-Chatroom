from fastapi import APIRouter, Depends, Request, HTTPException
from app.services.stripe_service import create_checkout_session, parse_webhook
from app.models.user import User
from app.db.database import SessionLocal
from sqlalchemy.orm import Session
from app.core.security import get_current_user
import json

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/subscribe/pro")
def subscribe(user: User = Depends(get_current_user)):
    session = create_checkout_session(user.id)
    return {"checkout_url": session.url}

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = parse_webhook(payload, sig_header)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session['metadata']['user_id']
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user:
            user.subscription = True
            db.commit()
    return {"status": "success"}

@router.get("/subscription/status")
def subscription_status(user: User = Depends(get_current_user)):
    return {"is_pro": user.subscription }