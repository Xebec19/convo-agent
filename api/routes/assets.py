import os
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from middlewares.authentication import get_current_user
from schemas.response import APIResponse

load_dotenv()

router = APIRouter(
    prefix="/assets", dependencies=[Depends(get_current_user)], tags=["assets"]
)

bucket_name = os.getenv("AWS_S3_BUCKET")

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)


@router.post("/upload", response_model=APIResponse)
async def upload_assset(file: UploadFile = File(...)) -> APIResponse:
    try:
        s3_key = f"rag-folder/uploads/{uuid4()}-{file.filename}"

        s3_client.upload_fileobj(
            file.file,
            bucket_name,
            s3_key,
            ExtraArgs={"ContentType": file.content_type or "application/octet-stream"},
        )

        return APIResponse(
            status=True, data=file.filename or "", message="File uploaded successfully"
        )
    except ClientError as e:
        raise HTTPException(
            status_code=500, detail="Failed to upload file to S3"
        ) from e
