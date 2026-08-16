"""اجرای زنجیره‌ای عملیات تبدیل."""

from __future__ import annotations

from pathlib import Path

from .contracts import ConverterModule
from .models import ConversionContext, ConversionResult


class Pipeline:
    """یک زنجیره از ماژول‌ها را به ترتیب اجرا می‌کند."""

    def __init__(self, modules: list[ConverterModule]) -> None:
        self.modules = modules

    def run(
        self,
        source: Path,
        destination: Path,
        context: ConversionContext | None = None,
    ) -> ConversionResult:
        if not self.modules:
            raise ValueError("Pipeline حداقل باید یک ماژول داشته باشد")

        context = context or ConversionContext()
        current = source
        result: ConversionResult | None = None

        for index, module in enumerate(self.modules):
            target = destination if index == len(self.modules) - 1 else destination.parent / (
                f".pipeline_{index}_{source.name}"
            )
            result = module.convert(current, target, context)
            current = result.output

        assert result is not None
        return result
