"""تبدیل تصویر به Word با OCR و تحلیل هوش مصنوعی."""

from __future__ import annotations

from pathlib import Path

from ai_document_converter.ai.protocol import DocumentAIAnalyzer
from ai_document_converter.image.ocr import ImageOCR
from ai_document_converter.output import DOCXWriter


class ImageToDOCXConverter:
    """تصویر اسکن‌شده را به سند Word ساختاریافته تبدیل می‌کند."""

    def __init__(self, image_ocr: ImageOCR, ai_analyzer: DocumentAIAnalyzer, writer: DOCXWriter) -> None:
        self.image_ocr = image_ocr
        self.ai_analyzer = ai_analyzer
        self.writer = writer

    def convert(self, source: Path, target: Path, language: str = "fas+eng") -> Path:
        text = self.image_ocr.extract(source, language=language)
        model = self.ai_analyzer.analyze(text, language=language.split("+")[0])
        return self.writer.write_model(model, target)
