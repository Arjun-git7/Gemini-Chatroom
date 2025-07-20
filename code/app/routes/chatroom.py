from fastapi import APIRouter, HTTPException
from app.workers.celery_worker import call_gemini_api
from pydantic import BaseModel

router = APIRouter()

class MessageRequest(BaseModel):
    prompt: str

@router.post("/{chatroom_id}/message")
def send_message(chatroom_id: int, request: MessageRequest):
    task = call_gemini_api.delay(request.prompt)  # Fire async task
    return {
        "status": "processing",
        "task_id": task.id
    }