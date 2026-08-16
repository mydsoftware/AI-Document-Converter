"""مسیر PDF → OCR/استخراج → تحلیل AI → DOCX."""

from __future__ import annotations

from pathlib import Path

from ai_document_converter.ai.protocol import DocumentAIAnalyzer
from ai_document_converter.output import DOCXWriter
from ai_document_converter.pdf import PDFEngine
from ai_document_converter.pdf.ocr_pipeline import PDFOCRPipeline


class AIPDFToDOCXConverter:
    """تبدیل PDF با تحلیل ساختاری قابل تعویض."""

    def __init__(
        self,
        pdf_engine: PDFEngine,
        ocr_pipeline: PDFOCRPipeline,
        ai_analyzer: DocumentAIAnalyzer,
        writer: DOCXWriter,
    ) -> None:
        self.pdf_engine = pdf_engine
        self.ocr_pipeline = ocr_pipeline
        self.ai_analyzer = ai_analyzer
        self.writer = writer

    def convert(self, source: Path, target: Path, language: str = "fas+eng") -> Path:
        inspection = self.pdf_engine.inspect(source)
        text = (
            self.ocr_pipeline.convert(source, language=language)
            if inspection.get("نیازمند OCR", False)
            else self.pdf_engine.extract(source)
        )
        model = self.ai_analyzer.analyze(text, language=language.split("+")[0])
        return self.writer.write_model(model, target)
