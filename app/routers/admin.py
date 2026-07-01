from fastapi import APIRouter,Depends,UploadFile,File,Form,HTTPException
from ..auth.oauth2 import get_current_admin
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Gallery,Photo
import os 
import shutil
import uuid

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)
UPLOAD_DIR="app/static/uploads"
@router.post("/photos")

def upload_photo(
    gallery_id: int=Form(...),
    caption: str = Form(...),
    sort_order: int = Form(0),
    image:UploadFile = File(...),
    current_admin=Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    gallery = (
        db.query(Gallery).filter(
            Gallery.id==gallery_id).first()
        )
    if gallery is None:
        raise HTTPException(
            status_code=404,
            detail="Gallery not found"
        )
    
    extension = os.path.splitext(image.filename)[1]
    filename=f"{uuid.uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR, filename
    )

    with open(file_path,"wb") as buffer:
        shutil.copyfileobj(image.file,buffer)

    new_photo=Photo(
        gallery_id=gallery_id,
        filename=filename,
        caption=caption,
        sort_order=sort_order
    )
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return{
        "message":"Photo uploaded successfully",
        "photo_id":new_photo.id,
        "filename":new_photo.filename,
        "caption":new_photo.caption
    }
 
   

   