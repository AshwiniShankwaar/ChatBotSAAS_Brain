# app/Main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import chatbot, query
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title=os.getenv("APP_NAME"), version=os.getenv("APP_VERSION"))

app.include_router(chatbot.router, prefix="/chatbot")
app.include_router(query.router, prefix="/query")

@app.get("/health")
def health():
    return {"status": "ok"}
