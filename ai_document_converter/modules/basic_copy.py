"""ماژول پایه برای آزمایش زیرساخت؛ تبدیل واقعی فرمت انجام نمی‌دهد."""

from __future__ import annotations

import shutil
from pathlib import Path

from ..core.contracts import ConverterModule
from ..core.models import ConversionContext, ConversionResult, FileInfo


class BasicCopyModule(ConverterModule):
    """کپی امن فایل برای تست قرارداد و Pipeline."""

    name = "basic-copy"
    description = "ماژول آزمایشی کپی فایل"

    @classmethod
    def can_handle(cls, file_info: FileInfo, target_extension: str | None = None) -> bool:
        return file_info.path.is_file()

    def convert(self, source: Path, destination: Path, context: ConversionContext) -> ConversionResult:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        return ConversionResult(output=destination, module=self.name)
