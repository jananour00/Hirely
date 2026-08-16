import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile

# Stub "object storage" — local disk. Swap this module's internals for
# S3/GCS later; callers only ever see save_file() -> file_url string.
STORAGE_ROOT = Path(__file__).resolve().parents[2] / "storage" / "resumes"
STORAGE_ROOT.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE_MB = 10


def save_resume(file: UploadFile) -> str:
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {ext}")

    unique_name = f"{uuid.uuid4().hex}{ext}"
    dest = STORAGE_ROOT / unique_name

    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    size_mb = dest.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        dest.unlink()
        raise ValueError(f"File exceeds {MAX_FILE_SIZE_MB}MB limit")

    return str(dest)  # becomes an S3 URL later; nothing downstream changes