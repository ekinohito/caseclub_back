from fastapi import APIRouter
from ..db.populate import load

router = APIRouter(prefix="/management", tags=["management"])

@router.get("/reload_db")
async def reload_db():
    load()
    return "ok"
