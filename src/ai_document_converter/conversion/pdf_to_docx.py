"""تبدیل کامل PDF به Word."""

from __future__ import annotations

from pathlib import Path

from ai_document_converter.output import DOCXWriter
from ai_document_converter.pdf import PDFEngine
from ai_document_converter.pdf.ocr_pipeline import PDFOCRPipeline


class PDFToDOCXConverter:
    """مسیر استاندارد PDF → استخراج/OCR → DOCX."""

    name = "pdf-to-docx"

    def __init__(self, pdf_engine: PDFEngine, ocr_pipeline: PDFOCRPipeline, writer: DOCXWriter) -> None:
        self.pdf_engine = pdf_engine
        self.ocr_pipeline = ocr_pipeline
        self.writer = writer

    def convert(self, source: Path, target: Path, language: str = "fas+eng") -> Path:
        inspection = self.pdf_engine.inspect(source)
        if inspection.get("نیازمند OCR", False):
            text = self.ocr_pipeline.convert(source, language=language)
        else:
            text = self.pdf_engine.extract(source)
        return self.writer.write(text, target, rtl=language.startswith("fas"))
