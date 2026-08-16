"""تبدیل هوشمند تصویر به Word با انتخاب خودکار OCR چاپی/دست‌خط."""

from __future__ import annotations

from pathlib import Path

from ai_document_converter.ai.protocol import DocumentAIAnalyzer
from ai_document_converter.handwriting.auto import AutoHandwritingEngine
from ai_document_converter.handwriting.router import WritingRouter
from ai_document_converter.output import DOCXWriter


class SmartImageToDOCXConverter:
    """یک تصویر را تحلیل کرده و مناسب‌ترین مسیر OCR را انتخاب می‌کند."""

    def __init__(self, printed_ocr, ai_analyzer: DocumentAIAnalyzer, writer: DOCXWriter) -> None:
        self.router = WritingRouter(AutoHandwritingEngine())
        self.printed_ocr = printed_ocr
        self.ai_analyzer = ai_analyzer
        self.writer = writer

    def convert(self, source: Path, target: Path, language: str = "fas+eng") -> Path:
        text = self.router.recognize(source, self.printed_ocr, language=language)
        model = self.ai_analyzer.analyze(text, language=language.split("+")[0])
        return self.writer.write_model(model, target)
