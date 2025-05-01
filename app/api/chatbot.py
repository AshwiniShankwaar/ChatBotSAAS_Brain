from fastapi import APIRouter,UploadFile,File,HTTPException
from app.schemas.chatbot import ChatbotCreateRequest
from app.services.chatbot_create import create_chatbot_pipeline
from Logger.logger import logger
from typing import Optional
from app.utils_file.files import save_data,clean_temp_folder

router = APIRouter()

async def create_chatbot(payload:ChatbotCreateRequest,
                         files:Optional[list[UploadFile]]=File(default=[]),
                         weblinks:Optional[dict[str]]=None):

    files_dir = save_data(payload.client_id,payload.chatbot_id,files,weblinks)

    try:
        result = create_chatbot_pipeline(payload,files_dir)
        logger.info(f"chatbot {payload.chatbot_name}"
                    f"of client {payload.client_id}"
                    f"is created and the namespace is"
                    f"{result}")
        clean_temp_folder(files_dir)
        return {
            "message":f"ChatBot {payload.chatbot_name} created successfully",
            "namespace":result
        }
    except Exception as ex:
        logger.error(f"Http exception is occured check at create_chatbot.py file {ex}")
        raise HTTPException(status_code=500,detail=str(ex))