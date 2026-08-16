"""Backendهای هوش مصنوعی."""

from .ollama import OllamaAnalyzer
from .openai_compatible import OpenAICompatibleAnalyzer

__all__ = ["OllamaAnalyzer", "OpenAICompatibleAnalyzer"]
