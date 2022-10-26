
from .db.models.user import User
from .db.models.post import Post
from .db.models.image import Image
from .db.models.event import Event
from sqladmin import ModelView


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.liked_posts]

class PostAdmin(ModelView, model=Post):
    column_list = [Post.id, Post.text]

class ImageAdmin(ModelView, model=Image):
    pass

class EventAdmin(ModelView, model=Event):
    pass