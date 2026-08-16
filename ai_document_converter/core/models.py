"""مدل‌های پایه و بدون وابستگی به موتورهای خارجی."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FileInfo:
    """اطلاعات استاندارد یک فایل ورودی."""

    path: Path
    mime_type: str | None = None
    extension: str = ""


@dataclass
class ConversionContext:
    """وضعیت مشترک در طول اجرای یک Pipeline."""

    metadata: dict[str, Any] = field(default_factory=dict)
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class ConversionResult:
    """نتیجه استاندارد یک عملیات تبدیل."""

    output: Path
    module: str
    metadata: dict[str, Any] = field(default_factory=dict)
