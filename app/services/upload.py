import uuid
import shutil
from pathlib import Path
from fastapi import UploadFile, File, HTTPException

# Директория для загрузки файлов
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)  # Создаем, если нет


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}  # Разрешенные форматы
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB

class UploadService:
    @staticmethod
    def upload_image(file: UploadFile = File(...)):
        """Загружает изображение и возвращает URL"""

        # Проверка формата
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Неверный формат файла")

        # Проверка размера
        file.file.seek(0, 2)  # Перемещаемся в конец файла
        file_size = file.file.tell()
        file.file.seek(0)  # Возвращаемся в начало
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="Файл слишком большой (макс. 2MB)")

        # Генерируем уникальное имя файла
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename

        # Сохраняем файл
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"url": f"/static/uploads/{unique_filename}"}
