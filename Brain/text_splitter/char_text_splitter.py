import os

from langchain_core.documents import Document
from Brain.text_splitter.splitter import splitter
from Logger.logger import get_logger
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
load_dotenv()
logger = get_logger()
class char_text_splitter(splitter):
    def __init__(self,document:list[Document],
                        chunk_size:int = int(os.getenv("CHUNK_SIZE")),
                        chunk_overlap:int = int(os.getenv("CHUNK_OVERLAPING")),
                        separator:list[str]=["\n\n", "\n", " ", ""]):
        self._doc = document
        self._chunk_size = chunk_size
        self._chunk_overlap = chunk_overlap
        self._sep = separator

    def processDocumnet(self)->list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            separators=self._sep,
            strip_whitespace=True
        )
        chunks = text_splitter.split_documents(self._doc)
        logger.info(f"Successfully preprocessed documents into {len(chunks)} chunks.")
        return chunks
