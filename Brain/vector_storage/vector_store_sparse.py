from pinecone import (
    Pinecone,
    ServerlessSpec,
    CloudProvider,
    AwsRegion,
    VectorType,
    DeletionProtection
)
from langchain_core.documents import Document
from dotenv import load_dotenv
from Brain.vector_storage.pinecone_store import pinecone_db
from rank_bm25 import BM25Okapi
from Brain.Logger.logger import logger

class vector_store_sparse(pinecone_db):
    def __init__(
            self,
            pc: Pinecone,
            index_name: str,
            chunks: list[Document],
            namespace: str = "default"
    ):
        self.pc = pc
        self.index_name = f"{index_name}-sparse"
        self.chunks = chunks
        self.namespace = namespace
        self.tokenized_corpus = [doc.page_content.split(" ") for doc in chunks]
        self.bm25 = BM25Okapi(self.tokenized_corpus)
        self.index = self.create_index()

    def create_index(self):
        if not self.pc.has_index(self.index_name):
            logger.info(f"{self.index_name} index not present ")
            self.pc.create_index(
                name=self.index_name,
                metric="dotproduct",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                vector_type=VectorType.SPARSE,
                deletion_protection=DeletionProtection.DISABLED
            )
        logger.info(f"{self.index_name} index is created ")
        return self.pc.Index(name=self.index_name)

    def generate_sparse_vector(self, text: str):
        tokenized_query = text.split(" ")
        scores = self.bm25.get_scores(tokenized_query)
        sparse = {
            "indices": [],
            "values": []
        }
        for idx, score in enumerate(scores):
            if score > 0:
                sparse["indices"].append(int(idx))
                sparse["values"].append(float(score))

        return sparse

    def save(self):
        vectors = []
        for i, doc in enumerate(self.chunks):
            sparse_vector = self.generate_sparse_vector(doc.page_content)
            vectors.append({
                "id": f"doc-{i}",
                "sparse_values": sparse_vector,
                "metadata": {
                    "text": doc.page_content,
                    "source": doc.metadata.get("source", "unknown")
                }
            })
        self.index.upsert(vectors=vectors, namespace=self.namespace)
        logger.info(f"vector saved in index {self.index_name}")
