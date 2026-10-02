import io
import os

import boto3
from dotenv import load_dotenv
from sqlalchemy import select

from db.db import SessionLocal
from db.models.asset_model import Asset
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

bucket_name = os.getenv("AWS_S3_BUCKET") or ""
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region_name = os.getenv("AWS_REGION")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name,
)


def ingestion_worker(id: int):
    db = SessionLocal()

    try:
        asset = db.execute(
            select(Asset).where(Asset.asset_id == id).where(Asset.asset_id == id)
        ).scalar()

        fileReader = get_s3_file(bucket_name=bucket_name, object_key=asset.asset_name)

        pages = []

        for page in fileReader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        doc = "\n".join(pages)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = splitter.create_documents([doc])

        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

    finally:
        db.close()


def get_s3_file(bucket_name: str, object_key: str) -> io.BytesIO:
    response = s3_client.get_object(Bucket=os.getenv("AWS_S3_BUCKET"), Key=object_key)

    return io.BytesIO(response["Body"].read())
