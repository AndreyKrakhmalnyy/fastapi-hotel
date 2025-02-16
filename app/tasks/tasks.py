import asyncio
import os
from PIL import Image
from app.config import settings
from app.tasks.celery import celery_instance
from app.utils.db_manager import DBManager
from app.database import async_session_maker_null_pool


@celery_instance.task
def resize_image(image_path: str):
    sizes = [1000, 500, 200]
    output_folder = settings.APP_STATIC_FOLDER
    # Открываем изображение
    img = Image.open(image_path)
    # Получаем имя файла и его расширение
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    # Проходим по каждому размеру
    for size in sizes:
        # Сжимаем изображение
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))),
            Image.Resampling.LANCZOS,
        )
        # Формируем имя нового файла
        new_file_name = f"{name}_{size}px{ext}"
        # Полный путь для сохранения
        output_path = os.path.join(output_folder, new_file_name)
        # Сохраняем изображение
        img_resized.save(output_path)
    print(
        f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}"
    )


async def get_bookings_today_db():
    print("START")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_today_bookings()
        print(f"{bookings}=")


@celery_instance.task(name="booking_today_alert")
def send_emails_to_users():
    asyncio.run(get_bookings_today_db())
