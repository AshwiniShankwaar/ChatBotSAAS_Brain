from Logger import get_logger
from app.utils_file import load_from_file
import multiprocessing
import logging
from Brain.text_splitter import char_text_splitter
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_core.documents import Document
logger = get_logger()
def get_cpu_cores():
    return multiprocessing.cpu_count()

def loading_doc(temp_dir,botlogger):
    botlogger.info("loading the document...")
    entries = sorted([entry for entry in os.scandir(temp_dir) if entry.is_file()],
                     key=lambda e: e.name.lower())
    doc_list = []
    num_workers = min(8, get_cpu_cores())  # You can adjust the max
    botlogger.info(f"Using {num_workers} threads for loading documents")

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(load_from_file, entry, botlogger) for entry in entries]
        for future in as_completed(futures):
            docs = future.result()
            if docs:
                doc_list.extend(docs)

    botlogger.info(f"Total documents loaded: {len(doc_list)}")
    return doc_list
    # first load the docs
    # for entry in entries:
    #     if os.path.basename(entry.path) == "weblinks.json":
    #         loader = DocumentLoader(entry.path)
    #         doc = loader.load()
    #         doc_list.append(doc)
    #     else:
    #         #first load the json file then extract the links
    #         with open(entry.path, "r", encoding="utf-8") as file:
    #             data = json.load(file)  # This will be a list of dictionaries
    #             for item in data:
    #                 # Now `item` is each dictionary like {'link': ..., 'follow': ..., 'depth': ...}
    #                 link = item.get("link")
    #                 follow = item.get("follow", False)
    #                 depth = item.get("depth", 1)
    #                 #then pass the data in the webloader then add the document list into the doc_list folder
    #                 loader = WebLoader(entry.path,follow,depth)
    #                 doc = loader.load()
    #                 doc_list.append(doc)

def preform_preprocessing(doc_list,botlogger)->list[Document]:
    botlogger.info(f"pre-processing phase begin... no of documents: {len(doc_list)}")
    # chunks_list=[]
    # nbr_wrks = min(4,get_cpu_cores())
    # botlogger.info(f"Using {num_workers} threads for loading documents")
    splitter = char_text_splitter(doc_list,2000,200)
    chunks = splitter.processDocumnet()
    return chunks

    pass
def create_chatbot_pipeline(payload,temp_dir,botlogger:logging.Logger):
    #phase file loading
    botlogger.info(f"loading all the documents from {temp_dir}")
    start_load = time.time()
    doc_list = loading_doc(temp_dir=temp_dir,botlogger=botlogger)
    end_load = time.time()
    botlogger.info(f"documents {len(doc_list)} are loadded now moving to pre-processing phase..."
                   f"time taken:{end_load-start_load}")

    #phase: pre-processing
    start_preprocess=time.time()
    chunks = preform_preprocessing(doc_list=doc_list,botlogger=botlogger)
    end_preprocessing=time.time()
    botlogger.info(f"chunks created, chunks size: {len(chunks)},"
                   f"time taken: {end_preprocessing-start_preprocess}")

    #phase: embedding
    start_embedded = time.time()
    botlogger.info(f"embedding start at{start_embedded}")

    end_embedded = time.time()
    botlogger.info(f"embedding end at: {end_embedded-start_embedded} ")
    return "deafult"



