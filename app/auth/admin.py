from fastapi import APIRouter,Depends,HTTPException,status
from .oauth2 import get_current_user

def get_current_admin(
        current_user=Depends(get_current_user)
):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

