from ai_document_converter.ai.model_selector import AIModelSelector
from ai_document_converter.system.hardware import HardwareProfile


def profile(ram, vram=None):
    return HardwareProfile("test", 8, ram, "GPU" if vram else None, vram, 50)


def test_selects_large_model_for_powerful_system():
    assert AIModelSelector().recommend(profile(32)).model == "qwen2.5:14b"


def test_selects_medium_model_for_mid_range_system():
    assert AIModelSelector().recommend(profile(16)).model == "qwen2.5:7b"


def test_selects_light_model_for_low_memory_system():
    assert AIModelSelector().recommend(profile(8)).model == "qwen2.5:3b"


def test_selects_minimal_model_for_very_low_memory_system():
    assert AIModelSelector().recommend(profile(4)).model == "qwen2.5:1.5b"
