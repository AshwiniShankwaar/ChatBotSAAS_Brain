from app.schemas import ChatbotCreateRequest
from fastapi import UploadFile
from io import BytesIO
import os
from app.api.chatbot import create_chatbot
import asyncio
payload = {
        "client_id": "test_client",
        "chatbot_id": "test_bot",
        "chatbot_name": "TestBot",
        "chatbot_description": "Test chatbot",
        "agent_role": "helper",
        "temprature": 0.5,
        "weblinks":[
            {"link": "https://python.langchain.com/docs/introduction/", "follow": True, "depth": 2},
            {"link": "https://langchain-ai.github.io/langgraph/tutorials/introduction/", "follow": True, "depth": 1}
        ]
    }
def create_fake_upload_file_from_path(file_path: str) -> UploadFile:
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        content = f.read()
    return UploadFile(filename=filename, file=BytesIO(content))

files = [
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Downloads\\concepts.pdf"),
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Downloads\\developers-guide.pdf"),
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Downloads\\plsqlLearning.txt"),
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Downloads\\json_schema.json"),
        create_fake_upload_file_from_path("C:\\Users\\ashwi\\Desktop\\projects\\angleApiTrading\\data\\bse_20241201TO20241224.csv")
    ]

data = ChatbotCreateRequest(
    client_id = payload['client_id'],
    chatbot_id = payload['chatbot_id'],
    chatbot_name = payload['chatbot_name'],
    chatbot_description= payload['chatbot_description'],
    agent_role = payload['agent_role'],
    temprature = payload['temprature']
)
weblinks = payload['weblinks']


def test_create_chatbot():
    res = asyncio.run(create_chatbot(data, files, weblinks))
    print(res['namespace'])