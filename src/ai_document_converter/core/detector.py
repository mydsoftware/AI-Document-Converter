"""تشخیص خودکار نوع فایل ورودی و مسیر تبدیل."""

from __future__ import annotations

from pathlib import Path


class InputDetector:
    """فرمت ورودی را بدون وابستگی به نام فایل تشخیص می‌دهد."""

    EXTENSIONS = {
        ".pdf": "pdf", ".png": "image", ".jpg": "image", ".jpeg": "image",
        ".webp": "image", ".bmp": "image", ".tif": "image", ".tiff": "image",
        ".mp3": "audio", ".wav": "audio", ".m4a": "audio", ".flac": "audio", ".ogg": "audio",
        ".mp4": "video", ".mkv": "video", ".mov": "video", ".avi": "video", ".webm": "video",
        ".docx": "document", ".doc": "document", ".txt": "text", ".md": "text",
    }

    def detect(self, source: Path) -> str:
        kind = self.EXTENSIONS.get(source.suffix.lower())
        if not kind:
            raise ValueError(f"فرمت فایل پشتیبانی نمی‌شود: {source.suffix or 'بدون پسوند'}")
        return kind
