import io
import os

import boto3
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient, models
from sqlalchemy import select, update
from pypdf import PdfReader
from db.db import SessionLocal
from db.models.asset_model import Asset
from logger import logger

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
    logger.info("DB connection opened")

    logger.info("Job starting for asset: %d , user_id: %d", id, user_id)

    try:
        asset = db.execute(
            select(Asset).where(Asset.asset_id == id).where(Asset.user_id == user_id)
        ).scalar()

        if asset is None:
            logger.info("Asset not found! asset id: %d, user id: %d", id, user_id)
            return

        fileReader = get_s3_file(bucket_name=bucket_name, object_key=asset.asset_key)

        buffer = PdfReader(fileReader)

        text = "\n".join(page.extract_text() or "" for page in buffer.pages)

        logger.info("Asset %d is being downloaded from S3", id)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
        )

        chunks = splitter.create_documents([text])

        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )

        ensure_collection()
        logger.info("%s collection exists in vectoredb", collection)

        # save in vectordb
        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            url="http://localhost:6333",
            collection_name=collection,
        )

        logger.info("Embeddings saved for Asset %d", id)

        db.execute(
            update(Asset)
            .where(Asset.asset_id == id)
            .where(Asset.user_id == user_id)
            .values({"is_ingested": True})
        )

        logger.info("Asset %s finished ingestion", id)

        return id

    except Exception as e:
        logger.error("Ingestion failed for asset %d: %s", id, e)

    finally:
        db.close()
        logger.info("DB connection closed")


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
