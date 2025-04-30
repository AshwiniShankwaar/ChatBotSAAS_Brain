import datetime
from pinecone import (
    Pinecone,
    ServerlessSpec,
    CloudProvider,
    AwsRegion,
    VectorType,
    DeletionProtection
)
from langchain_core.documents import Document
from Brain.vector_storage.pinecone_store import pinecone_db
from Brain.Logger.logger import logger


class vector_store_dense(pinecone_db):

    def __init__(
            self,
            pc: Pinecone,
            index_name: str,
            chunk_text: list[Document],
            embedded: list[list[float]],
            namespace: str
    ):
        self._pc = pc
        self._index_name = f"{index_name}-dense"
        self._chunk_text = chunk_text
        self._embedded = embedded
        self._namespace = namespace
        logger.info(f"Initialized vector_store_dense with index: {self._index_name}, namespace: {self._namespace}")

    def create_index(self):
        if not self._pc.has_index(self._index_name):
            logger.info(f"Index '{self._index_name}' not found. Creating new index...")
            self._pc.create_index(
                name=self._index_name,
                dimension=len(self._embedded[0]),
                metric="cosine",
                spec=ServerlessSpec(
                    cloud=CloudProvider.AWS,
                    region=AwsRegion.US_EAST_1
                ),
                deletion_protection=DeletionProtection.DISABLED,
                vector_type=VectorType.DENSE
            )
            logger.info(f"Index '{self._index_name}' created successfully.")
        else:
            logger.info(f"Index '{self._index_name}' already exists.")

        self._index = self._pc.Index(name=self._index_name)
        logger.info(f"Connected to index '{self._index_name}'.")

    def save(self):
        if not hasattr(self, "_index"):
            logger.info("Index not initialized. Creating index...")
            self.create_index()

        logger.info(f"Preparing to upsert {len(self._chunk_text)} vectors into index '{self._index_name}'...")
        vectors = []
        for i, (doc, embedding) in enumerate(zip(self._chunk_text, self._embedded)):
            vector_id = f"{self._namespace}-{i}"
            metadata = {"text": doc.page_content}
            vectors.append((vector_id, embedding, metadata))

        self._index.upsert(vectors=vectors, namespace=self._namespace)
        logger.info(
            f"{len(vectors)} vectors upserted to index '{self._index_name}' under namespace '{self._namespace}'.")
