from sqlalchemy.orm import Session
from app.models.chatroom import Chatroom, Message
from app.schemas.chat import ChatroomCreate, MessageCreate
from app.workers.celery_worker import call_gemini_api

def create_chatroom(db: Session, user_id: int, chatroom_data: ChatroomCreate):
    chatroom = Chatroom(name=chatroom_data.name, user_id=user_id)
    db.add(chatroom)
    db.commit()
    db.refresh(chatroom)
    return chatroom

def get_user_chatrooms(db: Session, user_id: int):
    return db.query(Chatroom).filter(Chatroom.user_id == user_id).all()

def get_chatroom(db: Session, chatroom_id: int):
    return db.query(Chatroom).filter(Chatroom.id == chatroom_id).first()

def send_message(db: Session, chatroom_id: int, msg_data: MessageCreate):
    message = Message(chatroom_id=chatroom_id, user_message=msg_data.message)
    db.add(message)
    db.commit()
    db.refresh(message)

    # Send async task to Gemini (mocked)
    call_gemini_api.delay(message.id, msg_data.message)

    return message