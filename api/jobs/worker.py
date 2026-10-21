import logging
import os
import tempfile
import uuid
from pathlib import Path

import boto3
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from qdrant_client.models import Distance, PointStruct, VectorParams
from vectordb.client import COLLECTION_NAME, embeddings, qdrant_client

load_dotenv()

logger = logging.getLogger(__name__)

MAX_PDF_BYTES = int(os.getenv("MAX_PDF_BYTES", 50 * 1024 * 1024))  # e.g., 50MB
MAX_PAGES = int(os.getenv("MAX_PAGES", 500))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 100))

NAMESPACE = uuid.UUID("f0e1d2c3-b4a5-4678-9012-3456789abcde")

bucket_name = os.getenv("AWS_S3_BUCKET")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region_name = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name,
)


def ensure_collection_exists():
    if not qdrant_client.collection_exists(COLLECTION_NAME):
        qdrant_client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


def ingestion_worker(user_id: str, asset_id: str, bucket_name: str, s3_key: str) -> int:
    """
    ingestion work ingests given s3 pdf file into
    vector store
    """

    total_chunks = 0

    metadata = s3_client.head_object(Bucket=bucket_name, Key=s3_key)

    size = metadata["ContentLength"]

    if size <= 0 or size >= MAX_PDF_BYTES:
        raise ValueError(f"PDF size is not allowed: {size} bytes")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    ensure_collection_exists()

    batch = []

    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / f"{uuid.uuid4()}-document.pdf"
        logger.info("PDF path is %s", pdf_path)

        with pdf_path.open("wb") as output:
            s3_client.download_fileobj(bucket_name, s3_key, output)
            logger.info("file downloaded successfully at %s", pdf_path)

        # Basic file signature check
        with pdf_path.open("rb") as pdf_file:
            if pdf_file.read(5) != b"%PDF-":
                raise ValueError("The S3 object is not a valid PDF file")

        reader = PdfReader(str(pdf_path))

        try:
            if reader.is_encrypted:
                raise ValueError("Encrypted PDFs are not supported")

            if len(reader.pages) == 0 or len(reader.pages) > MAX_PAGES:
                raise ValueError("PDF page count is not allowed")

            def flush_batch():
                nonlocal total_chunks, batch

                if not batch:
                    return

                texts = [item["text"] for item in batch]
                vectors = embeddings.embed_documents(texts)

                points = [
                    PointStruct(id=item["id"], vector=vector, payload=item["payload"])
                    for item, vector in zip(batch, vectors)
                ]

                qdrant_client.upsert(
                    collection_name=COLLECTION_NAME, points=points, wait=True
                )

                total_chunks += len(points)
                batch = []

            for page_index, page in enumerate(reader.pages):
                page_text = page.extract_text() or ""

                if not page_text.strip():
                    continue

                chunks = splitter.split_text(page_text)

                for chunk_index, chunk in enumerate(chunks):
                    # Stable IDs make retries overwrite the same points
                    point_id = str(
                        uuid.uuid5(NAMESPACE, f"{asset_id}:{page_index}:{chunk_index}")
                    )

                    batch.append(
                        {
                            "id": point_id,
                            "text": chunk,
                            "payload": {
                                "user_id": user_id,
                                "asset_id": asset_id,
                                "page_number": page_index + 1,
                                "chunk_index": chunk_index,
                                "text": chunk,
                            },
                        }
                    )

                    if len(batch) >= BATCH_SIZE:
                        flush_batch()

            flush_batch()

        finally:
            reader.close()

    logger.info("Ingested %s chunks for asset %s", total_chunks, asset_id)

    return total_chunks
