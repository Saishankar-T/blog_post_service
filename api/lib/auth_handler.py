from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.lib.jwt_handler import verify_token

# HTTPBearer security mechanism
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    username = verify_token(token)
    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return username
