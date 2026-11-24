
from database import get_db
from db.models.conversation_model import Conversation
from db.models.message_model import Message
from db.models.user_model import User
from fastapi import APIRouter, Depends, HTTPException, status
from logger import logger
from schemas.messages import MessageRequest
from schemas.response import APIResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.middlewares.authentication import get_current_user

router = APIRouter(
    prefix="/messages", dependencies=[Depends(get_current_user)], tags=["messages"]
)


@router.post("/create", response_model=APIResponse)
async def create_message(
    request: MessageRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> APIResponse:

    if request.conversation_id == "" or request.conversation_id == None:
        logger.error("message creation failed! conversation ID missing.")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid request")

    conversation = db.execute(
        select(Conversation)
        .where(Conversation.conversation_id == request.conversation_id)
        .where(Conversation.user_id == user.user_id)
    )

    if conversation is None:
        logger.error("message creation failed! conversation not found.")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "bad request")

    message = Message(conversation_id=request.conversation_id, content=request.content)

    db.add(message)
    db.commit()

    # qdrant_client.

    return APIResponse(status=True, data="", message="message posted successfully")
