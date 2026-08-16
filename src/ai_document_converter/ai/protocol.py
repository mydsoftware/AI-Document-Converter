"""قرارداد مستقل تحلیل هوش مصنوعی سند."""

from __future__ import annotations

from typing import Protocol

from ai_document_converter.document.model import DocumentModel


class DocumentAIAnalyzer(Protocol):
    """هر موتور هوش مصنوعی می‌تواند این قرارداد را پیاده‌سازی کند."""

    def analyze(self, text: str, language: str = "fas") -> DocumentModel:
        """ساختار سند را تحلیل و مدل استاندارد تولید کن."""
        ...
