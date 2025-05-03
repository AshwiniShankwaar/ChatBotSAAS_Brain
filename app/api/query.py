from app.schemas.query import QueryRequest
from Logger import get_logger,getlogger
from app.Main import model,pc
logger = get_logger()
async def query_request(payload:QueryRequest):
    botlogger = getlogger(payload.chatbot_id)
    botlogger.info(f"recevied query..{payload.query}")
    try:
        query_respose = process_query(payload,botlogger,model,pc)
        botlogger.info("query processed successfully")
        return {
            "response":query_respose
        }
    except Exception as e:
        logger.error(f"exception occered while processing query in chatbot: {payload.chatbot_id}")
        botlogger.error(f"error while processing request query: {payload.query}")
        raise HTTPException(status_code=500,detail=str(ex))