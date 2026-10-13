import os
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is not defined")

ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Seuls les algorithmes à clé partagée sont acceptés : la clé est un secret unique.
if ALGORITHM not in {"HS256", "HS384", "HS512"}:
    raise ValueError("JWT_ALGORITHM must be HS256, HS384 or HS512")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60")
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# bcrypt ne lit que les 72 premiers octets : on tronque explicitement, comme le faisait passlib,
# pour que les empreintes existantes restent valides.
BCRYPT_MAX_BYTES = 72


def _password_bytes(password: str) -> bytes:
    return password.encode("utf-8")[:BCRYPT_MAX_BYTES]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_password_bytes(password), bcrypt.gensalt()).decode("ascii")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(
            _password_bytes(plain_password), hashed_password.encode("ascii")
        )
    except ValueError:
        return False


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        return None
