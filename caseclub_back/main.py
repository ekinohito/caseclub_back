from fastapi import FastAPI

from .admin import ImageAdmin, PostAdmin, UserAdmin
from .routes import post, user, auth, images
from .db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(images.router)


admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(PostAdmin)
admin.add_view(ImageAdmin)
