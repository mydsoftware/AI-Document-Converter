"""زیرسیستم تشخیص دست‌خط."""

from .detector import WritingTypeDetector, WritingTypeResult
from .engine import HandwritingEngine, UnavailableHandwritingEngine
from .transformers import TransformersHandwritingEngine
from .router import WritingRouter

__all__ = [
    "HandwritingEngine",
    "TransformersHandwritingEngine",
    "UnavailableHandwritingEngine",
    "WritingRouter",
    "WritingTypeDetector",
    "WritingTypeResult",
]
