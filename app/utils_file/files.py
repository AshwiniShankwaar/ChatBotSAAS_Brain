import json
import os
import shutil
bash_path = "files"
from Logger.logger import logger
def save_data(client_id,chatbot_id,files,weblinks)->str:
    logger.info(f"creating temp folder for chatbot {chatbot_id}")
    temp_dir = f"./{bash_path}/{client_id}_{chatbot_id}"
    os.makedirs(temp_dir, exist_ok=True)
    logger.info(f"temp folder created for chatbot {chatbot_id}, path: {temp_dir}")

    #first store all the files in the temp folder
    for file in files:
        file_path = os.path.join(temp_dir,file.filename)
        with open(file_path,"wb") as f:
            shutil.copyfileobj(file.file,f)
        logger.info(f"Stored file: {file.filename} in {temp_dir}")

    # Store weblinks as JSON
    if weblinks and isinstance(weblinks, dict):
        weblink_path = os.path.join(temp_dir, "weblinks.json")
        with open(weblink_path, "w", encoding="utf-8") as f:
            json.dump(weblinks, f, indent=2)
        logger.info(f"Stored weblinks in {weblink_path}")

    logger.info(f"All docmuents are uploaded to folder: {temp_dir}.")
    return temp_dir

def clean_temp_folder(temp_dir:str):
    try:
        shutil.rmtree(temp_dir)
        logger.info(f"Temporary folder cleaned up: {temp_dir}")
    except Exception as e:
        logger.error(f"Failed to delete temp folder {temp_dir}: {str(e)}")