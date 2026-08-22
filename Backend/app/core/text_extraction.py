from pathlib import Path

from pypdf import PdfReader
from docx import Document


def extract_text_from_file(file_path: str) -> str:
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext == ".pdf":
        return _extract_pdf(path)
    elif ext == ".docx":
        return _extract_docx(path)
    else:
        raise ValueError(f"Unsupported file type for extraction: {ext}")


def _extract_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    # No embedded text = likely a scanned PDF. Real OCR fallback (e.g. pytesseract)
    # goes here later — flag it for now instead of silently returning empty text.
    if not text.strip():
        raise ValueError("No extractable text found — file may be a scanned image (OCR not yet implemented)")
    return text


def _extract_docx(path: Path) -> str:
    doc = Document(str(path))
    return "\n".join(p.text for p in doc.paragraphs)