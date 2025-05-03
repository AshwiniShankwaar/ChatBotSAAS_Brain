import os

from fastapi import FastAPI
from app.api import chatbot,query
from embeddedModel.huggingfaceModel import embedding_model
from Logger import get_logger
from pinecone import Pinecone
from dotenv import load_dotenv
model = None  # Global placeholder
logger = get_logger()
load_dotenv()
pine_api_key = os.getenv("PINECONE_API_KEY")
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    global pc
    logger.info("Loading embedding model...")
    model = embedding_model
    logger.info("Model loaded.")
    logger.info("creating pinecone instance..")
    pc = Pinecone(
        api_key=pine_api_key
    )
    logger.info("pinecone available for use in gloable pc")
    yield


app = FastAPI(
    title=os.getenv("APP_NAME"),
    version=os.getenv("APP_VERSION"),
)

app.include_router(chatbot.router,prefix="/chatbot")
app.include_router(query.router,prefix="/query")

@app.get("/health")
def health():
    return {"status": "ok"}
