from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models.user_model import User
from schemas.auth import SignInRequest, SignUpRequest
from services.auth_service import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    COOKIE_NAME,
    createAccessToken,
    createHash,
    verifyHash,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(
    request: SignUpRequest,
    db: Session = Depends(get_db),  # noqa: B008
):

    query = (
        select(func.count())
        .select_from(User)
        .where(func.lower(User.name) == request.email.lower())
    )

    count = db.scalar(query)

    if count is None or count > 0:
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


@router.post("/signin")
async def signin(
    request: SignInRequest,
    response: Response,
    db: Session = Depends(get_db),
):

    user = db.execute(
        select(User).where(func.lower(User.email) == request.email.lower())
    ).scalar()

    if user is None or verifyHash(request.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid credentials")

    token = createAccessToken(user.id)

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
    )

    return {"message": "Logged in"}
