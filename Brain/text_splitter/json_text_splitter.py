import os

from langchain_core.documents import Document
from Brain.text_splitter.splitter import splitter
from Logger.logger import get_logger
from langchain_text_splitters import RecursiveJsonSplitter
logger = get_logger()
class json_text_splitter(splitter):
    def __init__(self,document:list[Document],
                        chunk_size:int=os.getenv("JUNK_CHUNK_SIZE"),
                        ):
        self._doc = document
        self._chunk_size = chunk_size

    def processDocumnet(self)->list[Document]:
        raw_json_data = [doc.metadata for doc in self._doc]
        json_splitter = RecursiveJsonSplitter(
            max_chunk_size=self._chunk_size
        )
        chunks = json_splitter.create_documents(raw_json_data)
        logger.info(f"Successfully preprocessed documents into {len(chunks)} chunks.")
        return chunks
