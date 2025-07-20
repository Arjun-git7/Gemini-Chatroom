from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatroomCreate(BaseModel):
    name: str

class MessageCreate(BaseModel):
    message: str

class MessageOut(BaseModel):
    id: int
    user_message: str
    ai_response: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True

class ChatroomOut(BaseModel):
    id: int
    name: str
    created_at: datetime
    messages: List[MessageOut] = []

    class Config:
        orm_mode = True