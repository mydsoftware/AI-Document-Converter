from pathlib import Path

import pytest

from ai_document_converter.core.conversion_router import ConversionRouter


def test_supported_routes():
    router = ConversionRouter()
    assert router.route(Path("document.pdf"), "docx") == ("pdf", "docx")
    assert router.route(Path("photo.png"), "docx") == ("image", "docx")
    assert router.route(Path("video.mp4"), "srt") == ("video", "srt")
    assert router.route(Path("audio.mp3"), "txt") == ("audio", "txt")


def test_unsupported_route_fails():
    with pytest.raises(ValueError):
        ConversionRouter().route(Path("video.mp4"), "docx")
