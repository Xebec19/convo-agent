import logging
import tempfile
from pathlib import Path

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client.models import PointStruct
from dotenv import load_dotenv
import os
import boto3
import uuid

load_dotenv()

logger = logging.getLogger(__name__)

BATCH_SIZE = 32
MAX_PDF_BYTES = 100 * 1024 * 1024
MAX_PAGES = 2_000

bucket_name = os.getenv("AWS_S3_BUCKET")
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region_name = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    aws_region_name=aws_region_name,
)


def ingest_pdf_from_s3(
    bucket_name: str,
    object_key: str,
    user_id: str,
    asset_id: str,
) -> int:
    # Check the remote object's size before downloading
    metadata = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    size = metadata["ContentLength"]

    if size <= 0 or size > MAX_PDF_BYTES:
        raise ValueError("PDF size is not allowed: {size} bytes")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    total_chunks = 0
    batch = []

    # Download resource to disk
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_path = Path(temp_dir) / f"{uuid.uuid4()}-document.pdf"

        with pdf_path.open("wb") as output:
            s3_client.download_fileobj(
                bucket_name,
                object_key,
                output
            )

        # Parse and process one page at a time
        reader = PdfReader(str[pdf_path])

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
                    PointStruct(
                        id=item["id"],
                        vector=vector,
                        payload=item["payload"],
                    )
                    for item, vector in zip(batch,vectors)
                ]

                qdrant_client.upsert(
                    collection_name=COLLECTION_NAME,
                    points=points,
                    wait=True
                )

                total_chunks += len(points)
                batch = []

            for page_index, page in enumerate(chunks):
                point_id = str(uuid.uuid5(
                    NAMESPACE,
                    f"{asset_id}:{page_index}:{chunk_index}"
                ))

                batch.append({
                    "id": point_id,
                    "text": chunk,
                    "payload": {
                        "user_id": user_id,
                        "asset_id": asset_id,
                        "page_number": page_index + 1,
                        "chunk_index": chunk_index,
                        "text": chunk
                    },
                })

                if len(batch) >= BATCH_SIZE:
                    flush_batch()

        flush_batch()

    finally:
        render.close()

    