"""قرارداد موتور تشخیص دست‌خط."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class HandwritingEngine(Protocol):
    """قرارداد موتورهای تشخیص دست‌خط قابل تعویض."""

    name: str

    def recognize(self, image: Path, language: str = "fas") -> str:
        """متن دست‌نویس تصویر را استخراج کن."""
        ...


class UnavailableHandwritingEngine:
    """Fallback امن تا زمانی که موتور تخصصی روی سیستم فعال شود."""

    name = "unavailable"

    def recognize(self, image: Path, language: str = "fas") -> str:
        raise RuntimeError(
            "موتور تخصصی تشخیص دست‌خط فعال نیست. یک Backend دست‌خط مناسب باید نصب و انتخاب شود."
        )
