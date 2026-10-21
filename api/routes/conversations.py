from fastapi import APIRouter, Depends

from api.middlewares.authentication import get_current_user

router = APIRouter(
    prefix="/conversations",
    dependencies=[Depends(get_current_user)],
    tags=["conversations"],
)
