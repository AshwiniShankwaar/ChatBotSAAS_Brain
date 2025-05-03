import json
import os

from rank_bm25 import BM25Okapi
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
from Logger.logger import get_logger
from dotenv import load_dotenv
load_dotenv()

logger = get_logger()
# Load saved BM25 model (tokenized corpus)
def load_bm25_model(namespace: str) -> BM25Okapi:
    with open(f"bm25model/{namespace}.json", "r", encoding="utf-8") as f:
        tokenized_corpus = json.load(f)
    logger.info(f"bm25 model is loaded for chatbot: {namespace}")
    return BM25Okapi(tokenized_corpus)

# Generate sparse vector using loaded BM25
def generate_sparse_vector(text: str, bm25_model: BM25Okapi):
    tokenized_query = text.split(" ")
    scores = bm25_model.get_scores(tokenized_query)
    scores = [float(s) for s in scores]

    sparse = {
        "indices": [],
        "values": []
    }
    for idx, score in enumerate(scores):
        if score > 0:
            sparse["indices"].append(int(idx))
            sparse["values"].append(score)
    return sparse

# Hybrid Retrieval Function
def retrival_doc(
        embedded_model:HuggingFaceEmbeddings,
        index:str,
        pc: Pinecone,
        query: str,
        top_k: int = int(os.getenv("RETRIVAL_TOP_K")),
        namespace: str = os.getenv("RETRIVAL_NAMESPACE_DEFAULT")
):
    index_d = pc.Index(name=f"{index}-dense")
    index_s = pc.Index(name=f"{index}-sparse")
    # Load dense embedding model

    query_embedded = embedded_model.embed_documents([query])[0]
    logger.info("query embedded is generated")
    # Load saved BM25 model
    bm25 = load_bm25_model(namespace)
    sparse_vector = generate_sparse_vector(query, bm25)
    logger.info("query sparse embedded is also generated")
    # Hybrid search
    results_s = index_s.query(
        namespace=namespace,
        top_k=top_k,
        sparse_vector=sparse_vector,
        include_metadata=True
    )
    logger.info(f"sparse search result fetched for query {query}")
    results_d = index_d.query(
        vector=query_embedded,
        top_k=top_k,
        include_metadata=True,
        namespace=namespace
    )
    logger.info(f"dense search result is fetched for query {query}")
    return merge_results(results_d, results_s)

# Merge sparse + dense results
def merge_results(dense_results, sparse_results):
    all_hits = dense_results['matches'] + sparse_results['matches']
    deduped = {}
    for hit in all_hits:
        if hit['id'] not in deduped or hit['score'] > deduped[hit['id']]['score']:
            deduped[hit['id']] = hit
    s = sorted(deduped.values(), key=lambda x: x['score'], reverse=True)
    logger.info(f"Dense and sparse, both retrival result is merged")
    return s
