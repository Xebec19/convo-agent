from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient

qdrant_client = QdrantClient(url="http://localhost:6333")

COLLECTION_NAME = "documents"

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
