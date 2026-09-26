import os
from datetime import UTC, datetime, timedelta

from dotenv import load_dotenv
from jose import jwt
from pwdlib import PasswordHash

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_NAME = os.getenv("COOKIE_NAME") or ""

password_hash = PasswordHash.recommended()


def createHash(password: str) -> str:
    return password_hash.hash(password=password)


def verifyHash(password: str, hash: str) -> bool:
    return password_hash.verify(password=password, hash=hash)


def createAccessToken(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    if SECRET_KEY is None:
        raise ValueError("secret key not found!")

    return jwt.encode(
        {"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
    )


# def verifyAccessToken
