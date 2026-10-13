import logging
import os

import boto3
from dotenv import load_dotenv

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
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name,
)


def ingestion_worker(user_id: str, asset_id: str, bucket_name: str, s3_key: str) -> int:

    metadata = s3_client.head_object(Bucket=bucket_name, Key=s3_key)

    size = metadata["ContentLength"]

    if size <= 0 or size >= MAX_PDF_BYTES:
        raise ValueError(f"PDF size is not allowed: {size} bytes")

    # splitter = Recurs

    return 0
