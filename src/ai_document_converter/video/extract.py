"""استخراج فریم و صدا از ویدیو برای Pipelineهای تبدیل."""

from __future__ import annotations

from pathlib import Path
import subprocess


class VideoExtractor:
    """لایه FFmpeg برای استخراج فریم‌ها و صدا؛ تحلیل AI در ماژول‌های بالاتر انجام می‌شود."""

    name = "ffmpeg"

    def __init__(self, ffmpeg: str = "ffmpeg") -> None:
        self.ffmpeg = ffmpeg

    def extract_audio(self, source: Path, target: Path) -> Path:
        self._run([self.ffmpeg, "-y", "-i", str(source), "-vn", "-acodec", "pcm_s16le", str(target)])
        return target

    def extract_frame(self, source: Path, target: Path, timestamp: float = 0.0) -> Path:
        self._run([self.ffmpeg, "-y", "-ss", str(timestamp), "-i", str(source), "-frames:v", "1", str(target)])
        return target

    def _run(self, command: list[str]) -> None:
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except FileNotFoundError as exc:
            raise RuntimeError("FFmpeg نصب یا در PATH سیستم ثبت نشده است.") from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(f"FFmpeg خطا داد: {exc.stderr[-1000:]}") from exc
