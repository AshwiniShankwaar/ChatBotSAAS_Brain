from abc import ABC,abstractmethod

class pinecone_db(ABC):
    @abstractmethod
    def create_index(self):
        pass
    @abstractmethod
    def save(self):
        pass