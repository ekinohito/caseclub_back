from fastapi import APIRouter, File, Depends, HTTPException, UploadFile
from fastapi.responses import Response
from ..db.models.image import Image, ImageRead
from ..db.database import get_session
from sqlmodel import Session, select

router = APIRouter(prefix="/images", tags=["images"])

@router.post('/', response_model=ImageRead)
async def upload_image(file: UploadFile = File(), session: Session = Depends(get_session)):
    content_type = file.headers.get('content-type')
    if content_type is None:
        raise HTTPException(400, 'Missing Content-Type Header')
    image = Image(data=await file.read(), content_type=content_type)
    session.add(image)
    session.commit()
    return image

@router.get('/{id}', responses={
        200: {
            "content": {"image/png": {}},
            "description": "Returns an image.",
        }
    },
    response_class=Response
)
def get_image(id: int, session: Session = Depends(get_session)):
    image = session.exec(select(Image).where(Image.id == id)).first()
    if image is None:
        raise HTTPException(404, 'Not found')
    return Response(content=image.data, media_type=image.content_type)