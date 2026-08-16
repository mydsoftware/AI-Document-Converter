"""حالت خودکار انتخاب موتور و مدل هوش مصنوعی."""

from __future__ import annotations

from ai_document_converter.ai.model_selector import AIModelSelector
from ai_document_converter.ai.backends.ollama import OllamaAnalyzer
from ai_document_converter.system.hardware import detect_hardware


class AutoAIAnalyzer:
    """بدون نیاز به دخالت کاربر، مدل مناسب سیستم را انتخاب می‌کند."""

    def __init__(self) -> None:
        self.hardware = detect_hardware()
        self.recommendation = AIModelSelector().recommend(self.hardware)
        self.backend = OllamaAnalyzer(model=self.recommendation.model)

    def analyze(self, text: str, language: str = "fas"):
        return self.backend.analyze(text, language=language)
