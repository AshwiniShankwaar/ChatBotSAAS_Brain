import logging

from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document
from Logger.logger import get_logger
from concurrent.futures import ThreadPoolExecutor, as_completed
logger = get_logger()
load_dotenv()

def batch_task(chunks:list[Document],
        embedding_model:HuggingFaceEmbeddings):
    chunk_texts = [chunk.page_content for chunk in chunks]
    embedded = embedding_model.embed_documents(chunk_texts)
    return embedded
def perform_embedding_doc(
        chunks:list[Document],
        embedding_model:HuggingFaceEmbeddings,
        batch_size:int = 64,
        max_worker:int=4
)->list[list[float]]:
    try:
        batchs = [chunks[i:i+batch_size] for i in range(0,len(chunks),batch_size)]
        logger.info(f"batch created of len: {len(batchs)}")
        embeddings = []
        with ThreadPoolExecutor(max_workers=max_worker) as executor:
            futures = {executor.submit(batch_task,batch,embedding_model):batch for batch in batchs}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    embeddings.extend(result)
                except Exception as e:
                    logger.error(f"Error embedding batch: {e}")

        logger.info(f"document embedded: {len(embeddings)} of dim: {len(embeddings[0])}")
        return embeddings
    except Exception as e:
        logger.error(f"error in embedding doc {e}")

def perform_embedding_query(text:str)->list[list[float]]:
    try:
        embedded = embedding_model.embed_query(text)
        logger.info(f"query embedded: {len(embedded)} of dim: {len(embedded[0])}")
        return embedded
    except Exception as e:
        logger.error(f"error in embedding query {e}")
