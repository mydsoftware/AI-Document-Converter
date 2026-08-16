from pathlib import Path

from ai_document_converter.core.bootstrap import create_registry
from ai_document_converter.core.detector import detect_file
from ai_document_converter.core.models import ConversionContext


def test_detector():
    info = detect_file(Path("document.pdf"))
    assert info.extension == ".pdf"
    assert info.mime_type == "application/pdf"


def test_registry_contains_basic_module():
    registry = create_registry()
    assert registry.get("basic-copy").name == "basic-copy"


def test_basic_module_copies_file(tmp_path):
    source = tmp_path / "ورودی.txt"
    destination = tmp_path / "خروجی.txt"
    source.write_text("سلام جهان", encoding="utf-8")

    module = create_registry().get("basic-copy")
    result = module.convert(source, destination, ConversionContext())

    assert result.output == destination
    assert destination.read_text(encoding="utf-8") == "سلام جهان"
