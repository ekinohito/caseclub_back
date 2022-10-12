from fastapi import APIRouter, File, Depends, HTTPException
from fastapi.responses import StreamingResponse, Response

from ..db.models import Image
from ..db.database import get_session
from sqlmodel import Session, select, SQLModel

router = APIRouter(prefix="/images", tags=["images"])

class ImageRead(SQLModel):
    id: int

@router.post('/', response_model=ImageRead)
async def upload_image(file: bytes = File(), session: Session = Depends(get_session)):
    image = Image(data=file)
    session.add(image)
    session.commit()
    return {"id": image.id}

@router.get('/{id}', responses={
        200: {
            "content": {"image/*": {}},
            "description": "Returns an image.",
        }
    },
    response_class=Response
)
def get_image(id: int, session: Session = Depends(get_session)):
    image = session.exec(select(Image).where(Image.id == id)).first()
    if image is None:
        raise HTTPException(404, 'Not found')
    def wrapper():
        yield image.data
    return StreamingResponse(wrapper(), media_type="image/png")