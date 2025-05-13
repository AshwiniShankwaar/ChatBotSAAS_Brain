from fastapi import APIRouter,UploadFile,File,HTTPException,Form
from app.schemas.chatbot import ChatbotCreateRequest
from app.schemas.updateChatbot import ChatbotUpdateRequest
from app.services.chatbot_create import create_chatbot_task,update_chatbot_task,deleteChatBotData
from Logger import get_logger,getlogger
from typing import Optional,List,Dict,Any
from app.utils_file import save_data,clean_temp_folder
import json
logger = get_logger()
router = APIRouter()

from embeddedModel.huggingfaceModel import embedding_model as model

#if there is error log in app logger else chatbot related logs should be in chatbot related log files
@router.post("/create_chatbot")
async def create_chatbot(
                         payload_data:str=Form(...),
                         files:Optional[list[UploadFile]]=File(default_factory=list),
                         weblinks_str: Optional[str] = Form(default=None)):
    try:
        # Parse the payload string into a ChatbotCreateRequest object
        chatbot_request = json.loads(payload_data)
        payload = ChatbotCreateRequest(**chatbot_request)
        logger.info(payload)
        logger.info(weblinks_str)
        weblinks: Optional[List[Dict[str, Any]]] = json.loads(weblinks_str) if weblinks_str else []
        logger.info(weblinks)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON in payload")
    except Exception as e:
        logger.error(f"Error processing payload: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing payload: {e}")
    #request recived
    logger.info(f"creating chatbot {payload.chatbot_name}, chatbot id: {payload.chatbot_id}")
    botlogger = getlogger(f"{payload.client_id}_{payload.chatbot_id}")
    #first upload the files in the temp_dir for client's chatbot
    botlogger.info(f"saving files in temp_dir for chatbot id:{payload.chatbot_id} of client: {payload.client_id}")
    # delete the folder if it is there and also remove the bm25model and also the namespace

    files_dir = save_data(payload.client_id,payload.chatbot_id,files,weblinks,botlogger)

    try:
        result = create_chatbot_task(payload,files_dir,botlogger,model)
        botlogger.info(f"chatbot {payload.chatbot_name}"
                    f" of client {payload.client_id}"
                    f" is created and the namespace is"
                    f" {result}")
        clean_temp_folder(files_dir,botlogger)
        return {
            "message":f"ChatBot {payload.chatbot_name} created successfully",
            "namespace":result
        }
    except Exception as ex:
        logger.error(f"Http exception is occured check at create_chatbot.py file {ex}")
        # raise HTTPException(status_code=500,detail=str(ex))


@router.post("/update_chatbot")
async def update_chatbot(
                         payload:str=Form(...),
                         files:Optional[list[UploadFile]]=File(default_factory=list),
                         weblinks: Optional[str] = Form(default=None)):
    try:
        # Parse the payload string into a ChatbotCreateRequest object
        chatbot_request = json.loads(payload)
        payload = ChatbotUpdateRequest(**chatbot_request)
        logger.info(payload)
        logger.info(weblinks)
        weblinks: Optional[List[Dict[str, Any]]] = json.loads(weblinks) if weblinks else []
        logger.info(weblinks)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding payload: {e}")
        raise HTTPException(status_code=400, detail="Invalid JSON in payload")
    except Exception as e:
        logger.error(f"Error processing payload: {e}")
        raise HTTPException(status_code=400, detail=f"Error processing payload: {e}")
    #request recived
    logger.info(f"creating chatbot {payload.chatbot_name}, chatbot id: {payload.chatbot_id}")
    botlogger = getlogger(f"{payload.client_id}_{payload.chatbot_id}")
    #first upload the files in the temp_dir for client's chatbot

    botlogger.info(f"saving files in temp_dir for chatbot id:{payload.chatbot_id} of client: {payload.client_id}")
    files_dir = save_data(payload.client_id,payload.chatbot_id,files,weblinks,botlogger)

    try:
        result = update_chatbot_task(payload,files_dir,botlogger,model)
        botlogger.info(f"chatbot {payload.chatbot_name}"
                    f" of client {payload.client_id}"
                    f" is created and the namespace is"
                    f" {result}")
        clean_temp_folder(files_dir,botlogger)
        return {
            "message":f"ChatBot {payload.chatbot_name} updated successfully",
            "namespace":result
        }
    except Exception as ex:
        logger.error(f"Http exception is occured check at create_chatbot.py file {ex}")
        # raise HTTPException(status_code=500,detail=str(ex))

@router.delete("/delete_chatbot")
async def delete_chatbot(request: ChatbotUpdateRequest):
    try:
        # Simulate delete logic (e.g., remove vector DB entries, files, etc.)
        logger.info(f"Deleting chatbot: {request.chatbot_id} from namespace {request.namespace}")

        # TODO: Actual deletion logic goes here
        deleteChatBotData(namespace=request.namespace)
        return JSONResponse(
            status_code=200,
            content={"message": f"Chatbot {request.chatbot_id} deleted successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting chatbot: {str(e)}")