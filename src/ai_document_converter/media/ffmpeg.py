"""ابزارهای رسانه‌ای مبتنی بر FFmpeg."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


class FFmpegEngine:
    """اجرای امن عملیات پایه صوت و ویدیو."""

    name = "ffmpeg"

    def __init__(self, executable: str = "ffmpeg") -> None:
        self.executable = executable

    def available(self) -> bool:
        return shutil.which(self.executable) is not None

    def extract_audio(self, source: Path, target: Path) -> Path:
        if not self.available():
            raise RuntimeError("FFmpeg نصب یا در PATH سیستم پیدا نشد.")
        command = [self.executable, "-y", "-i", str(source), "-vn", "-ac", "1", "-ar", "16000", str(target)]
        subprocess.run(command, check=True, capture_output=True, text=True)
        return target
