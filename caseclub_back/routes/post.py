from typing import List, Optional
from .auth import get_current_user, require_current_user
from ..db.models.post import PostCreate, PostEdit, PostRead, Post
from ..db.models.image import Image
from ..db.models.user import User, UserLikesPost
from ..db.database import get_session
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session, and_

router = APIRouter(prefix="/post", tags=["post"])

async def get_post(id: int, session: Session = Depends(get_session)):
    post = session.exec(select(Post).where(Post.id == id)).first()
    if post is None:
        raise HTTPException(404, "Post not found")
    return post

@router.post("/", response_model=PostRead)
async def create_post(post: PostCreate, session:Session=Depends(get_session)):
    images = post.images
    post: Post = Post.from_orm(post)
    session.add(post)
    session.commit()
    session.refresh(post)
    for image in images:
        image: Image = session.exec(select(Image).where(Image.id == image)).first()
        if image is None:
            continue
        post.images.append(image)
    session.add(post)
    session.commit()
    session.refresh(post)
    return PostRead.from_orm(post, {"images": [image.id for image in post.images]})

@router.get("/", response_model=List[PostRead])
async def get_posts(offset: int=0, limit: int=20, session:Session=Depends(get_session), user:Optional[User] = Depends(get_current_user)):
    if user is None:
        posts = session.exec(select(Post).offset(offset).limit(limit).order_by(Post.created_at.desc())).all()
        return [PostRead.from_orm(post, {'images': [image.id for image in post.images]}) for post in posts]
    postsWithLikes = session.exec(
        select(Post, UserLikesPost)
        .join(UserLikesPost, isouter=True, onclause=and_(UserLikesPost.post_id == Post.id, UserLikesPost.user_id == user.id))
        .offset(offset)
        .limit(limit)
        .order_by(Post.created_at.desc())
        ).all()
    print(postsWithLikes)
    return [PostRead.from_orm(post, {'is_liked': like is not None, 'images': [image.id for image in post.images]}) for post, like in postsWithLikes]

id_router = APIRouter(prefix="/{id}")

@id_router.get("/", response_model=PostRead, responses={404: {"description": "Not found"}})
async def get_post(post: Post = Depends(get_post)):
    return post

@id_router.delete("/", response_model=PostRead, responses={404: {"description": "Not found"}})
async def delete_post(session:Session=Depends(get_session), post: Post = Depends(get_post)):
    session.delete(post)
    session.commit()
    return post
    

@id_router.post("/like", response_model=int)
async def like_post(remove: Optional[bool]=False, user: User=Depends(require_current_user), session:Session=Depends(get_session), post: Post = Depends(get_post)):
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

@id_router.patch("/")
async def edit_post(id: int, patch: PostEdit, session:Session=Depends(get_session), post: Post = Depends(get_post)):
    post = session.exec(select(Post).where(Post.id == id)).first()
    for k, v in patch.dict(exclude_unset=True).items():
        setattr(post, k, v)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

router.include_router(id_router)