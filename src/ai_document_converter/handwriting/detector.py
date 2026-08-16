"""تشخیص اولیه چاپی یا دست‌نویس بودن صفحه."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WritingTypeResult:
    """نتیجه تشخیص نوع نوشته."""

    type: str
    confidence: float
    reason: str


class WritingTypeDetector:
    """لایه تشخیص نوع نوشته؛ موتورهای دقیق‌تر بعداً قابل اتصال هستند."""

    def detect(self, image: Path) -> WritingTypeResult:
        try:
            from PIL import Image
            from PIL import ImageStat

            with Image.open(image) as source:
                gray = source.convert("L")
                # این معیار فقط یک fallback است و ادعای تشخیص قطعی دست‌خط ندارد.
                stat = ImageStat.Stat(gray)
                variation = stat.stddev[0]
        except Exception:
            return WritingTypeResult("نامشخص", 0.0, "امکان تحلیل تصویر وجود نداشت.")

        if variation < 20:
            return WritingTypeResult("چاپی", 0.55, "تنوع پیکسلی پایین؛ نتیجه اولیه و غیرقطعی است.")
        return WritingTypeResult("نیازمند تحلیل دست‌خط", 0.50, "برای تصمیم قطعی باید مدل تخصصی دست‌خط بررسی کند.")
