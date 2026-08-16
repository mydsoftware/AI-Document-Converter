"""تحلیل ساختار متن قبل از تولید خروجی."""

from __future__ import annotations

import re

from .model import BlockType, DocumentBlock, DocumentModel


class DocumentStructureAnalyzer:
    """تحلیل‌گر پایه؛ در آینده مدل AI می‌تواند این قرارداد را ارتقا دهد."""

    def analyze(self, text: str, language: str = "fas") -> DocumentModel:
        blocks: list[DocumentBlock] = []
        for raw in re.split(r"\n\s*\n", text):
            value = raw.strip()
            if not value:
                continue
            if len(value) < 100 and (value.endswith(":") or value.isupper()):
                kind = BlockType.TITLE
            elif re.match(r"^(?:[-*•]|\d+[.)])\s+", value):
                kind = BlockType.LIST
            else:
                kind = BlockType.PARAGRAPH
            blocks.append(DocumentBlock(type=kind, text=value))
        return DocumentModel(blocks=blocks, language=language, direction="rtl" if language.startswith("fas") else "ltr")
