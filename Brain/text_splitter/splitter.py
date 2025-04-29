from abc import ABC,abstractmethod
from langchain_core.documents import Document
class splitter(ABC):
    @abstractmethod
    def processDocumnet(self)->list[Document]:
        pass

