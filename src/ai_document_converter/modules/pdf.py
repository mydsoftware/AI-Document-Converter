"""ماژول تبدیل PDF در مبدل هوشمند همه‌کاره."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class PDFConverter:
    """مبدل پایه PDF با تشخیص PDF متنی و اسکن‌شده."""

    name = "pdf"
    supported_inputs = {".pdf"}
    supported_outputs = {".txt", ".md", ".docx"}

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in self.supported_inputs

    def inspect(self, path: Path) -> dict[str, Any]:
        """اطلاعات اولیه فایل را بدون اجرای OCR سنگین برمی‌گرداند."""
        if not self.can_handle(path):
            raise ValueError("فایل ورودی یک PDF نیست.")
        return {
            "نوع": "pdf",
            "مسیر": str(path),
            "وضعیت": "نیازمند تحلیل محتوا",
            "ocr": "در مرحله بعد فعال می‌شود",
        }

    def convert(self, source: Path, target: Path) -> Path:
        """نقطه ورود استاندارد ماژول؛ موتور واقعی استخراج/OCR در مراحل بعدی اضافه می‌شود."""
        if not self.can_handle(source):
            raise ValueError("فرمت ورودی پشتیبانی نمی‌شود.")
        raise NotImplementedError(
            "موتور تبدیل PDF هنوز نصب نشده است؛ این بخش باید توسط استخراج متن یا OCR اجرا شود."
        )
