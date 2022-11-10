from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from .admin import add_admin
from .routes import post, user, auth, images, event, management
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:3030",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory="caseclub_back/public"), name="static")
@app.get('/favicon.ico')
def favicon():
    return RedirectResponse('/static/favicon.ico', status_code=308)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(images.router)
app.include_router(event.router)
app.include_router(management.router)

add_admin(app)
