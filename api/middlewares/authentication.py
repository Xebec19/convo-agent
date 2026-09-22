import os

from dotenv import load_dotenv
from fastapi import HTTPException, status, Request
from jose import JWTError, jwt
from server import app
from services.auth_service import COOKIE_NAME

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY") or ""
ALGORITHM = "HS256"


@app.middleware("http")
async def get_current_user(request: Request, call_next):
    # access_token: str | None = Cookie(default=None)

    cookie_key = os.getenv(COOKIE_NAME)

    if cookie_key is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

        print(user_id)
        call_next(request)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )
