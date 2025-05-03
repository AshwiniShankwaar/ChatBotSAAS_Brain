from fastapi import APIRouter,UploadFile,File,HTTPException,Form
from app.schemas.chatbot import ChatbotCreateRequest
from app.services.chatbot_create import create_chatbot_task
from Logger import get_logger,getlogger
from typing import Optional
from app.utils_file import save_data,clean_temp_folder
from app.Main import model
logger = get_logger()
router = APIRouter()

#if there is error log in app logger else chatbot related logs should be in chatbot related log files
# @router.post("/create_chatbot")
async def create_chatbot(
                         payload:ChatbotCreateRequest,
                         files:Optional[list[UploadFile]]=File(default=[]),
                         weblinks:Optional[list[dict[str]]]=None):
    #request recived
    logger.info(f"creating chatbot {payload.chatbot_name}, chatbot id: {payload.chatbot_id}")
    botlogger = getlogger(payload.chatbot_id)
    #first upload the files in the temp_dir for client's chatbot
    botlogger.info(f"saving files in temp_dir for chatbot id:{payload.chatbot_id} of client: {payload.client_id}")
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