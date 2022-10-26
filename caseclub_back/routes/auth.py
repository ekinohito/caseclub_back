from typing import Optional

from ..utils.password_hash import verify_password
from ..db.models.user import UserRead, User
from ..db.database import engine
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):
    if token is None:
        return None
    try:
        user = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id = user.get('id')
        if not id:
            return None
        with Session(engine) as session:
            user: User = session.exec(select(User).where(User.id == id)).first()
            if not user:
                return None
            return user
    except JWTError:
        return None

async def require_current_user(user: Optional[User] = Depends(get_current_user)):
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


class Token(BaseModel):
    access_token: str
    token_type: str

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        email = form_data.username
        password = form_data.password
        user = session.exec(select(User).where(User.email == email)).first()
        if user is None:
            raise HTTPException(401, "Wrong email/password")
        if not verify_password(password, user.hashed_password):
            raise HTTPException(401, "Wrong email/password")
        return {"access_token": jwt.encode(UserRead.from_orm(user).dict(), SECRET_KEY, ALGORITHM), "token_type": "bearer"}

