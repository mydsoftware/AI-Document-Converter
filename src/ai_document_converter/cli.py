"""رابط خط فرمان مبدل هوشمند."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="adc",
        description="مبدل هوشمند همه‌کاره؛ آماده توسعه برای PDF، تصویر، صوت و ویدیو.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    convert = sub.add_parser("convert", help="تبدیل یک فایل")
    convert.add_argument("input", type=Path, help="مسیر فایل ورودی")
    convert.add_argument("--to", required=True, choices=["docx", "txt", "md"], help="فرمت خروجی")
    convert.add_argument("--output", type=Path, help="مسیر فایل خروجی")
    convert.add_argument("--language", default="fas+eng", help="زبان OCR")

    info = sub.add_parser("system", help="نمایش سخت‌افزار و پیشنهاد AI")
    info.add_argument("--ai", action="store_true", help="نمایش وضعیت مدل AI")
    return parser


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
        print(f"مدل پیشنهادی AI: {recommendation.model}")
        print(f"سطح: {recommendation.level}")
        if args.ai:
            from ai_document_converter.ai.auto import AutoAIAnalyzer
            status = AutoAIAnalyzer().status()
            print(f"مدل نصب شده: {'بله' if status['نصب‌شده'] else 'خیر'}")
        return 0

    if args.command == "convert":
        if not args.input.exists():
            print(f"خطا: فایل پیدا نشد: {args.input}")
            return 2
        print("مسیر تبدیل عمومی در حال اتصال به موتورهای فرمت است.")
        print(f"ورودی: {args.input}")
        print(f"خروجی: {args.to}")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
