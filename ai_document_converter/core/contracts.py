"""قراردادهای عمومی ماژول‌ها."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar

from .models import ConversionContext, ConversionResult, FileInfo


class ConverterModule(ABC):
    """قرارداد هر ماژول تبدیل یا پردازش."""

    name: ClassVar[str]
    description: ClassVar[str]
    input_extensions: ClassVar[frozenset[str]] = frozenset()
    output_extensions: ClassVar[frozenset[str]] = frozenset()

    @classmethod
    @abstractmethod
    def can_handle(cls, file_info: FileInfo, target_extension: str | None = None) -> bool:
        """بررسی می‌کند آیا ماژول می‌تواند فایل را پردازش کند."""

    @abstractmethod
    def convert(
        self,
        source: Path,
        destination: Path,
        context: ConversionContext,
    ) -> ConversionResult:
        """فایل را پردازش کرده و نتیجه استاندارد برمی‌گرداند."""


class AIProvider(ABC):
    """قرارداد عمومی برای مدل‌های هوش مصنوعی."""

    name: ClassVar[str]

    @abstractmethod
    def analyze(self, content: str, **options: object) -> str:
        """تحلیل یا اصلاح متن."""


class OCRProvider(ABC):
    """قرارداد عمومی برای موتورهای OCR و دست‌خط."""

    name: ClassVar[str]

    @abstractmethod
    def extract_text(self, image: Path, **options: object) -> str:
        """استخراج متن از تصویر."""
