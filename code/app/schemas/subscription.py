from pydantic import BaseModel

class SubscriptionStatus(BaseModel):
    subscription: str