from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from dotenv import load_dotenv
from pytz import timezone

from app.core.config import get_module_secret

load_dotenv()

SECURITY_SECRET_KEY = get_module_secret("SECURITY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone('UTC')) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": subject,
        "exp": expire
    }
    return jwt.encode(payload, SECURITY_SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECURITY_SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise ValueError("Invalid token")