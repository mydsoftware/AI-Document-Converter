"""موتور تشخیص دست‌خط مبتنی بر مدل‌های Transformer محلی."""

from __future__ import annotations

from pathlib import Path


class TransformersHandwritingEngine:
    """اجرای مدل‌های سازگار با TrOCR از روی فایل محلی یا مخزن مدل.

    نام مدل عمداً قابل تنظیم است تا برای هر زبان، از جمله فارسی،
    مدل تخصصی تأییدشده بدون تغییر هسته پروژه انتخاب شود.
    """

    name = "transformers-handwriting"

    def __init__(self, model_name: str = "microsoft/trocr-base-handwritten", device: str = "auto") -> None:
        self.model_name = model_name
        self.device = device
        self._processor = None
        self._model = None

    def _load(self):
        try:
            from transformers import TrOCRProcessor, VisionEncoderDecoderModel
        except ImportError as exc:
            raise RuntimeError(
                "برای موتور Transformer باید بسته‌های transformers و torch نصب شوند."
            ) from exc

        self._processor = TrOCRProcessor.from_pretrained(self.model_name)
        self._model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
        if self.device == "auto":
            try:
                import torch
                self.device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                self.device = "cpu"
        self._model.to(self.device)
        self._model.eval()

    def recognize(self, image: Path, language: str = "fas") -> str:
        if self._model is None:
            self._load()

        from PIL import Image
        image_data = Image.open(image).convert("RGB")
        pixel_values = self._processor(images=image_data, return_tensors="pt").pixel_values
        pixel_values = pixel_values.to(self.device)
        generated_ids = self._model.generate(pixel_values, max_new_tokens=256)
        return self._processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
