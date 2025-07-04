import logging
import os

from app.schemas.query import QueryRequest
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from Brain.Retrival import retrival_doc
from logging import Logger
from dotenv import load_dotenv
from pinecone import Pinecone
from Brain.llm_struture.answer_generator import get_answer
load_dotenv()
def process_query(payload:QueryRequest,
                  botlogger:logging.Logger,
                  model:HuggingFaceEmbeddings,
                  pc:Pinecone):
    #pipline for processing the query
    #phase: retriving the document based on query
    botlogger.info(f"retriving docs based on query {payload.query}")
    namespace = f"{payload.client_id}_{payload.chatbot_id}"
    retrieved_docs = retrival_doc(
        embedded_model=model,
        index = os.getenv("INDEX_NAME"),
        pc = pc,
        query = payload.query,
        top_k = 5,
        namespace=namespace
    )
    # botlogger.info(f"{retrived_doc}")
    botlogger.info("document retrived now passing to the llm for generating output..")
    if not retrieved_docs:
        fallback_context = "No relevant information was found for this query."
    else:
        fallback_context = retrieved_docs
    # botlogger.info(fallback_context)
    answer,usages_data = get_answer(payload.query,fallback_context,payload.agent_role,payload.past_msg)
    botlogger.info("answer recived from llm...")
    return answer,usages_data
