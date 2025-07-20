from sqlalchemy import Column, Integer, String, Boolean
from app.db.database import Base
from sqlalchemy import Boolean

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    mobile = Column(String, unique=True, index=True)
    otp = Column(String)
    is_verified = Column(Boolean, default=False)
    subscription = Column(String, default="basic")  # basic or pro
