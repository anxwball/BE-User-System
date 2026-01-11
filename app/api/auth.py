
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token


oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user_email(token: str = Depends(oauth_scheme)) -> str:
    try:
        return decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
