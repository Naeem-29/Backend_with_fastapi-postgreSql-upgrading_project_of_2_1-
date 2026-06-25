import os
from dotenv import load_dotenv

from jose import jwt
from datetime import datetime, timedelta,timezone

load_dotenv()
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_DAYS=int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS",30)  )

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM)
    return encoded_jwt
