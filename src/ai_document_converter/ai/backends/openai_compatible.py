"""Backend عمومی برای APIهای سازگار با OpenAI."""

from __future__ import annotations

import json
import os
from urllib import request

from ai_document_converter.document.model import BlockType, DocumentBlock, DocumentModel


class OpenAICompatibleAnalyzer:
    """تحلیل سند با API سازگار با OpenAI، بدون وابستگی به SDK خاص."""

    name = "openai-compatible"

    def __init__(self, endpoint: str, model: str, api_key: str | None = None) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.api_key = api_key or os.getenv("AI_API_KEY")
        if not self.api_key:
            raise RuntimeError("کلید API تنظیم نشده است. متغیر AI_API_KEY را تنظیم کنید.")

    def analyze(self, text: str, language: str = "fas") -> DocumentModel:
        prompt = (
            "متن سند را به JSON ساختاری تبدیل کن. فقط JSON برگردان. "
            "هر بلوک دارای type و text باشد. type فقط title, paragraph, list, table, image باشد.\n\n"
            f"زبان: {language}\nمتن:\n{text}"
        )
        payload = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }).encode("utf-8")
        req = request.Request(
            f"{self.endpoint}/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=120) as response:
                data = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise RuntimeError(f"خطا در ارتباط با سرویس هوش مصنوعی: {exc}") from exc

        content = data["choices"][0]["message"]["content"]
        try:
            parsed = json.loads(content)
            blocks = [
                DocumentBlock(type=BlockType(item.get("type", "paragraph")), text=item.get("text", ""))
                for item in parsed.get("blocks", [])
            ]
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            raise RuntimeError("پاسخ مدل هوش مصنوعی JSON معتبر نیست.") from exc
        return DocumentModel(blocks=blocks, language=language, direction="rtl" if language == "fas" else "ltr")
