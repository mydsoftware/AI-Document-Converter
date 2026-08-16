"""پردازش هوشمند چندصفحه‌ای PDF با تشخیص چاپی/دست‌خط در هر صفحه."""

from __future__ import annotations

from pathlib import Path

from ai_document_converter.handwriting.auto import AutoHandwritingEngine
from ai_document_converter.handwriting.router import WritingRouter


class SmartPDFOCRPipeline:
    """هر صفحه PDF را مستقل بررسی و موتور OCR مناسب را انتخاب می‌کند."""

    def __init__(self, pdf_backend, printed_ocr, renderer, handwriting_engine=None) -> None:
        self.pdf_backend = pdf_backend
        self.printed_ocr = printed_ocr
        self.renderer = renderer
        self.handwriting_engine = handwriting_engine or AutoHandwritingEngine()
        self.router = WritingRouter(self.handwriting_engine)

    def convert(self, source: Path, language: str = "fas+eng") -> str:
        inspection = self.pdf_backend.inspect(str(source))
        direct_text = self.pdf_backend.extract_text(str(source))
        if not inspection.get("نیازمند OCR", False):
            return direct_text

        pages = int(inspection.get("صفحات", 0))
        results: list[str] = []
        for page_number in range(pages):
            image = self.renderer.render(source, page_number)
            text = self.router.recognize(image, self.printed_ocr, language=language)
            if text:
                results.append(text)
        return "\n\n".join(results).strip()
