"""انتخاب و راه‌اندازی خودکار موتور HTR."""

from __future__ import annotations

from ai_document_converter.handwriting.model_selector import HandwritingModelSelector
from ai_document_converter.handwriting.transformer import TransformerHandwritingEngine
from ai_document_converter.system.hardware import detect_hardware


class AutoHandwritingEngine:
    """مدل دست‌خط مناسب سیستم را انتخاب می‌کند و موتور را تنبل بارگذاری می‌کند."""

    def __init__(self) -> None:
        self.hardware = detect_hardware()
        self.recommendation = HandwritingModelSelector().recommend(self.hardware)
        self.engine = TransformerHandwritingEngine(self.recommendation.model)

    def recognize(self, image, language: str = "fas") -> str:
        return self.engine.recognize(image, language=language)
