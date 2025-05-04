from Logger import get_logger
from app.utils_file import load_from_file
from Brain.text_splitter import char_text_splitter
from Brain import perform_embedding_doc,vector_store_dense,vector_store_sparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_core.documents import Document
from dotenv import load_dotenv
import os
import time
import multiprocessing
import logging

load_dotenv()
index_name = os.getenv("INDEX_NAME")
chunk_size = int(os.getenv("CHUNK_SIZE"))
chunk_overlap = int(os.getenv("CHUNK_OVERLAPING"))
logger = get_logger()
worker = int(os.getenv("MAX_WORKERS"))

from pinecone import Pinecone
pine_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(api_key=pine_api_key)

def get_cpu_cores():
    return multiprocessing.cpu_count()

def loading_doc(temp_dir,botlogger):
    botlogger.info("loading the document...")
    entries = sorted([entry for entry in os.scandir(temp_dir) if entry.is_file()],
                     key=lambda e: e.name.lower())
    doc_list = []
    num_workers = min(worker, get_cpu_cores())  # You can adjust the max
    botlogger.info(f"Using {num_workers} threads for loading documents")

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(load_from_file, entry, botlogger) for entry in entries]
        for future in as_completed(futures):
            docs = future.result()
            if docs:
                doc_list.extend(docs)

    botlogger.info(f"Total documents loaded: {len(doc_list)}")
    return doc_list

def preform_preprocessing(doc_list,botlogger)->list[Document]:
    botlogger.info(f"pre-processing phase begin... no of documents: {len(doc_list)}")
    splitter = char_text_splitter(doc_list,chunk_size=chunk_size,chunk_overlap=chunk_overlap)
    chunks = splitter.processDocumnet()
    return chunks
    pass



def create_chatbot_task(payload, temp_dir,botlogger:logging.Logger,embedded_model):  # Define a Celery task, add self
    botlogger.info(f"Celery task started for chatbot: {payload.chatbot_name}, id: {payload.chatbot_id}")
    try:
        # phase file loading
        botlogger.info(f"loading all the documents from {temp_dir}")
        start_load = time.time()
        doc_list = loading_doc(temp_dir=temp_dir, botlogger=botlogger)
        end_load = time.time()
        botlogger.info(
            f"documents are loaded, now moving to pre-processing phase... time taken:{end_load - start_load}"
        )

        # phase: pre-processing
        start_preprocess = time.time()
        chunks = preform_preprocessing(doc_list=doc_list, botlogger=botlogger)
        end_preprocessing = time.time()
        botlogger.info(
            f"chunks created, chunks size: {len(chunks)}, time taken: {end_preprocessing - start_preprocess}"
        )

        # phase: embedding
        start_embedded = time.time()
        botlogger.info(f"embedding start at {start_embedded}")
        embeddings = perform_embedding_doc(chunks,embedded_model)  # Call your synchronous embedding function
        end_embedded = time.time()
        botlogger.info(f"embedding end at: {end_embedded} ")

        # phase: store in pinecone
        #  Add your Pinecone storage logic here, using payload.chatbot_id to create a unique namespace
        namespace = f"{payload.client_id}_{payload.chatbot_id}"  # Or generate a namespace as needed.
        botlogger.info(f"embedded len: {len(embeddings)} dimentions: {len(embeddings[0])}")
        dense_store = vector_store_dense(
            pc=pc,
            index_name=index_name,
            chunk_text=chunks,
            embedded=embeddings,
            namespace=namespace
        )
        dense_store.save()
        botlogger.info(f"dense vector data is stored in {index_name} index with namespace {namespace}")
        sparse_store = vector_store_sparse(
            pc=pc,
            index_name=index_name,
            chunks=chunks,
            namespace=namespace
        )
        sparse_store.save()
        botlogger.info(f"sparse vector data is stored in {index_name} index with namespace {namespace}")
        botlogger.info(
            f"Chatbot {payload.chatbot_name} (ID: {payload.chatbot_id}) processing complete.  Namespace: {namespace}"
        )
        return namespace  # Return the namespace or any relevant result
    except Exception as e:
        logger.error(f"Error in Celery task: {e}", exc_info=True)
        raise  # Re-raise the exception to be handled by Celery's error handling




