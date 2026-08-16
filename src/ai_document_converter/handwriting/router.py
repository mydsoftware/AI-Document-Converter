"""انتخاب خودکار OCR چاپی یا موتور دست‌خط."""

from __future__ import annotations

from pathlib import Path

from .detector import WritingTypeDetector
from .engine import HandwritingEngine


class WritingRouter:
    """بر اساس تشخیص اولیه، موتور مناسب را انتخاب می‌کند."""

    def __init__(self, handwriting_engine: HandwritingEngine) -> None:
        self.detector = WritingTypeDetector()
        self.handwriting_engine = handwriting_engine

    def recognize(self, image: Path, printed_ocr, language: str = "fas+eng") -> str:
        result = self.detector.detect(image)
        if result.type == "نیازمند تحلیل دست‌خط":
            return self.handwriting_engine.recognize(image, language=language.split("+")[0])
        return printed_ocr.recognize(image, language=language).text
