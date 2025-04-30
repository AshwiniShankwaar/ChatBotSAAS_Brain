from Brain.DataLoader.DocumentLoader import DocumentLoader # Import the class
from Brain.DataLoader.WebLoader import WebLoader # Import the class
import os
from dotenv import load_dotenv
from Brain.text_splitter.json_text_splitter import json_text_splitter
from Brain.text_splitter.char_text_splitter import char_text_splitter
from Brain.embedding.haggingFaceEmbedding import perform_embedding_doc,perform_embedding_query
from Brain.vector_storage import vector_store_dense,vector_store_sparse
from pinecone import Pinecone
from Brain.Logger.logger import logger
from Brain.Retrival import retrival_doc
from Brain.llm_struture import get_answer
load_dotenv()
pine_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(
        api_key=pine_api_key
    )

index_name = "rag-application-kb"
namespace = "concepts"
def load_doc():
    # load document
    # test for pdf loader
    loader = DocumentLoader("./files/concepts.pdf")
    # loader = WebLoader("https://python.langchain.com/docs",True,2)
    doc = loader.load()
    # print(len(doc))
    logger.info("doc loaded")
    return doc

def preprocess_doc(doc):
    # perform text_split
    # splitter = json_text_splitter(doc)
    splitter = char_text_splitter(doc)
    chunks = splitter.processDocumnet()[0:100]
    # print(len(chunks))
    logger.info("chunks created")
    return chunks

def perform_embedding(chunks):
    embedded_doc = perform_embedding_doc(chunks)
    print(f"embedded performed {len(embedded_doc)}, dimentions {len(embedded_doc[0])}")
    return embedded_doc

def store_data(chunks,embedded_doc):
    # Dense Vector Store
    dense_store = vector_store_dense(
        pc=pc,
        index_name=index_name,
        chunk_text=chunks,
        embedded=embedded_doc,
        namespace=namespace
    )
    dense_store.save()
    logger.info("dense data stored")
    # Sparse Vector Store
    sparse_store = vector_store_sparse(
        pc=pc,
        index_name=index_name,
        chunks=chunks,
        namespace=namespace
    )
    sparse_store.save()
    logger.info("sparse data stored")

def retriver(query:str):
    res = retrival_doc(index_name, pc, query, 5, namespace)
    return res

def answer(query:str,res)->str:
    answer = get_answer(query,res)
    return answer

if __name__ == '__main__':
    # doc = load_doc()
    # chunks = preprocess_doc(doc)
    # embedded = perform_embedding(chunks)
    # store_data(chunks,embedded)
    print("Ask your question")
    query = input()
    r_doc = retriver(query)
    ans = answer(query,r_doc)
    print(ans)
    pass

