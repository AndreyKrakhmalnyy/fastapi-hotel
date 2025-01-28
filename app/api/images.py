import shutil
from app.config import settings
from fastapi import APIRouter, UploadFile, status
from app.tasks.tasks import resize_image

router = APIRouter(prefix="/images", tags=["Изображения"])


@router.post("", status_code=status.HTTP_200_OK)
def upload_image(file: UploadFile):
    image_path = f"{settings.APP_STATIC_FOLDER}{file.filename}"
    with open(image_path, "wb+") as new_file:
        shutil.copyfileobj(file.file, new_file)
    resize_image.delay(image_path)
    return {"message": "Изображения успешно обработаны и сохранены"}
