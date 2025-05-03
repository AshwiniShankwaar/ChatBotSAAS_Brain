import os

from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
load_dotenv()
huggingface_model_name = os.getenv("EMBEDDED_MODEL")
embedding_model = HuggingFaceEmbeddings(
    model_name=huggingface_model_name
)