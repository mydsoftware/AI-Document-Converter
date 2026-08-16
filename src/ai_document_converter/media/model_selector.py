"""انتخاب مدل گفتار به متن بر اساس سخت‌افزار."""

from dataclasses import dataclass

from ai_document_converter.system.hardware import HardwareProfile


@dataclass(frozen=True)
class TranscriptionModelRecommendation:
    model: str
    level: str
    reason: str


class TranscriptionModelSelector:
    """مدل Whisper مناسب را بدون API انتخاب می‌کند."""

    def recommend(self, hardware: HardwareProfile) -> TranscriptionModelRecommendation:
        vram = hardware.vram_gb or 0
        ram = hardware.ram_gb
        if vram >= 8 or ram >= 32:
            return TranscriptionModelRecommendation("large-v3", "قدرتمند", "منابع کافی برای مدل دقیق‌تر وجود دارد.")
        if vram >= 4 or ram >= 16:
            return TranscriptionModelRecommendation("medium", "متوسط", "تعادل مناسب بین سرعت و دقت.")
        if ram >= 8:
            return TranscriptionModelRecommendation("small", "سبک", "مصرف حافظه پایین‌تر برای سیستم متوسط.")
        return TranscriptionModelRecommendation("tiny", "حداقلی", "سیستم منابع محدودی دارد.")
