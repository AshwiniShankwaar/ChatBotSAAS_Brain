import json
import os
import re
from rank_bm25 import BM25Okapi
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from pinecone import Pinecone
from Logger.logger import get_logger
from dotenv import load_dotenv
load_dotenv()

logger = get_logger()
project_root = os.path.dirname(os.path.abspath(__file__))  # current file's dir
root_dir = os.path.abspath(os.path.join(project_root, "../../"))
bash_dir = os.path.join(root_dir,"bm25model")
# Load saved BM25 model (tokenized corpus)
def load_bm25_model(namespace: str) -> BM25Okapi:
    with open(f"{bash_dir}/{namespace}.json", "r", encoding="utf-8") as f:
        tokenized_corpus = json.load(f)
    logger.info(f"bm25 model is loaded for chatbot: {namespace}")
    return BM25Okapi(tokenized_corpus)

def simple_tokenize(text: str) -> list[str]:
    # Lowercase, remove punctuation, and split on word boundaries
    return re.findall(r"\b\w+\b", text.lower())
# Generate sparse vector using loaded BM25
def generate_sparse_vector(text: str, bm25_model: BM25Okapi):
    tokenized_query = simple_tokenize(text)
    scores = bm25_model.get_scores(tokenized_query)
    # logger.info(f"score is {scores}")
    scores = [float(s) for s in scores]

    sparse = {
        "indices": [],
        "values": []
    }
    for idx, score in enumerate(scores):
        if score > 0:
            sparse["indices"].append(int(idx))
            sparse["values"].append(score)
            # logger.info(f"{idx} score: {score}")

    return sparse

# Hybrid Retrieval Function
def retrival_doc(
        embedded_model:HuggingFaceEmbeddings,
        index:str,
        pc: Pinecone,
        query: str,
        top_k: int = 5,
        namespace: str = os.getenv("RETRIVAL_NAMESPACE_DEFAULT")
):
    index_d = pc.Index(name=f"{index}-dense")
    # logger.info(f"{index}-dense is present" )
    index_s = pc.Index(name=f"{index}-sparse")
    # logger.info(f"{index}-sparse is present")
    # Load dense embedding model

    query_embedded = embedded_model.embed_documents([query])[0]
    logger.info(f"query embedded is generated len: {len(query_embedded)}")
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
