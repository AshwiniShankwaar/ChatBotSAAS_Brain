from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document
from Brain.Logger.logger import logger
load_dotenv()
huggingface_model_name = "sentence-transformers/all-mpnet-base-v2"
embedding_model = HuggingFaceEmbeddings(
    model_name=huggingface_model_name
)

def perform_embedding_doc(chunks:list[Document])->list[list[float]]:
    chunk_texts = [chunk.page_content for chunk in chunks]
    embedded = embedding_model.embed_documents(chunk_texts)
    logger.info(f"document embedded: {len(embedded)} of dim: {len(embedded[0])}")
    return embedded

def perform_embedding_query(text:str)->list[list[float]]:
    embedded = embedding_model.embed_query(text)
    logger.info(f"query embedded: {len(embedded)} of dim: {len(embedded[0])}")
    return embedded
