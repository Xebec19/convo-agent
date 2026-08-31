from fastapi import APIRouter

from api.schemas.auth import SignInRequest, SignUpRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(request: SignUpRequest):
    pass


@router.get("/signin")
async def signin(request: SignInRequest):
    pass
