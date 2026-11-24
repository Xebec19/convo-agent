import os

from fastembed import TextEmbedding
from qdrant_client import QdrantClient

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = os.getenv("QDRANT_PORT", "6333")
qdrant_client = QdrantClient(url=f"http://{QDRANT_HOST}:{QDRANT_PORT}")

COLLECTION_NAME = "documents"

embeddings = TextEmbedding()
