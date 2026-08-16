"""آزمون Backend استخراج متن PDF."""

from pathlib import Path

import pytest

from ai_document_converter.pdf.backends import PyPDFBackend


def test_backend_requires_pdf() -> None:
    backend = PyPDFBackend()
    with pytest.raises((ValueError, FileNotFoundError)):
        backend.extract_text("نمونه.txt")


def test_backend_isolates_dependency(tmp_path: Path) -> None:
    """وجود فایل نامعتبر نباید باعث اجرای بی‌قیدوشرط موتور شود."""
    source = tmp_path / "نمونه.pdf"
    source.write_bytes(b"not a real pdf")
    backend = PyPDFBackend()
    with pytest.raises(Exception):
        backend.extract_text(str(source))
