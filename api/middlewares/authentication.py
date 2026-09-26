import os

from database import get_db
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from models.session_model import Session as SessionSchema
from models.user_model import User
from server import app
from models.asset_model import AssetStatus
from services.auth_service import COOKIE_NAME
from sqlalchemy import select
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY") or ""
ALGORITHM = "HS256"


# @app.middleware("http")
async def get_current_user(request: Request, db: Session = Depends(get_db)):

    cookie_key = COOKIE_NAME

    access_token = request.cookies.get(cookie_key)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    try:
        payload = jwt.decode(token=access_token, key=SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        session = db.execute(
            select(SessionSchema)
            .where(SessionSchema.token == access_token)
            .where(SessionSchema.user_id == int(user_id))
            .where(SessionSchema.status == AssetStatus.ACTIVE)
        ).scalar()

        if session is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        user = db.execute(select(User).where(User.id == int(user_id))).scalars().one()

        return User(
            id=user.id, name=user.name, email=user.email, phone_num=user.phone_num
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
