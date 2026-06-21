from sqlalchemy import Column,Integer,String,Boolean,Text,ForeignKey,DateTime
from sqlalchemy .orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email =Column(String,unique=True,nullable=False,index=True)
    username=Column(String,nullable=False)
    hashed_password=Column(String,nullable=False)
    is_admin=Column(Boolean,default=False)
    created_at=Column(DateTime(timezone=True),server_default=func.now())

    comments=relationship("Comment",back_populates="user")

class Gallery(Base): 
    __tablename__ ="galleries"
    id = Column(Integer,primary_key=True ,index=True)
    slug = Column(String,unique=True,nullable=False)
    title = Column(String,nullable=False)

    photos = relationship("Photo", back_populates="gallery")

class Photo(Base):
    __tablename__ = "photos"
    id = Column(Integer,primary_key=True,index=True)
    gallery_id = Column(Integer,ForeignKey("galleries.id"))
    filename=Column(String,nullable=False)
    caption=Column(String,nullable=True)
    sort_order=Column(Integer,default=0)
    uploaded_at=Column(DateTime(timezone=True),server_default=func.now())

    gallery = relationship("Gallery",back_populates="photos")
    comments= relationship("Comment",back_populates="photo")

class Comment(Base):
    __tablename__ ="comments"
    id = Column(Integer,primary_key =True,index=True)
    photo_id = Column(Integer,ForeignKey("photos.id"))
    user_id = Column(Integer,ForeignKey("users.id"))
    body = Column(Text,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())

    photo = relationship("Photo",back_populates="comments")
    user=relationship("User",back_populates="comments")

class PageView(Base):
    __tablename__ = "page_views"
    id = Column(Integer,primary_key=True,index=True)
    path = Column(String,nullable=False)
    viewed_at = Column(DateTime(timezone=True),server_default=func.now())

   