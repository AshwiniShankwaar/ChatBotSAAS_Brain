from typing import Optional
class chatBotFileNotFoundError(Exception):
    def __init__(self,message:str,chatbot_id:str):
        super().__init__(message)
        self.chatbot_id = chatbot_id
    def __str__(self):
        if self.chatbot_id:
            return f"Error creating file for {self.chatbot_id}:{super().__str__()}"
        return super().__str__()
