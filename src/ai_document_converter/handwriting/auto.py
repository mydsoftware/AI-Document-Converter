"""انتخاب و راه‌اندازی خودکار موتور HTR."""

from __future__ import annotations

from ai_document_converter.handwriting.model_selector import HandwritingModelSelector
from ai_document_converter.handwriting.transformer import TransformerHandwritingEngine
from ai_document_converter.system.hardware import detect_hardware


class AutoHandwritingEngine:
    """مدل دست‌خط مناسب سیستم را انتخاب می‌کند و موتور را تنبل بارگذاری می‌کند."""

    name = "auto-htr"

    def __init__(self, model_name: str | None = None) -> None:
        self.hardware = detect_hardware()
        self.recommendation = HandwritingModelSelector().recommend(self.hardware)
        self.model_name = model_name or self.recommendation.model
        self.engine = TransformerHandwritingEngine(self.model_name)

    def recognize(self, image, language: str = "fas") -> str:
        return self.engine.recognize(image, language=language)

    def status(self) -> dict[str, object]:
        return {
            "مدل پیشنهادی": self.model_name,
            "سطح": self.recommendation.level,
            "دلیل": self.recommendation.reason,
            "سخت‌افزار": {
                "RAM": self.hardware.ram_gb,
                "GPU": self.hardware.gpu_name,
                "VRAM": self.hardware.vram_gb,
            },
        }
