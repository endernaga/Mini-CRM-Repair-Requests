import os
from datetime import datetime, timedelta
from typing import Any

import jwt

SECRET_KEY = os.getenv("SECRET_KEY").encode()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3600 * 24
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict[str, Any], expires_delta: int | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, Any], expires_delta: int | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        days=expires_delta or REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return {}
