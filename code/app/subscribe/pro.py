import stripe
from fastapi import Depends
from app.models.user import User
from app.core.security import decode_token

stripe.api_key = os.getenv("STRIPE_SECRET")

@router.post("/subscribe/pro")
def subscribe_pro(token: str = Depends(oauth2_scheme)):
    user_id = decode_token(token)["sub"]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': os.getenv("STRIPE_PRICE_ID"),
            'quantity': 1,
        }],
        mode='subscription',
        success_url="http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="http://localhost:8000/cancel",
        metadata={"user_id": user_id}
    )
    return {"checkout_url": session.url}