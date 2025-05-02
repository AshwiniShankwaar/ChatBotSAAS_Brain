import os
import logging
from datetime import datetime
from Logger.logger_exception.ChatBot_Log_file_not_found import chatBotFileNotFoundError
from Logger.logger import get_logger

logger = get_logger()

BASE_LOG_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", "chatBot_Logs"))

def create_chatbot_log_dir(chatbot_id: str):
    chatbot_log_path = os.path.join(BASE_LOG_DIR, chatbot_id)
    try:
        os.makedirs(chatbot_log_path, exist_ok=True)
    except Exception as e:
        err_msg = f"Error creating log folder for chatbot ID: {chatbot_id}"
        logger.error(err_msg)
        raise chatBotFileNotFoundError(err_msg, chatbot_id)

class ChatBotLogger:
    def __init__(self, chatbot_id: str):
        self.chatbot_id = chatbot_id
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.log_dir = os.path.join(BASE_LOG_DIR, chatbot_id)
        self.file_path = os.path.join(self.log_dir, f"{self.today}.log")

        try:
            create_chatbot_log_dir(chatbot_id)
            self.logger = self._get_chatbot_logger()
        except Exception as e:
            err_msg = f"Error while creating chatbot log file for {chatbot_id}"
            logger.error(err_msg)
            raise chatBotFileNotFoundError(err_msg, chatbot_id)

    def _get_chatbot_logger(self) -> logging.Logger:
        logger_name = f"chatbot_{self.chatbot_id}"
        log = logging.getLogger(logger_name)
        log.setLevel(logging.INFO)
        log.propagate = False

        if not any(isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(self.file_path) for h in log.handlers):
            file_handler = logging.FileHandler(self.file_path, encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
            file_handler.setFormatter(formatter)
            log.addHandler(file_handler)

        return log

    def get_logger(self) -> logging.Logger:
        return self.logger

def getlogger(chatbot_id: str) -> logging.Logger:
    return ChatBotLogger(chatbot_id).get_logger()
