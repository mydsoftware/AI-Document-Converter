"""آزمون انتخاب خودکار مدل هوش مصنوعی."""

from ai_document_converter.ai.model_selector import AIModelSelector
from ai_document_converter.system.hardware import HardwareProfile


def profile(ram, vram=None):
    return HardwareProfile("test", 8, ram, "GPU" if vram else None, vram, 20)


def test_selects_large_model_for_powerful_system():
    result = AIModelSelector().recommend(profile(32, 12))
    assert result.model == "qwen2.5:14b"


def test_selects_medium_model_for_mid_range_system():
    result = AIModelSelector().recommend(profile(16, 6))
    assert result.model == "qwen2.5:7b"


def test_selects_light_model_for_low_memory_system():
    result = AIModelSelector().recommend(profile(8))
    assert result.model == "qwen2.5:3b"
