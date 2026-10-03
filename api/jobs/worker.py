import io
import os

import boto3
from dotenv import load_dotenv
from sqlalchemy import select, update

from db.db import SessionLocal
from db.models.asset_model import Asset
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore

load_dotenv()

bucket_name = os.getenv("AWS_S3_BUCKET") or ""
aws_access_key = os.getenv("AWS_ACCESS_KEY")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region_name = os.getenv("AWS_REGION")
collection = os.getenv("COLLECTION_NAME") or ""

s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region_name,
)

qdrant = QdrantClient(url="http://localhost:6333")


def ingestion_worker(id: int, user_id: int):
    db = SessionLocal()

    try:
        asset = db.execute(
            select(Asset).where(Asset.asset_id == id).where(Asset.user_id == user_id)
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

        ensure_collection()

        # save in vectordb
        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            url="http://localhost:6333",
            collection_name=collection,
        )

        db.execute(
            update(Asset)
            .where(Asset.asset_id == id)
            .where(Asset.user_id == user_id)
            .values({"is_ingested": True})
        )

    finally:
        db.close()


def get_s3_file(bucket_name: str, object_key: str) -> io.BytesIO:
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)

    return io.BytesIO(response["Body"].read())


def ensure_collection():
    if not qdrant.collection_exists(collection):
        qdrant.create_collection(
            collection_name=collection,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE,
            ),
        )
