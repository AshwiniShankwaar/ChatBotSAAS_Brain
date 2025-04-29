from langchain_core.documents import Document
from Brain.text_splitter.splitter import splitter
from Brain.Logger.logger import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter
class char_text_splitter(splitter):
    def __init__(self,document:list[Document],
                        chunk_size:int=500,
                        chunk_overlap:int=50,
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
