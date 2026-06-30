from fastapi import APIRouter,Depends,UploadFile,File,Form
from ..auth.oauth2 import get_current_admin
from fastapi import UploadFile,File,Form

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/photos")
def upload_photo(
    title: str=Form(...),
    description: str = Form(...),
    gallery_id: int = Form(...),
    image:UploadFile = File(...),
    current_admin=Depends(get_current_admin)
):
    return{
         "title": title,
        "description": description,
        "gallery_id":gallery_id,
        "filename":image.filename,
        "content_type":image.content_type
    }

   