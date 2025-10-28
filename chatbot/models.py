import datetime
from pydantic import BaseModel

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    timestamp: datetime   

    model_config = {
        "arbitrary_types_allowed": True
    }     