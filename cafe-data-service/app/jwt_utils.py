from datetime import datetime, timedelta, timezone
from jose import jwt
from app.config import settings

def create_access_token(data: dict):
    """
    Gera um token JWT com expiração embutida.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)