"""تولید زیرنویس استاندارد SRT از قطعات زمان‌بندی‌شده."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SubtitleSegment:
    start: float
    end: float
    text: str


def _timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    seconds_value, millis = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds_value:02d},{millis:03d}"


def write_srt(segments: list[SubtitleSegment], target: Path) -> Path:
    lines: list[str] = []
    for index, segment in enumerate(segments, 1):
        lines.extend([str(index), f"{_timestamp(segment.start)} --> {_timestamp(segment.end)}", segment.text, ""])
    target.write_text("\n".join(lines), encoding="utf-8")
    return target
