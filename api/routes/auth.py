from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from models.user_model import User
from schemas.auth import SignInRequest, SignUpRequest
from services.auth_service import createHash
from sqlalchemy import func, select
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(
    request: SignUpRequest,
    db: Session = Depends(get_db),  # noqa: B008
    status_code=201,
):

    query = (
        select(func.count())
        .select_from(User)
        .where(func.lower(User.name) == request.email.lower())
    )

    count = db.scalar(query)

    if count > 0:
        raise HTTPException(status_code=401, detail="User is already present")

    existing_user = (
        db.query(User).filter(func.lower(User.name) == request.email.lower()).first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    password_hash = createHash(request.password)

    user = User(
        name=request.name,
        phone_num=request.phoneNum,
        email=request.email,
        password_hash=password_hash,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"id": user.id, "email": user.email}


@router.get("/signin")
async def signin(request: SignInRequest):
    pass
