from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Comment,Photo
from ..schemas import CommentCreate,CommentResponse
from ..auth.oauth2 import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["comments"]

)

@router.post(
    "/photos/{photo_id}",
    response_model=CommentResponse
)
def create_comment(
    photo_id:int,
    comment:CommentCreate,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):
    photo=(
        db.query(Photo).filter(Photo.id==photo_id).first()
        
    )
    if not photo:
        raise HTTPException(
            status_code=404,
            detail="Photo not found"
        )
    new_comment = Comment(
        body=comment.body,
        photo_id=photo_id,
        user_id=int(current_user["user_id"])
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/photos/{photo_id}",response_model=list[CommentResponse])
def get_comments(
    photo_id:int,
    db:Session=Depends(get_db)
):
    comments=(
        db.query(Comment).
        filter(Comment.photo_id==photo_id).
        order_by(Comment.created_at.desc()).
        all()
    )
    return comments