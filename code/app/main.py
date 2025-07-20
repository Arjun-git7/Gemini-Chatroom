from fastapi import FastAPI
from app.routes import auth, chatroom, subscription
from app.routes import stripe_routes
from app.api import routes_chatroom


app = FastAPI()

app.include_router(auth.router, prefix="/auth")
app.include_router(stripe_routes.router)
app.include_router(subscription.router)
app.include_router(chatroom.router, prefix="/chatroom")
app.include_router(routes_chatroom.router)
@app.get("/")
def root():
    return {"message": "Gemini Backend API running"}