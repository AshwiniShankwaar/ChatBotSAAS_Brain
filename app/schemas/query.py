from pydantic import BaseModel
from typing import List, Dict, Optional

class QueryRequest(BaseModel):
    query: str
    past_msg: List[Dict[str, str]]  # Format: [{"user": "..."}, {"ai": "..."}]
    client_id: str
    chatbot_id: str
    chatbot_config: Optional[Dict[str, str]] = {}  # ex: {"temp": 0.7, "agent_role": "financial analyst"}
