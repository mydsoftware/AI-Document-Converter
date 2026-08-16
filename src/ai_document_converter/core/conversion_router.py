"""مسیریاب مرکزی تبدیل فایل."""

from __future__ import annotations

from pathlib import Path

from .detector import InputDetector


class ConversionRouter:
    """فرمت ورودی را تشخیص داده و مسیر تبدیل مربوطه را انتخاب می‌کند."""

    def __init__(self) -> None:
        self.detector = InputDetector()

    def route(self, source: Path, target_format: str) -> tuple[str, str]:
        kind = self.detector.detect(source)
        supported = {
            "pdf": {"docx", "txt", "md"},
            "image": {"docx", "txt", "md"},
            "audio": {"txt", "srt", "md"},
            "video": {"txt", "srt", "md"},
            "document": {"pdf", "txt", "md"},
            "text": {"pdf", "docx", "md"},
        }
        if target_format not in supported.get(kind, set()):
            raise ValueError(f"تبدیل {kind} به {target_format} در این نسخه فعال نیست.")
        return kind, target_format
