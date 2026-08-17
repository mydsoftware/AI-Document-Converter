"""مدیریت مدل‌های محلی و Ollama بدون API اجباری."""

from __future__ import annotations

import json
from pathlib import Path
from urllib import request

from ai_document_converter.ai.model_selector import ModelRecommendation


class OllamaModelManager:
    """بررسی و مدیریت مدل‌های نصب‌شده در Ollama."""

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
        return f"ollama pull {recommendation.model}"

    def status(self, recommendation: ModelRecommendation) -> dict[str, object]:
        try:
            installed = self.installed_models()
            return {"در دسترس": True, "مدل پیشنهادی": recommendation.model, "نصب‌شده": recommendation.model in installed, "مدل‌ها": installed, "دستور نصب": self.installation_command(recommendation)}
        except RuntimeError:
            return {"در دسترس": False, "مدل پیشنهادی": recommendation.model, "نصب‌شده": False, "مدل‌ها": [], "دستور نصب": self.installation_command(recommendation)}


class LocalModelCache:
    """کش عمومی مدل‌های محلی در پوشه کاربر."""

    def __init__(self, root: Path | None = None) -> None:
        self.root = root or (Path.home() / ".ai-document-converter" / "models")
        self.root.mkdir(parents=True, exist_ok=True)

    def path(self, name: str) -> Path:
        return self.root / name

    def exists(self, name: str) -> bool:
        return self.path(name).exists()
