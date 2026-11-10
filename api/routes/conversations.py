from database import get_db
from db.models.conversation_model import Conversation
from db.models.user_model import User
from fastapi import APIRouter, Depends
from logger import logger
from middlewares.authentication import get_current_user
from schemas.response import APIResponse
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/conversations",
    dependencies=[Depends(get_current_user)],
    tags=["conversations"],
)


# TODO Test this route
@router.post("/create", response_model=APIResponse)
async def createConverstation(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> APIResponse:

    conversation = Conversation(user_id=user.user_id)

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    logger.info(
        "conversation %d created, user id: %d",
        conversation.conversation_id,
        conversation.user_id,
    )

    return APIResponse(
        status=True,
        data=conversation.conversation_id,
        message="Conversation created successfully",
    )
