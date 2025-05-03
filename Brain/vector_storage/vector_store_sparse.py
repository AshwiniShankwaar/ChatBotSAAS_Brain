from pinecone import (
    Pinecone,
    ServerlessSpec,
    VectorType,
    DeletionProtection
)
from langchain_core.documents import Document
from Brain.vector_storage.pinecone_store import pinecone_db
from rank_bm25 import BM25Okapi
from Logger.logger import get_logger

import json
import os

logger = get_logger()

class vector_store_sparse(pinecone_db):
    def __init__(
            self,
            pc: Pinecone,
            index_name: str,
            chunks: list[Document],
            namespace: str = os.getenv("RETRIVAL_NAMESPACE_DEFAULT")
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
        self.save_bm25_model()
        logger.info(f"vector saved in index {self.index_name}")

    def save_bm25_model(self):
        """Save tokenized corpus as JSON inside the project root under /bm25model/{namespace}.json"""
        # Get the root project directory (assumes this script runs from anywhere inside the project)
        project_root = os.path.dirname(os.path.abspath(__file__))  # current file's dir
        root_dir = os.path.abspath(os.path.join(project_root, "../../"))  # adjust as needed

        bm25_dir = os.path.join(root_dir, "bm25model")
        os.makedirs(bm25_dir, exist_ok=True)
        logger.info(f"bm25model directory ensured at {bm25_dir}")

        path = os.path.join(bm25_dir, f"{self.namespace}.json")

        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.tokenized_corpus, f)
            logger.info(f"BM25 model saved for namespace {self.namespace} at {path}")
        except Exception as e:
            logger.error(f"Error saving BM25 model: {e}")
