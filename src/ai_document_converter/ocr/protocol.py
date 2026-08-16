"""قرارداد مستقل برای اتصال موتورهای OCR مختلف."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class OCRResult:
    """خروجی استاندارد OCR."""

    text: str
    language: str | None = None
    handwritten: bool = False
    confidence: float | None = None


class OCRService(Protocol):
    """هر موتور OCR باید این قرارداد را پیاده‌سازی کند."""

    def recognize(self, image: Path, language: str | None = None) -> OCRResult:
        """متن تصویر را تشخیص بده."""
        ...
