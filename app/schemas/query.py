from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    query: str
    past_msg: Optional[List[Dict[str, str]]] = None   # Format: [{"user": "..."}, {"ai": "..."}]
    client_id: str
    chatbot_id: str
    agent_role: Optional[str] = None
