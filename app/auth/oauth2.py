from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from .jwt_handler import SECRET_KEY,ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")
        is_admin=payload.get("is_admin")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return {
            "user_id": user_id,
            "is_admin": is_admin
        }

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


def get_current_user(
    token: str = Depends(oauth2_scheme)
):
    return verify_access_token(token)

def get_current_admin(
        current_user=Depends(get_current_user)
):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )
    return current_user