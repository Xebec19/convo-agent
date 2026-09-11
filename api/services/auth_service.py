from datetime import UTC, datetime, timedelta

from jose import jwt
from pwdlib import PasswordHash

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
COOKIE_NAME = "access_token"

password_hash = PasswordHash.recommended()


def createHash(password: str) -> str:
    return password_hash.hash(password=password)


def verifyHash(password: str, hash: str) -> bool:
    return password_hash.verify(password=password, hash=hash)


def createAccessToken(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return jwt.encode(
        {"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM
    )
