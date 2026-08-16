from pathlib import Path

import pytest

from ai_document_converter.document.model import BlockType, DocumentBlock, DocumentModel
from ai_document_converter.output import DOCXWriter


def test_docx_writer_creates_valid_file(tmp_path: Path):
    pytest.importorskip("docx")
    target = tmp_path / "خروجی.docx"
    model = DocumentModel(
        blocks=[
            DocumentBlock(BlockType.TITLE, "عنوان آزمایشی"),
            DocumentBlock(BlockType.PARAGRAPH, "این یک متن آزمایشی فارسی است."),
            DocumentBlock(BlockType.LIST, "گزینه اول"),
        ],
        language="fas",
        direction="rtl",
    )
    result = DOCXWriter().write_model(model, target)
    assert result.exists()
    assert result.stat().st_size > 0
