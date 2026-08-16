"""ترجمه زیرنویس با AI محلی."""

from __future__ import annotations

from dataclasses import replace

from .transcription import TranscriptSegment, TranscriptionResult


class LocalSubtitleTranslator:
    """ترجمه را از طریق یک تحلیل‌گر AI محلی انجام می‌دهد."""

    def __init__(self, analyzer) -> None:
        self.analyzer = analyzer

    def translate(self, result: TranscriptionResult, target_language: str = "fa") -> TranscriptionResult:
        translated: list[TranscriptSegment] = []
        for segment in result.segments:
            model = self.analyzer.analyze(segment.text, language=target_language)
            text = getattr(model, "text", None) or getattr(model, "content", None) or segment.text
            translated.append(replace(segment, text=str(text)))
        return TranscriptionResult(
            text=" ".join(item.text for item in translated),
            segments=translated,
            language=target_language,
        )
