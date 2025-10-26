import hashlib
import hmac
import os
import secrets

SECRET_KEY = os.getenv("SECRET_KEY").encode()


def hash_password(password: str) -> str:
    return hmac.new(SECRET_KEY, password.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    computed_hash = hmac.new(
        SECRET_KEY, plain_password.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_hash, hashed_password)


def generate_random_password(length: int = 12) -> str:
    return secrets.token_urlsafe(length)
