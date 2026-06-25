
from typing import Optional
from pydantic import BaseModel , EmailStr


class GalleryResponse(BaseModel):
    id: int
    slug: str
    title: str

    class Config:
        from_attributes = True


class PhotoResponse(BaseModel):
    id: int
    filename: str
    caption: Optional[str]
    sort_order: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_admin: bool

    class Config:
        from_attributes = True  

class Userlogin(BaseModel):
    email:EmailStr
    password: str

class Token(BaseModel):
     access_token: str
     token_type: str

