"""حالت خودکار انتخاب موتور و مدل هوش مصنوعی."""

from __future__ import annotations

from ai_document_converter.ai.backends.ollama import OllamaAnalyzer
from ai_document_converter.ai.model_manager import OllamaModelManager
from ai_document_converter.ai.model_selector import AIModelSelector
from ai_document_converter.system.hardware import detect_hardware


class AutoAIAnalyzer:
    """بدون انتخاب دستی مدل، گزینه مناسب سیستم را تعیین می‌کند."""

    def __init__(self) -> None:
        self.hardware = detect_hardware()
        self.recommendation = AIModelSelector().recommend(self.hardware)
        self.model_manager = OllamaModelManager()
        self.backend = OllamaAnalyzer(model=self.recommendation.model)

    def status(self) -> dict[str, object]:
        try:
            installed = self.model_manager.installed_models()
            available = self.recommendation.model in installed
        except RuntimeError:
            installed = []
            available = False
        return {
            "مدل پیشنهادی": self.recommendation.model,
            "سطح": self.recommendation.level,
            "نصب‌شده": available,
            "مدل‌های نصب‌شده": installed,
            "دستور نصب": self.model_manager.installation_command(self.recommendation),
        }

    def analyze(self, text: str, language: str = "fas"):
        if not self.model_manager.is_installed(self.recommendation):
            raise RuntimeError(
                f"مدل پیشنهادی نصب نیست: {self.recommendation.model}. "
                f"دستور نصب: {self.model_manager.installation_command(self.recommendation)}"
            )
        return self.backend.analyze(text, language=language)
