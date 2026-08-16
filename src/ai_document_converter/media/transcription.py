"""زیرساخت ماژولار تبدیل صوت و ویدیو به متن و زیرنویس."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class TranscriptSegment:
    """یک قطعه گفتار همراه با زمان شروع و پایان."""

    start: float
    end: float
    text: str


@dataclass(frozen=True)
class TranscriptionResult:
    """خروجی کامل گفتار به متن."""

    text: str
    segments: list[TranscriptSegment]
    language: str


class TranscriptionEngine(Protocol):
    """قرارداد موتورهای گفتار به متن."""

    name: str

    def transcribe(self, audio: Path, language: str = "fa") -> TranscriptionResult: ...


class WhisperTranscriptionEngine:
    """موتور محلی Whisper با بارگذاری تنبل مدل و زمان‌بندی واقعی."""

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

    def transcribe(self, audio: Path, language: str = "fa") -> TranscriptionResult:
        self._load()
        try:
            result = self._model.transcribe(str(audio), language=language, fp16=False)
            segments = [
                TranscriptSegment(float(item["start"]), float(item["end"]), str(item["text"]).strip())
                for item in result.get("segments", [])
                if str(item.get("text", "")).strip()
            ]
            return TranscriptionResult(
                text=str(result.get("text", "")).strip(),
                segments=segments,
                language=str(result.get("language", language)),
            )
        except Exception as exc:
            raise RuntimeError(f"تبدیل گفتار به متن انجام نشد: {exc}") from exc
