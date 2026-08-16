"""Backend اختیاری OCR با Tesseract."""

from __future__ import annotations

from pathlib import Path

from ai_document_converter.ocr.protocol import OCRResult


class TesseractOCR:
    """اتصال OCR به Tesseract؛ موتور مستقل و قابل تعویض."""

    name = "tesseract"

    def recognize(self, image: Path, language: str | None = None) -> OCRResult:
        try:
            import pytesseract
        except ImportError as exc:
            raise RuntimeError("کتابخانه pytesseract نصب نشده است.") from exc

        lang = language or "fas+eng"
        text = pytesseract.image_to_string(str(image), lang=lang).strip()
        return OCRResult(text=text, language=language or "fas+eng", handwritten=False)
