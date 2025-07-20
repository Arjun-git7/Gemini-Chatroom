from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.chat import ChatroomCreate, ChatroomOut, MessageCreate, MessageOut
from app.services.chat import create_chatroom, get_user_chatrooms, get_chatroom, send_message
from app.core.security import get_current_user

router = APIRouter()

@router.post("/chatroom", response_model=ChatroomOut)
def create_chatroom_api(data: ChatroomCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_chatroom(db, user["id"], data)

@router.get("/chatroom", response_model=list[ChatroomOut])
def list_chatrooms_api(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_user_chatrooms(db, user["id"])

@router.get("/chatroom/{chatroom_id}", response_model=ChatroomOut)
def get_chatroom_api(chatroom_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chatroom = get_chatroom(db, chatroom_id)
    if not chatroom or chatroom.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    return chatroom

@router.post("/chatroom/{chatroom_id}/message", response_model=MessageOut)
def send_message_api(chatroom_id: int, data: MessageCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chatroom = get_chatroom(db, chatroom_id)
    if not chatroom or chatroom.user_id != user["id"]:
        raise HTTPException(status_code=404, detail="Chatroom not found")
    return send_message(db, chatroom_id, data)