"""استخراج متن از PDF و تشخیص نیاز به OCR."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PDFInspection:
    """نتیجه تحلیل اولیه PDF."""

    pages: int
    text_pages: int
    scanned_pages: int
    requires_ocr: bool


class PDFTextExtractor:
    """لایه مستقل استخراج متن که موتور PDF را از هسته جدا نگه می‌دارد."""

    def inspect(self, source: Path) -> PDFInspection:
        """PDF را بررسی می‌کند؛ وابستگی سنگین استخراج در این لایه تزریق می‌شود."""
        if source.suffix.lower() != ".pdf":
            raise ValueError("فایل ورودی PDF نیست.")
        if not source.exists():
            raise FileNotFoundError(f"فایل پیدا نشد: {source}")
        # پیاده‌سازی موتور واقعی PDF در گام بعدی متصل می‌شود.
        return PDFInspection(
            pages=0,
            text_pages=0,
            scanned_pages=0,
            requires_ocr=True,
        )

    def extract_text(self, source: Path) -> str:
        """متن PDF را استخراج می‌کند یا در صورت نیاز مسیر OCR را اعلام می‌کند."""
        inspection = self.inspect(source)
        if inspection.requires_ocr:
            raise RuntimeError("این PDF نیازمند موتور OCR است که در مرحله بعد متصل می‌شود.")
        return ""
