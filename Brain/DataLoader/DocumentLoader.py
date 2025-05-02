import os
from Brain.DataLoader.Loader import Loader
from Brain.Exceptions.lodderError import lodderError
from Logger.logger import get_logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, TextLoader, JSONLoader, CSVLoader
logger = get_logger()
class DocumentLoader(Loader):
    """
    Loads data from a local document file.
    Supports text, PDF, JSON, and CSV files.
    """

    def __init__(self, file_path: str):
        """
        Initialize the DocumentLoader.

        Args:
            file_path (str): The path to the document file.
        """
        logger.info(f"Initializing DocumentLoader for file: {file_path}")

        if not isinstance(file_path, str):
            logger.error("File path is not a string.")
            raise TypeError(f"filename must be a string, got {type(file_path)}")

        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            raise FileNotFoundError(f"filename {file_path} does not exist")

        if not (file_path.endswith(".txt") or
                file_path.endswith(".pdf") or
                file_path.endswith(".json") or
                file_path.endswith(".csv")):
            logger.error(f"Unsupported file format for file: {file_path}")
            raise ValueError(f"filename must end with .txt, .pdf, .json, or .csv, got {file_path}")

        self._file_path = file_path
        self.filename = os.path.basename(file_path)
        logger.info(f"DocumentLoader initialized for file: {self.filename}")

    def load(self) -> list[Document]:
        """
        Load data from the document file.

        Returns:
            list[Document]: List of LangChain Document objects.

        Raises:
            loaderError: If there is an error reading the file.
        """
        logger.info(f"Attempting to load document from: {self._file_path}")

        try:
            if self._file_path.endswith(".pdf"):
                loader = PyPDFLoader(self._file_path)
                doc = loader.load()
                logger.info(f"PDF file loaded successfully from: {self.filename}")

            elif self._file_path.endswith(".txt"):
                loader = TextLoader(self._file_path)
                doc = loader.load()
                logger.info(f"Text file loaded successfully from: {self.filename}")

            elif self._file_path.endswith(".json"):
                loader = JSONLoader(self._file_path, jq_schema=".[]", text_content=False)
                doc = loader.load()
                logger.info(f"JSON file loaded successfully from: {self.filename}")

            elif self._file_path.endswith(".csv"):
                loader = CSVLoader(self._file_path)
                doc = loader.load()
                logger.info(f"CSV file loaded successfully from: {self.filename}")

            else:
                logger.error(f"Unsupported file format: {self.filename}")
                raise ValueError(f"file must be .pdf, .txt, .json, or .csv but got {self.filename}")

            logger.info(f"Document loaded. Total segments: {len(doc)}")
            return doc

        except (IOError, OSError) as e:
            error_msg = f"Error reading file: {e}"
            logger.error(error_msg)
            raise lodderError(error_msg, source=self._file_path)

    @property
    def source(self) -> str:
        """
        Returns the source of the data being loaded.

        Returns:
            str: The file path of the document.
        """
        return self._file_path
