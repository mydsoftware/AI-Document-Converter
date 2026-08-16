"""مسیر کامل ویدیو به متن و زیرنویس با پردازش محلی."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from .auto_transcription import AutoTranscriptionEngine
from .ffmpeg import FFmpegEngine
from .subtitles import SubtitleSegment, write_srt


class VideoToTextConverter:
    """صوت ویدیو را استخراج و با Whisper محلی به متن تبدیل می‌کند."""

    def __init__(self, ffmpeg: FFmpegEngine | None = None, transcription=None) -> None:
        self.ffmpeg = ffmpeg or FFmpegEngine()
        self.transcription = transcription or AutoTranscriptionEngine()

    def convert(self, source: Path, text_target: Path, srt_target: Path | None = None, language: str = "fa") -> tuple[Path, Path | None]:
        with tempfile.TemporaryDirectory(prefix="adc-") as directory:
            audio = Path(directory) / "audio.wav"
            self.ffmpeg.extract_audio(source, audio)
            text = self.transcription.transcribe(audio, language=language)
            text_target.write_text(text, encoding="utf-8")

            subtitle_target = None
            if srt_target:
                # Whisper backend فعلی متن نهایی را ارائه می‌کند؛ قطعه‌بندی زمان‌دار
                # در نسخه بعدی از خروجی segmentهای Whisper تغذیه خواهد شد.
                subtitle_target = write_srt([SubtitleSegment(0.0, 0.0, text)], srt_target)
            return text_target, subtitle_target
