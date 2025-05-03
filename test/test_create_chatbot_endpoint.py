import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from typing import List, Optional
from pydantic import BaseModel
from app.Main import app
from unittest.mock import patch, MagicMock

# Define Pydantic models for request body (if you have them)
class ChatbotCreateRequest(BaseModel):
    client_id: str
    chatbot_id: str
    chatbot_name: str
    chatbot_description: str
    agent_role: str
    temprature: float

class WebLink(BaseModel):
    link: str
    follow: bool
    depth: int

# Override Celery task for testing
@pytest.fixture
def mock_celery_task():
    with patch("app.services.chatbot_create.create_chatbot_task") as mock_task:  # Path to your Celery task
        mock_task.return_value = "test_namespace"  # Mock the return value
        yield mock_task

# Create a test client
@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

def test_create_chatbot_endpoint(test_client: TestClient, mock_celery_task: MagicMock):
    """
    Tests the /create_chatbot endpoint with a valid request, mocking the Celery task.
    """
    # Prepare test data
    payload = {
        "client_id": "test_client",
        "chatbot_id": "test_bot",
        "chatbot_name": "TestBot",
        "chatbot_description": "Test chatbot",
        "agent_role": "helper",
        "temprature": 0.5,
    }
    files = [
        ("files", ("test_file1.txt", b"File content 1")),
        ("files", ("test_file2.txt", b"File content 2")),
    ]
    weblinks = [
        {"link": "https://python.langchain.com/docs/introduction/", "follow": True, "depth": 2},
        {"link": "https://langchain-ai.github.io/langgraph/tutorials/introduction/", "follow": True, "depth": 1},
    ]

    # Send the request
    response = test_client.post(
        "/create_chatbot",
        data=payload,
        files=files,
        params={"weblinks": weblinks},  # Send weblinks as query parameters
    )

    # Assert the response
    assert response.status_code == 200
    # assert response.json() == {
    #     "message": "ChatBot TestBot created successfully",
    #     "namespace": "test_namespace",
    # }

    # Assert that the Celery task was called with the correct arguments
    mock_celery_task.assert_called_once()
    args, kwargs = mock_celery_task.call_args
    assert args[0] == payload  # Check the payload
    assert isinstance(args[1], str)  # Check the temp_dir (it's a string)
    # Add more assertions here to check the files_dir if needed.

def test_create_chatbot_endpoint_no_files(test_client: TestClient, mock_celery_task: MagicMock):
    """
    Tests the /create_chatbot endpoint with no files.
    """
    payload = {
        "client_id": "test_client",
        "chatbot_id": "test_bot",
        "chatbot_name": "TestBot",
        "chatbot_description": "Test chatbot",
        "agent_role": "helper",
        "temprature": 0.5,
    }
    weblinks = [
        {"link": "https://python.langchain.com/docs/introduction/", "follow": True, "depth": 2},
        {"link": "https://langchain-ai.github.io/langgraph/tutorials/introduction/", "follow": True, "depth": 1},
    ]
    response = test_client.post(
        "/create_chatbot",
        data=payload,
        params={"weblinks": weblinks},
    )

    assert response.status_code == 200
    assert response.json()["message"].startswith("ChatBot")

def test_create_chatbot_endpoint_error(test_client: TestClient, mock_celery_task: MagicMock):
    """
    Tests the /create_chatbot endpoint when the Celery task raises an exception.
    """
    mock_celery_task.side_effect = Exception("Simulated error")
    payload = {
        "client_id": "test_client",
        "chatbot_id": "test_bot",
        "chatbot_name": "TestBot",
        "chatbot_description": "Test chatbot",
        "agent_role": "helper",
        "temprature": 0.5,
    }
    response = test_client.post(
        "/create_chatbot",
        data=payload,
    )
    assert response.status_code == 500  # Or whatever error code you return
    assert "Failed to create chatbot" in response.json()["detail"]
