
from .db.models.user import User
from .db.models.post import Post
from .db.models.image import Image
from .db.models.event import Event
from sqladmin import ModelView, Admin
from fastapi import FastAPI
from .db.database import engine


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.name]

class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.text, Post.likes]

class ImageAdmin(ModelView, model=Image):
    column_list = [Image.id]

class EventAdmin(ModelView, model=Event):
    column_list = [Event.id, Event.icon, Event.title]

def add_admin(app: FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserAdmin)
    admin.add_view(PostAdmin)
    admin.add_view(ImageAdmin)
    admin.add_view(EventAdmin)