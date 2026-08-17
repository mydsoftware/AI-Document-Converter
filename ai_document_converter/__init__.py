"""سازگاری مسیر قدیمی با بسته اصلی داخل src."""

from pathlib import Path

__version__ = "0.1.0"
_src_package = Path(__file__).resolve().parent.parent / "src" / "ai_document_converter"
if _src_package.is_dir():
    __path__.insert(0, str(_src_package))
