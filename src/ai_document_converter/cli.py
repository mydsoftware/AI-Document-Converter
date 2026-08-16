"""رابط خط فرمان مبدل هوشمند."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="adc",
        description="مبدل هوشمند همه‌کاره؛ تبدیل فایل با OCR و هوش مصنوعی محلی.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    convert = sub.add_parser("convert", help="تبدیل یک فایل")
    convert.add_argument("input", type=Path, help="مسیر فایل ورودی")
    convert.add_argument("--to", required=True, choices=["docx"], help="فرمت خروجی")
    convert.add_argument("--output", type=Path, help="مسیر فایل خروجی")
    convert.add_argument("--language", default="fas+eng", help="زبان OCR")

    info = sub.add_parser("system", help="نمایش سخت‌افزار و پیشنهاد AI")
    info.add_argument("--ai", action="store_true", help="نمایش وضعیت مدل AI")
    return parser


def _build_pdf_pipeline(language: str):
    from ai_document_converter.ocr.backends import TesseractOCR
    from ai_document_converter.pdf import PDFEngine
    from ai_document_converter.pdf.backends import PyPDFBackend
    from ai_document_converter.pdf.backends.pymupdf_renderer import PyMuPDFRenderer
    from ai_document_converter.pdf.ocr_pipeline import PDFOCRPipeline

    backend = PyPDFBackend()
    engine = PDFEngine(backend=backend)
    ocr = TesseractOCR()
    pipeline = PDFOCRPipeline(engine, ocr, PyMuPDFRenderer())
    return engine, pipeline


def _convert_pdf_to_docx(source: Path, target: Path, language: str) -> None:
    from ai_document_converter.ai.auto import AutoAIAnalyzer
    from ai_document_converter.conversion.ai_pdf_to_docx import AIPDFToDOCXConverter
    from ai_document_converter.output import DOCXWriter

    engine, pipeline = _build_pdf_pipeline(language)
    converter = AIPDFToDOCXConverter(engine, pipeline, AutoAIAnalyzer(), DOCXWriter())
    converter.convert(source, target, language=language)


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "system":
        from ai_document_converter.ai.model_selector import AIModelSelector
        from ai_document_converter.system.hardware import detect_hardware

        hardware = detect_hardware()
        recommendation = AIModelSelector().recommend(hardware)
        print(f"سیستم‌عامل: {hardware.operating_system}")
        print(f"هسته پردازنده: {hardware.cpu_cores}")
        print(f"RAM: {hardware.ram_gb} GB")
        print(f"GPU: {hardware.gpu_name or 'شناسایی نشد'}")
        print(f"VRAM: {hardware.vram_gb or 0} GB")
        print(f"مدل پیشنهادی هوش مصنوعی: {recommendation.model}")
        print(f"سطح: {recommendation.level}")
        if args.ai:
            from ai_document_converter.ai.auto import AutoAIAnalyzer
            status = AutoAIAnalyzer().status()
            print(f"مدل نصب شده: {'بله' if status['نصب‌شده'] else 'خیر'}")
            if not status["نصب‌شده"]:
                print(f"دستور نصب: {status['دستور نصب']}")
        return 0

    if args.command == "convert":
        if not args.input.exists():
            print(f"خطا: فایل پیدا نشد: {args.input}")
            return 2
        if args.input.suffix.lower() != ".pdf" or args.to != "docx":
            print("در این نسخه فقط PDF به Word پیاده‌سازی شده است.")
            return 2
        target = args.output or args.input.with_suffix(".docx")
        try:
            _convert_pdf_to_docx(args.input, target, args.language)
        except Exception as exc:
            print(f"خطا در تبدیل: {exc}")
            return 1
        print(f"تبدیل با موفقیت انجام شد: {target}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
