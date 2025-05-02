import os
from datetime import datetime
from Logger.chatbotLogger import create_chatbot_log_dir,getlogger

chatbot_id = "123abcd456"
BASE_LOG_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", "chatBot_Logs"))
file_path = os.path.abspath(os.path.join(BASE_LOG_DIR,chatbot_id))
today = datetime.now().strftime("%Y-%m-%d")
def test_create_log_dir():
    create_chatbot_log_dir(chatbot_id)

    #check
    assert os.path.exists(file_path)

def test_chatbot_logger():
    logger = getlogger(chatbot_id)

    assert os.path.exists(os.path.join(file_path,f"{today}.log"))

def test_logging():
    logger = getlogger(chatbot_id)
    logger.info("hello from test")

