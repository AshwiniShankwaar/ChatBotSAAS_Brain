from pydantic import BaseModel, HttpUrl
from typing import Optional

class ChatbotCreateRequest(BaseModel):
    client_id: str
    chatbot_id: str
    chatbot_name: str
    chatbot_description: Optional[str] = None
    agent_role: Optional[str] = "assistant"
    temprature:Optional[float]=0.8
