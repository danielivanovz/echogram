from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from api.routers.auth import decode_access_token

security = HTTPBearer()


def get_current_user(token: HTTPAuthorizationCredentials = Security(security)):
    try:
        return decode_access_token(token.credentials)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
