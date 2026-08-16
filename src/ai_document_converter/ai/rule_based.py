"""تحلیل‌گر محلی بدون نیاز به API خارجی."""

from __future__ import annotations

from ai_document_converter.document.analyzer import DocumentStructureAnalyzer
from ai_document_converter.document.model import DocumentModel


class LocalDocumentAnalyzer:
    """تحلیل‌گر پیش‌فرض برای کارکرد آفلاین و تست."""

    name = "local"

    def __init__(self) -> None:
        self._analyzer = DocumentStructureAnalyzer()

    def analyze(self, text: str, language: str = "fas") -> DocumentModel:
        return self._analyzer.analyze(text, language=language)
