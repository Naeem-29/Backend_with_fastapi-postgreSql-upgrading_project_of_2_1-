# app/routers/galleries.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Gallery, Photo
from ..schemas import GalleryResponse, PhotoResponse

router = APIRouter(
    prefix="/galleries",
    tags=["Galleries"]
)

@router.get("/", response_model=list[GalleryResponse])
def get_galleries(db: Session = Depends(get_db)):
    galleries = db.query(Gallery).all()
    return galleries

@router.get("/{slug}/photos", response_model=list[PhotoResponse])
def get_gallery_photos(
    slug: str,
    db: Session = Depends(get_db)
):
    gallery = (
        db.query(Gallery)
        .filter(Gallery.slug == slug)
        .first()
    )

    if not gallery:
        raise HTTPException(
            status_code=404,
            detail="Gallery not found"
        )

    photos = (
        db.query(Photo)
        .filter(Photo.gallery_id == gallery.id)
        .order_by(Photo.sort_order)
        .all()
    )

    return photos
