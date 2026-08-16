"""Backend استخراج متن PDF با pypdf."""

from __future__ import annotations

from pathlib import Path
from typing import Any


class PyPDFBackend:
    """استخراج متن از PDFهای دارای لایه متنی."""

    name = "pypdf"

    def _reader(self, source: Path) -> Any:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("کتابخانه pypdf نصب نشده است.") from exc
        return PdfReader(str(source))

    def extract_text(self, source: str) -> str:
        reader = self._reader(Path(source))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages).strip()

    def inspect(self, source: str) -> dict[str, Any]:
        reader = self._reader(Path(source))
        text_pages = sum(bool((page.extract_text() or "").strip()) for page in reader.pages)
        pages = len(reader.pages)
        return {
            "صفحات": pages,
            "صفحات دارای متن": text_pages,
            "صفحات اسکن‌شده": pages - text_pages,
            "نیازمند OCR": text_pages < pages,
        }
