"""مدل ساختاری سند برای بازسازی حرفه‌ای خروجی."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class BlockType(StrEnum):
    """انواع بلوک قابل تشخیص در سند."""

    TITLE = "عنوان"
    PARAGRAPH = "پاراگراف"
    LIST = "فهرست"
    TABLE = "جدول"
    IMAGE = "تصویر"
    UNKNOWN = "ناشناخته"


@dataclass
class DocumentBlock:
    """یک بخش ساختاری از سند."""

    type: BlockType
    text: str = ""
    level: int = 0
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass
class DocumentModel:
    """نمایش مستقل از فرمت برای انتقال بین OCR، AI و خروجی‌ها."""

    blocks: list[DocumentBlock] = field(default_factory=list)
    language: str | None = None
    direction: str = "rtl"
