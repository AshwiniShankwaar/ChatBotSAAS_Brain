"""
This is a interface that will be inherit by other loaders like document loader, webpage loader,..
"""
from abc import ABC, abstractmethod
from typing import List, Union
from langchain_core.documents import Document
class Loader(ABC):
    """
    Abstract base class for all loaders.  Defines the common interface.
    All loaders should inherit from this class and implement the load() method.
    """
    @abstractmethod
    def load(self) -> list[Document]:
        """
        Load data from the specified source.

        Returns:
            Union[str, List[str]]: The loaded data, either as a single string or a list of strings.
                The type of data returned depends on the specific loader implementation.
                String(s) will be passed for pre-processing.

        Raises:
            LoaderError: If there is an error during the loading process.  This allows
                for more specific error handling, such as retrying or notifying the user.
        """
        pass

    @property
    @abstractmethod
    def source(self) -> str:
        """
        Returns the source of the data being loaded.

        This is a read-only property.  It should not have a setter.

        Returns:
            str: The source of the data (e.g., filename, URL).
        """
        pass