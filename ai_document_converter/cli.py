"""رابط خط فرمان ویندوز."""

from __future__ import annotations

import argparse
from pathlib import Path

from .core.bootstrap import create_registry
from .core.detector import detect_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="adc",
        description="مبدل هوشمند همه‌کاره و ماژولار",
    )
    sub = parser.add_subparsers(dest="command")

    info = sub.add_parser("اطلاعات", help="نمایش اطلاعات فایل")
    info.add_argument("file", type=Path)

    modules = sub.add_parser("ماژول‌ها", help="نمایش ماژول‌های فعال")
    modules.set_defaults(show_modules=True)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if getattr(args, "show_modules", False):
        for module in create_registry().all():
            print(f"- {module.name}: {module.description}")
        return 0

    if args.command == "اطلاعات":
        info = detect_file(args.file)
        print(f"فایل: {info.path}")
        print(f"پسوند: {info.extension or 'ندارد'}")
        print(f"نوع MIME: {info.mime_type or 'نامشخص'}")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
