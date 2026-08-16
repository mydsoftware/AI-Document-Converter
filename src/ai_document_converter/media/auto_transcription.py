"""گفتار به متن خودکار و محلی."""

from pathlib import Path

from ai_document_converter.system.hardware import detect_hardware

from .model_selector import TranscriptionModelSelector
from .transcription import WhisperTranscriptionEngine


class AutoTranscriptionEngine:
    """به‌صورت خودکار مدل Whisper متناسب با سیستم را انتخاب می‌کند."""

    def __init__(self, model_name: str | None = None) -> None:
        hardware = detect_hardware()
        self.recommendation = TranscriptionModelSelector().recommend(hardware)
        self.model_name = model_name or self.recommendation.model
        self.engine = WhisperTranscriptionEngine(self.model_name)

    def transcribe(self, audio: Path, language: str = "fa") -> str:
        return self.engine.transcribe(audio, language=language)

    def status(self) -> dict[str, object]:
        return {
            "مدل": self.model_name,
            "سطح": self.recommendation.level,
            "دلیل": self.recommendation.reason,
        }
