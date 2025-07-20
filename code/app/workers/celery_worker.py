from celery import Celery
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.chatroom import Message


import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

celery = Celery("gemini_tasks",
    broker=os.getenv("CELERY_BROKER_URL", "pyamqp://guest@localhost//"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "rpc://")
)

@celery.task
def call_gemini_api(message_id: int, prompt: str):
    db: Session = SessionLocal()
    try:
        # Get the message row
        message = db.query(Message).filter(Message.id == message_id).first()
        if not message:
            return f"Message ID {message_id} not found"

        # Generate Gemini response
        response = model.generate_content(prompt)
        message.ai_response = response.text if response and hasattr(response, 'text') else "No response from Gemini"

        # Save response
        db.commit()
        return message.ai_response

    except Exception as e:
        return f"Error during Gemini call: {str(e)}"

    finally:
        db.close()