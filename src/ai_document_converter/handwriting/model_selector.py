"""انتخاب مدل تشخیص دست‌خط بر اساس سخت‌افزار کاربر."""

from __future__ import annotations

from dataclasses import dataclass

from ai_document_converter.system.hardware import HardwareProfile


@dataclass(frozen=True)
class HandwritingModelRecommendation:
    """پیشنهاد مدل دست‌خط."""

    model: str
    level: str
    reason: str


class HandwritingModelSelector:
    """مدل را بدون وابستگی به یک سخت‌افزار خاص انتخاب می‌کند."""

    def recommend(self, hardware: HardwareProfile) -> HandwritingModelRecommendation:
        vram = hardware.vram_gb or 0
        ram = hardware.ram_gb
        if vram >= 8 or ram >= 24:
            return HandwritingModelRecommendation(
                "microsoft/trocr-large-handwritten", "قدرتمند", "منابع کافی برای مدل بزرگ تشخیص دست‌خط وجود دارد."
            )
        if vram >= 4 or ram >= 16:
            return HandwritingModelRecommendation(
                "microsoft/trocr-base-handwritten", "متوسط", "مدل پایه برای سیستم متوسط انتخاب شد."
            )
        return HandwritingModelRecommendation(
            "microsoft/trocr-small-handwritten", "سبک", "برای کاهش مصرف حافظه مدل سبک انتخاب شد."
        )
