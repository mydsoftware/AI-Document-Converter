"""تشخیص نوع فایل ورودی برای مسیریابی ماژولار."""

from __future__ import annotations

from pathlib import Path

from dataclasses import dataclass


@dataclass(frozen=True)
class InputKind:
    """نوع منطقی ورودی."""
    name: str
    category: str


_EXTENSIONS = {
    ".pdf": InputKind("PDF", "document"),
    ".docx": InputKind("Word", "document"),
    ".doc": InputKind("Word قدیمی", "document"),
    ".txt": InputKind("متن", "document"),
    ".md": InputKind("Markdown", "document"),
    ".jpg": InputKind("تصویر", "image"),
    ".jpeg": InputKind("تصویر", "image"),
    ".png": InputKind("تصویر", "image"),
    ".bmp": InputKind("تصویر", "image"),
    ".webp": InputKind("تصویر", "image"),
    ".mp3": InputKind("صوت", "audio"),
    ".wav": InputKind("صوت", "audio"),
    ".m4a": InputKind("صوت", "audio"),
    ".mp4": InputKind("ویدیو", "video"),
    ".mkv": InputKind("ویدیو", "video"),
    ".avi": InputKind("ویدیو", "video"),
    ".mov": InputKind("ویدیو", "video"),
    ".webm": InputKind("ویدیو", "video"),
}


def detect_input(path: Path) -> InputKind:
    """نوع فایل را بر اساس پسوند تشخیص می‌دهد."""
    suffix = path.suffix.lower()
    if suffix not in _EXTENSIONS:
        raise ValueError(f"فرمت فایل پشتیبانی‌شده نیست: {suffix or 'بدون پسوند'}")
    return _EXTENSIONS[suffix]
