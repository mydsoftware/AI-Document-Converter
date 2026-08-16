"""Backend هوش مصنوعی محلی با Ollama و بدون نیاز به API Key."""

from __future__ import annotations

import json
from urllib import request

from ai_document_converter.document.model import BlockType, DocumentBlock, DocumentModel


class OllamaAnalyzer:
    """تحلیل ساختار سند با مدل محلی Ollama."""

    name = "ollama"

    def __init__(self, model: str = "qwen2.5:7b", endpoint: str = "http://127.0.0.1:11434") -> None:
        self.model = model
        self.endpoint = endpoint.rstrip("/")

    def analyze(self, text: str, language: str = "fas") -> DocumentModel:
        prompt = (
            "متن زیر را برای بازسازی سند تحلیل کن. فقط JSON با کلید blocks برگردان. "
            "هر block شامل type و text باشد. type یکی از title, paragraph, list, table, image باشد.\n"
            f"زبان: {language}\nمتن:\n{text}"
        )
        payload = json.dumps({"model": self.model, "prompt": prompt, "stream": False}).encode("utf-8")
        req = request.Request(
            f"{self.endpoint}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=180) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise RuntimeError(
                "اتصال به Ollama برقرار نشد. ابتدا Ollama را نصب و مدل انتخابی را دریافت کنید."
            ) from exc

        content = data.get("response", "").strip()
        try:
            parsed = json.loads(content)
            blocks = [
                DocumentBlock(type=BlockType(item.get("type", "paragraph")), text=item.get("text", ""))
                for item in parsed.get("blocks", [])
            ]
        except (TypeError, ValueError, json.JSONDecodeError, KeyError) as exc:
            raise RuntimeError("مدل محلی پاسخ JSON معتبر تولید نکرد.") from exc

        return DocumentModel(
            blocks=blocks,
            language=language,
            direction="rtl" if language.startswith("fas") else "ltr",
        )
