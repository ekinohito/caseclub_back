from typing import List, Optional
from .auth import get_current_user
from ..db.models import PostCreate, PostEdit, PostRead, Post, UserLikesPost
from ..db.database import get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session

router = APIRouter(prefix="/post", tags=["post"])

async def get_post(id: int, session: Session = Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == id)).first()
    if post is None:
        raise HTTPException(404, "Post not found")
    return post

@router.post("/", response_model=PostRead)
async def create_post(post: PostCreate, session:Session=Depends(get_session)):
    post = Post.from_orm(post)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@router.get("/", response_model=List[PostRead])
async def get_posts(offset: int=0, limit: int=20, session:Session=Depends(get_session)):
    return session.exec(select(Post).offset(offset).limit(limit).order_by(Post.created_at.desc())).all()

@router.get("/{id}", response_model=PostRead, responses={404: {"description": "Not found"}})
async def get_post(id: int, session:Session=Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == id)).first()
    if post is None:
        raise HTTPException(404, "Post not found")
    return post

@router.delete("/{id}", response_model=PostRead, responses={404: {"description": "Not found"}})
async def delete_post(id: int, session:Session=Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == id)).first()
    if post is None:
        raise HTTPException(404, "Post not found")
    session.delete(post)
    session.commit()
    return post
    

@router.post("/like/{id}", response_model=int)
async def like_post(id: int, remove: Optional[bool]=False, user=Depends(get_current_user), session:Session=Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == id)).first()
    if (post is None):
        raise HTTPException(404, "Post not found")
    is_liked = session.exec(
        select(UserLikesPost).where(UserLikesPost.user_id == user.id, UserLikesPost.post_id == post.id)
        ).first() is not None
    if remove != is_liked:
        raise HTTPException(400, 'Already liked/disliked')
    if remove:
        post.likes -= 1
        post.users.remove(user)
    else:
        post.likes += 1
        post.users.append(user)
    session.add(post)
    session.commit()
    return post.likes

@router.patch("/{id}")
async def edit_post(id: int, patch: PostEdit, session:Session=Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == id)).first()
    for k, v in patch.dict(exclude_unset=True).items():
        setattr(post, k, v)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post