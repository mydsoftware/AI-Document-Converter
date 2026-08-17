"""تنظیمات فارسی رابط کاربری و موتورهای هوش مصنوعی."""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class AppSettings:
    language: str = "fa"
    output_format: str = "docx"
    output_directory: str = ""
    ai_mode: str = "خودکار"
    ocr_mode: str = "خودکار"
    handwriting_mode: str = "خودکار"
    transcription_mode: str = "خودکار"
    keep_intermediate: bool = False


class SettingsStore:
    """ذخیره تنظیمات در پوشه کاربر، بدون نیاز به حساب یا API."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or (Path.home() / ".ai-document-converter" / "settings.json")

    def load(self) -> AppSettings:
        if not self.path.exists():
            return AppSettings()
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return AppSettings(**{key: value for key, value in data.items() if key in AppSettings.__dataclass_fields__})
        except (OSError, ValueError, TypeError):
            return AppSettings()

    def save(self, settings: AppSettings) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(asdict(settings), ensure_ascii=False, indent=2), encoding="utf-8")
