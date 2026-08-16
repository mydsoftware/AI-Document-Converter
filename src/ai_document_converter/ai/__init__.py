"""زیرسیستم هوش مصنوعی."""

from .protocol import DocumentAIAnalyzer
from .router import AIBackendRouter
from .rule_based import LocalDocumentAnalyzer

__all__ = ["AIBackendRouter", "DocumentAIAnalyzer", "LocalDocumentAnalyzer"]
