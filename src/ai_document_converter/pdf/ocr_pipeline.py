"""Pipeline تبدیل PDF به متن با مسیر مستقیم و OCR."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class PageRenderer(Protocol):
    """قرارداد تبدیل یک صفحه PDF به تصویر."""

    def render(self, source: Path, page_number: int) -> Path: ...


class PDFOCRPipeline:
    """استخراج متن و استفاده از OCR برای صفحات بدون لایه متنی."""

    def __init__(self, pdf_backend, ocr_service, renderer: PageRenderer) -> None:
        self.pdf_backend = pdf_backend
        self.ocr_service = ocr_service
        self.renderer = renderer

    def convert(self, source: Path, language: str = "fas+eng") -> str:
        inspection = self.pdf_backend.inspect(str(source))
        direct_text = self.pdf_backend.extract_text(str(source))
        if not inspection.get("نیازمند OCR", False):
            return direct_text

        pages = int(inspection.get("صفحات", 0))
        results: list[str] = []
        for page_number in range(pages):
            image = self.renderer.render(source, page_number)
            result = self.ocr_service.recognize(image, language=language)
            results.append(result.text)
        return "\n\n".join(part for part in results if part).strip()
