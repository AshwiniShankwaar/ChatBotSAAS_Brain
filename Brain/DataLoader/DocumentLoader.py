import os
import logging
from Brain.DataLoader.Loader import Loader
from Brain.Exceptions.lodderError import lodderError
from Brain.Logger.logger import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader,JSONLoader,CSVLoader
class DocumentLoader(Loader):
    """
    Loads data from a local document file.
    Supports text files. Can be extended to support other file types.
    """
    def __init__(self, file_path: str):
        """
        Initialize the DocumentLoader.

        Args:
            file_path (str): The path to the document file.
        """
        if not isinstance(file_path, str):
            raise TypeError(f"filename must be a string, got {type(file_path)}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"filename {file_path} does not exist")
        if not (file_path.endswith(".txt") or
                file_path.endswith("pdf") or
                file_path.endswith(".json") or
                file_path.endswith(".csv")
        ):
            raise ValueError(f"filename must end with .txt or .pdf, got {file_path}")
        self._file_path = file_path
        self.filename = os.path.basename(file_path)

    def load(self) -> list[Document]:
        """
        Load data from the document file.

        Returns:
            str: The content of the document as a string.

        Raises:
            loaderError: If there is an error reading the file.
        """
        try:
            if self._file_path.endswith(".pdf"):
                loader = PyPDFLoader(self._file_path)
                doc = loader.load()
                logger.info(f"pdf file loaded successfully from: {self.filename}")
            elif self._file_path.endswith(".txt"):
                loader = TextLoader(self._file_path)
                doc = loader.load()
                logger.info(f"txt file loaded successfully from: {self.filename}")
            elif self._file_path.endswith(".json"):
                loader = JSONLoader(self._file_path,jq_schema=".[]", text_content=False)
                doc = loader.load()
                logger.info(f"json file loaded successfully from: {self.filename}")
            elif self._file_path.endswith(".csv"):
                loader = CSVLoader(self._file_path)
                doc = loader.load()
                logger.info(f"json file loaded successfully from: {self.filename}")
            else:
                raise ValueError(f"file need to be pdf, txt, csv or json but provided is {self.filename}")
            return doc
        except (IOError, OSError) as e:
            error_msg = f"Error reading file: {e}"
            logger.error(error_msg)
            raise loaderError(error_msg, source=self._file_path)

    @property
    def source(self) -> str:
        """
        Returns the source of the data being loaded.

        Returns:
            str: The file path of the document.
        """
        return self._file_path
