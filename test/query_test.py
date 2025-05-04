from app.api.query import query_request
from app.schemas.query import QueryRequest
import asyncio
from Logger import get_logger

logger = get_logger()
def test_query():
    q = "What is uim"
    payload = QueryRequest(
        query="What is uim",
        past_msg=None,
        client_id="test_client",
        chatbot_id="test_bot",
        agent_role="helper"
    )

    # Since query_request is async, we need to run it in an event loop
    result = asyncio.run(query_request(payload))
    logger.info(f"answer: {result}")
