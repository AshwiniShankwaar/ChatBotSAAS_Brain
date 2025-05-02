
import os
from dotenv import load_dotenv
from Brain import (
     DocumentLoader,
     WebLoader,
     char_text_splitter,
     json_text_splitter,
     perform_embedding_doc,
     vector_store_dense,
     vector_store_sparse,
     retrival_doc,
     get_answer
)
from pinecone import Pinecone
from Logger.logger import get_logger

import json
load_dotenv()
pine_api_key = os.getenv("PINECONE_API_KEY")
pc = Pinecone(
        api_key=pine_api_key
    )
logger = get_logger()
index_name = "rag-application-kb"
namespace = "concepts"
exclude = ['include', 'Lib', 'Scripts', 'share','.git','.idea']
depth =1
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
    chunks = splitter.processDocumnet()[0:200]
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

def print_tree(path, prefix='', current_depth=0):

    if current_depth > depth:
        return
    try:
        entries = sorted(os.scandir(path), key=lambda e: (not e.is_dir(), e.name.lower()))
        for entry in entries:
            if current_depth == 0 and entry.name in exclude:
                continue
            print(f"{prefix}├── {entry.name}")
            if entry.is_dir():
                print_tree(entry.path, prefix + "│   ", current_depth + 1)
    except PermissionError:
        print(f"{prefix}├── [Permission Denied]")

if __name__ == '__main__':
    doc = load_doc()
    chunks = preprocess_doc(doc)
    embedded = perform_embedding(chunks)
    store_data(chunks,embedded)
    print("Ask your question")
    query = input()
    r_doc = retriver(query)
    ans = answer(query,r_doc)
    print(ans)

    # cwd_path = os.getcwd()
    # print_tree(path=cwd_path)

    # cwd_path = os.getcwd()
    # temp_path = f"{cwd_path}\\files"
    # entries = sorted(os.scandir(temp_path),
    #                  key = lambda e: (e.name.lower()))
    # for entry in entries:
    #     if not os.path.basename(entry.path) == "anscombe.json":
    #         print(entry.path)
    #     else:
    #         with open(entry.path, "r", encoding="utf-8") as file:
    #             data = json.load(file)  # This will be a list of dictionaries
    #             for item in data:
    #                 # Now `item` is each dictionary like {'link': ..., 'follow': ..., 'depth': ...}
    #                 # link = item.get("link")
    #                 # follow = item.get("follow", False)
    #                 # depth = item.get("depth", 1)
    #                 Series = item.get("Series")
    #                 print(Series)
    pass

