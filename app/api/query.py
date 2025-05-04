import json

from app.schemas.query import QueryRequest
from app.services.chatbot_query import process_query
from Logger import get_logger,getlogger
from fastapi import APIRouter, HTTPException,Form
logger = get_logger()
router = APIRouter()

from embeddedModel.huggingfaceModel import embedding_model as model
from pinecone import Pinecone
import os
pine_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pine_api_key)

@router.post("/ask")
async def query_request(payload_data:str=Form(...)):
    chatbot_request = json.loads(payload_data)
    payload = QueryRequest(**chatbot_request)
    botlogger = getlogger(payload.chatbot_id)
    botlogger.info(f"recevied query..{payload.query}")
    try:
        query_respose = process_query(payload,botlogger,model,pc)
        botlogger.info("query processed successfully")
        return {
            "response":query_respose
        }
    except Exception as ex:
        logger.error(f"exception occered while processing query in chatbot: {payload.chatbot_id}")
        botlogger.error(f"error while processing request query: {payload.query}")
        raise HTTPException(status_code=500,detail=str(ex))