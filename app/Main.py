from fastapi import FastAPI
from app.api import chatbot,query

app = FastAPI(
    title="ChatBot Brain Api",
    version="1.0.0",
)

app.include_router(chatbot.router,prefix="/chatbot")
app.include_router(query.router,prefix="/query")