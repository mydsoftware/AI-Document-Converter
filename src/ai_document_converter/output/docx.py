"""خروجی Word قابل ویرایش."""

from __future__ import annotations

from pathlib import Path


class DOCXWriter:
    """متن استخراج‌شده را به DOCX تبدیل می‌کند."""

    name = "docx"

    def write(self, text: str, target: Path, rtl: bool = True) -> Path:
        try:
            from docx import Document
            from docx.enum.text import WD_ALIGN_PARAGRAPH
        except ImportError as exc:
            raise RuntimeError("کتابخانه python-docx نصب نشده است.") from exc

        document = Document()
        for block in text.split("\n\n"):
            if not block.strip():
                continue
            paragraph = document.add_paragraph(block.strip())
            if rtl:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                paragraph.paragraph_format.left_indent = None
        document.save(str(target))
        return target
