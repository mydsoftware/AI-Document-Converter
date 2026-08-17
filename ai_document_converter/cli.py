"""رابط خط فرمان فارسی مبدل همه‌کاره."""

from __future__ import annotations

import argparse
from pathlib import Path

from .core.conversion_router import ConversionRouter
from .core.executor import ConversionExecutor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="adc", description="مبدل هوشمند همه‌کاره با OCR و هوش مصنوعی محلی")
    sub = parser.add_subparsers(dest="command", required=True)
    convert = sub.add_parser("convert", help="تبدیل فایل")
    convert.add_argument("input", type=Path, help="مسیر فایل ورودی")
    convert.add_argument("--to", required=True, dest="target_format", help="فرمت خروجی")
    convert.add_argument("--output", type=Path, help="مسیر فایل خروجی")
    convert.add_argument("--language", default="fa", help="زبان پردازش")
    info = sub.add_parser("system", help="نمایش سخت‌افزار و پیشنهاد AI")
    info.add_argument("--ai", action="store_true", help="نمایش وضعیت AI")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
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
        print(f"مدل پیشنهادی: {recommendation.model}")
        if args.ai:
            from ai_document_converter.ai.auto import AutoAIAnalyzer
            status = AutoAIAnalyzer().status()
            print(f"مدل نصب‌شده: {'بله' if status['نصب‌شده'] else 'خیر'}")
            if not status['نصب‌شده']:
                print(f"دستور نصب: {status['دستور نصب']}")
        return 0

    if args.command == "convert":
        if not args.input.exists():
            print(f"خطا: فایل پیدا نشد: {args.input}")
            return 2
        try:
            target_format = args.target_format.lower().lstrip('.')
            ConversionRouter().route(args.input, target_format)
            target = args.output or args.input.with_suffix('.' + target_format)
            target.parent.mkdir(parents=True, exist_ok=True)
            result = ConversionExecutor().execute(args.input, target, target_format, language=args.language)
            print(f"تبدیل با موفقیت انجام شد: {result}")
            return 0
        except Exception as exc:
            print(f"خطا در تبدیل: {exc}")
            return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
