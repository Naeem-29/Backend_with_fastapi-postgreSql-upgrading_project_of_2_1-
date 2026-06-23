from pydantic import BaseModel
from typing import Optional


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