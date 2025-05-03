import os
from app.services.chatbot_create import create_chatbot_task
from app.schemas.chatbot import ChatbotCreateRequest
import threading
temp_dir = "C:\\Users\\ashwi\\Desktop\\projects\\chatBotBrain\\files\\test_client_test_bot"

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


def thread_test(thread_id):
    data = ChatbotCreateRequest(
        client_id=f"{payload['client_id']}{thread_id}",
        chatbot_id=f"{payload['chatbot_id']}{thread_id}",
        chatbot_name=payload['chatbot_name'],
        chatbot_description=payload['chatbot_description'],
        agent_role=payload['agent_role'],
        temprature=payload['temprature']
    )
    res = create_chatbot_task(payload=data, temp_dir=temp_dir)
    assert res == f"{payload['client_id']}_{payload['chatbot_id']}"
def test_create_chatbot_task():
    threads = []
    for i in range(4):
        thread = threading.Thread(target=thread_test,args=(i,))
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join()

    print("test finised")
