"""خط لوله کامل ویدیو به متن و زیرنویس."""

from __future__ import annotations

from pathlib import Path
import tempfile

from .auto_transcription import AutoTranscriptionEngine
from .ffmpeg import FFmpegEngine
from .subtitles import from_transcription, write_srt


class VideoTranscriptionPipeline:
    """ویدیو را با FFmpeg و Whisper محلی به متن و SRT تبدیل می‌کند."""

    def __init__(self, ffmpeg: FFmpegEngine | None = None, transcription=None) -> None:
        self.ffmpeg = ffmpeg or FFmpegEngine()
        self.transcription = transcription or AutoTranscriptionEngine()

    def run(self, source: Path, text_target: Path, srt_target: Path, language: str = "fa") -> tuple[Path, Path]:
        with tempfile.TemporaryDirectory(prefix="adc-") as directory:
            audio = Path(directory) / "audio.wav"
            self.ffmpeg.extract_audio(source, audio)
            result = self.transcription.engine.transcribe(audio, language=language)
            text_target.write_text(result.text, encoding="utf-8")
            write_srt(from_transcription(result), srt_target)
        return text_target, srt_target
