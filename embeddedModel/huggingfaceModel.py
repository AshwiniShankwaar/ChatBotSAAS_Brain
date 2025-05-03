from langchain_huggingface.embeddings import HuggingFaceEmbeddings
huggingface_model_name = "sentence-transformers/all-mpnet-base-v2"
embedding_model = HuggingFaceEmbeddings(
    model_name=huggingface_model_name
)