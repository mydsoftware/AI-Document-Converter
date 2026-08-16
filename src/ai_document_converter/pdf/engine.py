"""موتور مستقل PDF برای استخراج متن و تشخیص سند اسکن‌شده."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class PDFEngine:
    """رابط موتور PDF؛ پیاده‌سازی کتابخانه‌ای از هسته جدا است."""

    def __init__(self, backend: Any | None = None) -> None:
        self.backend = backend

    def extract(self, source: Path) -> str:
        """استخراج متن با موتور تزریق‌شده."""
        if not source.exists():
            raise FileNotFoundError(f"فایل پیدا نشد: {source}")
        if source.suffix.lower() != ".pdf":
            raise ValueError("فایل ورودی PDF نیست.")
        if self.backend is None:
            raise RuntimeError("موتور PDF نصب یا متصل نشده است.")
        return self.backend.extract_text(str(source))

    def inspect(self, source: Path) -> dict[str, Any]:
        """تحلیل اولیه PDF را از backend دریافت می‌کند."""
        if self.backend is None:
            return {"صفحات": 0, "متن": False, "نیازمند OCR": True}
        return self.backend.inspect(str(source))
