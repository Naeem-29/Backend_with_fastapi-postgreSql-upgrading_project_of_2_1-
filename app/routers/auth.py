from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import UserCreate,UserResponse,Token
from ..auth.hashing import hash_password,verify_password
from ..auth.jwt_handler import create_access_token
from ..auth.oauth2 import get_current_admin

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register",response_model=UserResponse,status_code=201)
def register(user_data:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter(User.email==user_data.email).first()
    if existing_user :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed=hash_password(user_data.password)
    new_user=User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=Token)
def login(
    form_data:OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(get_db)
):
    user=(
        db.query(User).filter(User.email==form_data.username).first()
    )
    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials")
    
    access_token=create_access_token(
        data={
            "user_id":str(user.id),
            "is_admin":user.is_admin
        }
    )
    return{
        "access_token": access_token,
        "token_type":"bearer"
    }

