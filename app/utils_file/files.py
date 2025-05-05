import json
import os
import shutil
cwd = os.getcwd()
abs_path = os.path.abspath(f"{cwd}")
bash_path = "files"
from Logger import get_logger
logger = get_logger()
def save_data(client_id,chatbot_id,files,weblinks,botlogger)->str:

    botlogger.info(f"creating temp folder")
    temp_dir = f"{abs_path}/{bash_path}/{client_id}_{chatbot_id}"
    try:
        os.makedirs(temp_dir, exist_ok=True)
        botlogger.info(f"temp folder created")
    except Exception as e:
        botlogger.error("error while creating temp folder")
        logger.error(f"error while creating temp folder for client "
                     f"{client_id} and chatbot {chatbot_id}")
        raise HTTPException(  # Re-raise as HTTPException
            status_code=500,
            detail=f"Failed to create folder: {str(e)}"
        )

    #first store all the files in the temp folder
    botlogger.info(len(files))
    if len(files) != 0:
        try:
            for file in files:
                file_path = os.path.join(temp_dir,file.filename)
                with open(file_path,"wb") as f:
                    shutil.copyfileobj(file.file,f)
                botlogger.info(f"Stored file: {file.filename} in {temp_dir}")
        except Exception as e:
            botlogger.error("error while storing files")
            logger.error(f"error while storing files in temp folder for client "
                         f"{client_id} and chatbot {chatbot_id}")
            raise HTTPException(  # Re-raise as HTTPException
                status_code=500,
                detail=f"Failed to store file: {str(e)}"
            )
    botlogger.info(weblinks)
    if len(weblinks) !=0:
        try:
            # Store weblinks as JSON
            if weblinks and isinstance(weblinks, list):
                weblink_path = os.path.join(temp_dir, "weblinks.json")
                with open(weblink_path, "w", encoding="utf-8") as f:
                    json.dump(weblinks, f, indent=2)
                botlogger.info(f"Stored weblinks in {weblink_path}")
            botlogger.info(f"All linkes are saved in weblink.json and uploaded to folder: {temp_dir}.")

        except Exception as e:
            botlogger.error("error while storing weblinks files")
            logger.error(f"error while storing weblinkes files in temp folder for client "
                         f"{client_id} and chatbot {chatbot_id}")
            raise HTTPException(  # Re-raise as HTTPException
                status_code=500,
                detail=f"Failed to store files: {str(e)}"
            )
    botlogger.info(f"All docmuents are uploaded to folder: {temp_dir}.")
    return temp_dir

def clean_temp_folder(temp_dir:str,botlogger):
    try:
        shutil.rmtree(temp_dir)
        botlogger.info(f"Temporary folder cleaned up: {temp_dir}")
    except Exception as e:
        logger.error(f"Failed to delete temp folder {temp_dir}: {str(e)}")