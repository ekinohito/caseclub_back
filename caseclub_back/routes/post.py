from typing import List, Optional
from ..db.models import PostCreate, PostRead, Post
from ..db.database import engine
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select

router = APIRouter(prefix="/post", tags=["post"])

@router.post("/", response_model=PostRead)
async def create_post(post: PostCreate):
    with Session(engine) as session:
        post = Post.from_orm(post)
        session.add(post)
        session.commit()
        session.refresh(post)
        return post

@router.get("/", response_model=List[PostRead])
async def get_posts(offset: int=0, limit: int=20):
    with Session(engine) as session:
        return session.exec(select(Post).offset(offset).limit(limit).order_by(Post.created_at)).all()

@router.get("/{id}", response_model=PostRead, responses={404: {"description": "Not found"}})
async def get_posts(id: int):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == id)).first()
        if post is None:
            raise HTTPException(404, "Post not found")
        return post

@router.delete("/{id}", response_model=PostRead, responses={404: {"description": "Not found"}})
async def delete_post(id: int):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == id)).first()
        if post is None:
            raise HTTPException(404, "Post not found")
        session.delete(post)
        session.commit()
        return post
    

@router.post("/like/{id}", response_model=int)
async def like_post(id: int, remove: Optional[bool]=False):
    with Session(engine) as session:
        post = session.exec(select(Post).where(Post.id == id)).first()
        if (post is None):
            raise HTTPException(404, "Post not found")
        if remove:
            post.likes -= 1
        else:
            post.likes += 1
        session.add(post)
        session.commit()
        return post.likes