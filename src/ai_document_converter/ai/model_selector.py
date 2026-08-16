"""انتخاب خودکار مدل محلی بر اساس سخت‌افزار."""

from __future__ import annotations

from dataclasses import dataclass

from ai_document_converter.system.hardware import HardwareProfile


@dataclass(frozen=True)
class ModelRecommendation:
    """پیشنهاد مدل و سطح اجرای آن."""

    model: str
    level: str
    reason: str


class AIModelSelector:
    """مدل را بر اساس منابع واقعی سیستم انتخاب می‌کند."""

    def recommend(self, hardware: HardwareProfile) -> ModelRecommendation:
        ram = hardware.ram_gb
        vram = hardware.vram_gb or 0

        if vram >= 12 or ram >= 32:
            return ModelRecommendation("qwen2.5:14b", "قدرتمند", "RAM/VRAM کافی برای مدل بزرگ‌تر است.")
        if vram >= 6 or ram >= 16:
            return ModelRecommendation("qwen2.5:7b", "متوسط", "سیستم برای مدل متوسط مناسب است.")
        if ram >= 8:
            return ModelRecommendation("qwen2.5:3b", "سبک", "مدل سبک برای محدودیت حافظه انتخاب شد.")
        return ModelRecommendation("qwen2.5:1.5b", "حداقلی", "منابع سیستم محدود است؛ مدل کوچک انتخاب شد.")
