import os
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from database import get_db
from db.models.asset_model import Asset
from db.models.user_model import User
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from jobs.worker import ingestion_worker
from logger import logger
from middlewares.authentication import get_current_user
from rqclient.client import queue
from schemas.response import APIResponse
from sqlalchemy.orm import Session

load_dotenv()

router = APIRouter(
    prefix="/assets", dependencies=[Depends(get_current_user)], tags=["assets"]
)

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


@router.post("/upload", response_model=APIResponse)
async def upload_assset(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> APIResponse:
    try:
        s3_key = f"rag-folder/uploads/{uuid4()}-{file.filename}"

        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            s3_key,
            ExtraArgs={"ContentType": file.content_type or "application/octet-stream"},
        )

        url = f"https://{bucket_name}.s3.{aws_region_name}.amazonaws.com/{s3_key}"

        logger.info("Asset uploaded to S3: %s", url)

        asset = Asset(asset_key=s3_key, url=url, user_id=user.id)

        db.add(asset)
        db.commit()
        db.refresh(asset)

        logger.info("Asset saved in DB: %d", asset.asset_id)

        queue.enqueue(ingestion_worker, asset.asset_id, user.id)

        logger.info("Asset enqueued for ingestion: %d", asset.asset_id)

        return APIResponse(
            status=True, data=asset.asset_id, message="File uploaded successfully"
        )
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail="Failed to upload file to S3"
        ) from e
