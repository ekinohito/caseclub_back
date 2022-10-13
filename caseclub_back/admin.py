
from .db.models import Image, Post, User
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.liked_posts]

class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.text]

class ImageAdmin(ModelView, model=Image):
    pass
