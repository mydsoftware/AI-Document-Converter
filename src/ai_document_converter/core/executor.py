"""اجرای واقعی مسیرهای تبدیل فعال."""

from __future__ import annotations

from pathlib import Path


class ConversionExecutor:
    """مسیریاب را به موتورهای واقعی تبدیل متصل می‌کند."""

    def execute(self, source: Path, target: Path, target_format: str, language: str = "fa") -> Path:
        target_format = target_format.lower().lstrip(".")
        suffix = source.suffix.lower()

        if suffix == ".pdf" and target_format == "docx":
            from ai_document_converter.ai.auto import AutoAIAnalyzer
            from ai_document_converter.conversion.ai_pdf_to_docx import AIPDFToDOCXConverter
            from ai_document_converter.output import DOCXWriter
            from ai_document_converter.ocr.backends import TesseractOCR
            from ai_document_converter.pdf import PDFEngine
            from ai_document_converter.pdf.backends import PyPDFBackend
            from ai_document_converter.pdf.backends.pymupdf_renderer import PyMuPDFRenderer
            from ai_document_converter.pdf.ocr_pipeline import PDFOCRPipeline

            engine = PDFEngine(backend=PyPDFBackend())
            pipeline = PDFOCRPipeline(engine, TesseractOCR(), PyMuPDFRenderer())
            return AIPDFToDOCXConverter(engine, pipeline, AutoAIAnalyzer(), DOCXWriter()).convert(source, target, language=language)

        if suffix in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"} and target_format == "docx":
            from ai_document_converter.ai.auto import AutoAIAnalyzer
            from ai_document_converter.conversion.smart_image_to_docx import SmartImageToDOCXConverter
            from ai_document_converter.ocr.backends import TesseractOCR
            from ai_document_converter.output import DOCXWriter

            return SmartImageToDOCXConverter(TesseractOCR(), AutoAIAnalyzer(), DOCXWriter()).convert(source, target, language=language)

        if suffix in {".mp4", ".mkv", ".mov", ".avi", ".webm"} and target_format in {"txt", "srt"}:
            from ai_document_converter.media.video_pipeline import VideoTranscriptionPipeline
            text_target = target if target_format == "txt" else target.with_suffix(".txt")
            srt_target = target if target_format == "srt" else target.with_suffix(".srt")
            VideoTranscriptionPipeline().run(source, text_target, srt_target, language=language)
            return target

        if suffix in {".mp3", ".wav", ".m4a", ".flac", ".ogg"} and target_format == "txt":
            from ai_document_converter.media.auto_transcription import AutoTranscriptionEngine
            result = AutoTranscriptionEngine().engine.transcribe(source, language=language)
            target.write_text(result.text, encoding="utf-8")
            return target

        raise ValueError(f"مسیر اجرایی برای {suffix} به {target_format} هنوز فعال نشده است.")
