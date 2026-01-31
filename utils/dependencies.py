from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from utils.auth_utils import verify_token

security = HTTPBearer()

def get_current_user(credentials=Depends(security)):
    try:
        token = credentials.credentials
        return verify_token(token)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

def role_required(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user["role"] != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized"
            )
        return user
    return role_checker
