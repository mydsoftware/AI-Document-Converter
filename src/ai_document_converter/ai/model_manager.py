"""مدیریت مدل محلی انتخاب‌شده توسط سیستم."""

from __future__ import annotations

import json
from urllib import request

from ai_document_converter.ai.model_selector import ModelRecommendation


class OllamaModelManager:
    """بررسی نصب بودن مدل و فراهم‌کردن اطلاعات لازم برای اجرای آن."""

    def __init__(self, endpoint: str = "http://127.0.0.1:11434") -> None:
        self.endpoint = endpoint.rstrip("/")

    def installed_models(self) -> list[str]:
        req = request.Request(f"{self.endpoint}/api/tags", method="GET")
        try:
            with request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise RuntimeError("Ollama در دسترس نیست.") from exc
        return [item.get("name", "") for item in data.get("models", [])]

    def is_installed(self, recommendation: ModelRecommendation) -> bool:
        return recommendation.model in self.installed_models()

    def installation_command(self, recommendation: ModelRecommendation) -> str:
        """دستور نصب مدل را برای CLI برمی‌گرداند؛ اجرای خودکار بعداً سیاست‌گذاری می‌شود."""
        return f"ollama pull {recommendation.model}"
