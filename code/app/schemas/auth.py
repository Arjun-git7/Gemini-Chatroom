from pydantic import BaseModel

class UserSignup(BaseModel):
    mobile: str

class OTPVerify(BaseModel):
    mobile: str
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"