"""پردازش تصویر و OCR."""

from __future__ import annotations

from pathlib import Path


class ImageOCR:
    """تصویر را با موتور OCR موجود به متن تبدیل می‌کند."""

    name = "image-ocr"

    def __init__(self, ocr_engine) -> None:
        self.ocr_engine = ocr_engine

    def extract(self, source: Path, language: str = "fas+eng") -> str:
        result = self.ocr_engine.recognize(source, language=language)
        return result.text
