"""زیرساخت ماژولار تبدیل صوت و ویدیو به متن."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol


class TranscriptionEngine(Protocol):
    """قرارداد موتورهای گفتار به متن."""

    name: str

    def transcribe(self, audio: Path, language: str = "fa") -> str: ...


class WhisperTranscriptionEngine:
    """موتور محلی Whisper با بارگذاری تنبل مدل."""

    name = "whisper"

    def __init__(self, model_name: str = "small", device: str = "auto") -> None:
        self.model_name = model_name
        self.device = device
        self._model = None

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            import whisper
        except ImportError as exc:
            raise RuntimeError("برای گفتار به متن باید بسته openai-whisper نصب شود.") from exc
        self._model = whisper.load_model(self.model_name, device=None if self.device == "auto" else self.device)

    def transcribe(self, audio: Path, language: str = "fa") -> str:
        self._load()
        try:
            result = self._model.transcribe(str(audio), language=language, fp16=False)
            return str(result.get("text", "")).strip()
        except Exception as exc:
            raise RuntimeError(f"تبدیل گفتار به متن انجام نشد: {exc}") from exc
