from ..db.models import User, UserCreate
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def register_user(user_create: UserCreate) -> User:
    hashed_password = get_password_hash(user_create.password)
    return User.from_orm(user_create, {"hashed_password": hashed_password})