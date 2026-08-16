"""ساخت هسته و ثبت ماژول‌های داخلی."""

from __future__ import annotations

from .registry import ModuleRegistry
from ..modules.basic_copy import BasicCopyModule


def create_registry() -> ModuleRegistry:
    """ثبت ماژول‌های داخلی و آماده‌سازی رجیستری."""
    registry = ModuleRegistry()
    registry.register(BasicCopyModule())
    return registry
