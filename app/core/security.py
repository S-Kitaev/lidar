import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from lidar.app.core.config import settings
from jwt import PyJWTError, ExpiredSignatureError

# Читаем ключи единожды
with open(settings.JWT_PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()
with open(settings.JWT_PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

def hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode(), salt).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, PRIVATE_KEY, algorithm="RS256")

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"],
            options={"verify_exp": True}  # Явная проверка срока действия
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )