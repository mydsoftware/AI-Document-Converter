"""تشخیص اولیه نوع فایل بدون وابستگی به ماژول‌های تبدیل."""

from __future__ import annotations

import mimetypes
from pathlib import Path

from .models import FileInfo


def detect_file(path: Path) -> FileInfo:
    """اطلاعات فایل را با استفاده از پسوند و MIME حدسی تولید می‌کند."""
    extension = path.suffix.lower()
    mime_type, _ = mimetypes.guess_type(path.name)
    return FileInfo(path=path, mime_type=mime_type, extension=extension)
