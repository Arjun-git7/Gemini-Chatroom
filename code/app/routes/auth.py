from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserSignup, OTPVerify, Token
from app.models.user import User
from app.core.security import create_access_token
from app.db.database import get_db
import random
from pydantic import BaseModel

router = APIRouter()

class SignupRequest(BaseModel):
    mobile: str

@router.post("/signup")
def signup(data: UserSignup, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile=data.mobile).first()
    otp = str(random.randint(100000, 999999))
    if user:
        user.otp = otp
    else:
        user = User(mobile=data.mobile, otp=otp)
        db.add(user)
    db.commit()
    return {"otp": otp}  # Return OTP in response (mocked)

@router.post("/verify-otp", response_model=Token)
def verify_otp(data: OTPVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(mobile=data.mobile, otp=data.otp).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    user.is_verified = True
    db.commit()
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token}
