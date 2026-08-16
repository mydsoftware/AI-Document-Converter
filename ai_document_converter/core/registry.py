"""ثبت و کشف ماژول‌های قابل استفاده."""

from __future__ import annotations

from .contracts import ConverterModule


class ModuleRegistry:
    """ثبت‌کننده مرکزی ماژول‌ها؛ هسته به پیاده‌سازی آنها وابسته نیست."""

    def __init__(self) -> None:
        self._modules: dict[str, ConverterModule] = {}

    def register(self, module: ConverterModule) -> None:
        if module.name in self._modules:
            raise ValueError(f"ماژول تکراری است: {module.name}")
        self._modules[module.name] = module

    def get(self, name: str) -> ConverterModule:
        try:
            return self._modules[name]
        except KeyError as exc:
            raise KeyError(f"ماژول پیدا نشد: {name}") from exc

    def all(self) -> tuple[ConverterModule, ...]:
        return tuple(self._modules.values())

    def find(self, file_info, target_extension: str | None = None) -> list[ConverterModule]:
        return [
            module
            for module in self._modules.values()
            if module.can_handle(file_info, target_extension)
        ]
