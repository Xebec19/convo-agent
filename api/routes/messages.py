from fastapi import APIRouter, Depends

from api.middlewares.authentication import get_current_user
from database import get_db
from db.models.user_model import User
from schemas.response import APIResponse
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/messages", dependencies=[Depends(get_current_user)], tags=["messages"]
)


@router.post("/create", response_model=APIResponse)
async def create_message(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
) -> APIResponse:

    return APIResponse(status=True, data="", message="message posted successfully")
