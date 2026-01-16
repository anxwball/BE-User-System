from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError

from app.core.config import get_module_secret

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def _ensure_secret(secret_key: Optional[str]) -> str:
    if secret_key:
        return secret_key
    return get_module_secret("SECURITY")


def create_access_token(subject: str, secret_key: Optional[str] = None, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT for `subject` using `secret_key` (injected).

    If `secret_key` is not provided, fall back to the module-secret lookup.
    The `exp` claim is emitted as an integer UNIX timestamp for broad compatibility.
    """
    secret = _ensure_secret(secret_key)
    expire_dt = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {
        "sub": subject,
        # Emit `exp` as an integer UNIX timestamp (seconds since epoch).
        # Using timezone-aware UTC datetimes avoids ambiguity when parsing
        # tokens in different environments.
        "exp": int(expire_dt.timestamp())
    }
    return jwt.encode(payload, secret, algorithm=ALGORITHM)


def decode_access_token(token: str, secret_key: Optional[str] = None) -> str:
    try:
        secret = _ensure_secret(secret_key)
        payload = jwt.decode(token, secret, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise ValueError("Invalid token")