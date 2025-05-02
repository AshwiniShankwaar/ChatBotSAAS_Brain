import json
import os
import shutil
cwd = os.getcwd()
abs_path = os.path.abspath(f"{cwd}/..")
bash_path = "files"
from Logger import get_logger
logger = get_logger()
def save_data(client_id,chatbot_id,files,weblinks,botlogger)->str:
    botlogger.info(f"creating temp folder")
    temp_dir = f"{abs_path}/{bash_path}/{client_id}_{chatbot_id}"
    os.makedirs(temp_dir, exist_ok=True)
    botlogger.info(f"temp folder created")

    #first store all the files in the temp folder
    for file in files:
        file_path = os.path.join(temp_dir,file.filename)
        with open(file_path,"wb") as f:
            shutil.copyfileobj(file.file,f)
        botlogger.info(f"Stored file: {file.filename} in {temp_dir}")

    # Store weblinks as JSON
    if weblinks and isinstance(weblinks, dict):
        weblink_path = os.path.join(temp_dir, "weblinks.json")
        with open(weblink_path, "w", encoding="utf-8") as f:
            json.dump(weblinks, f, indent=2)
        botlogger.info(f"Stored weblinks in {weblink_path}")
    botlogger.info(f"All docmuents are uploaded to folder: {temp_dir}.")
    return temp_dir

def clean_temp_folder(temp_dir:str,botlogger):
    try:
        shutil.rmtree(temp_dir)
        botlogger.info(f"Temporary folder cleaned up: {temp_dir}")
    except Exception as e:
        logger.error(f"Failed to delete temp folder {temp_dir}: {str(e)}")