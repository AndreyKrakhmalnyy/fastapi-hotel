import shutil
from fastapi import APIRouter, UploadFile, status


router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("", status_code=status.HTTP_200_OK)
async def upload_image(file: UploadFile):
    with open(
        f"app/static/images/{file.filename}", "wb+"
    ) as new_image:
        shutil.copyfileobj(file.file, new_image)
        return True
