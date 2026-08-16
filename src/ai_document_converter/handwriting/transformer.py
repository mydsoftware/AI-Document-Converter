"""موتور HTR مبتنی بر Transformer با بارگذاری تنبل مدل."""

from __future__ import annotations

from pathlib import Path


class TransformerHandwritingEngine:
    """یک Backend عمومی برای مدل‌های Vision-to-Text سازگار با Transformers."""

    name = "transformer-htr"

    def __init__(self, model_name: str, device: str = "auto") -> None:
        self.model_name = model_name
        self.device = device
        self._processor = None
        self._model = None

    def _load(self) -> None:
        if self._model is not None:
            return
        try:
            from transformers import AutoProcessor, VisionEncoderDecoderModel
        except ImportError as exc:
            raise RuntimeError("برای موتور دست‌خط باید بسته transformers نصب شود.") from exc
        self._processor = AutoProcessor.from_pretrained(self.model_name)
        self._model = VisionEncoderDecoderModel.from_pretrained(self.model_name)
        if self.device != "auto":
            import torch
            self._model.to(self.device)

    def recognize(self, image: Path, language: str = "fas") -> str:
        self._load()
        try:
            from PIL import Image
            import torch
            picture = Image.open(image).convert("RGB")
            inputs = self._processor(images=picture, return_tensors="pt")
            device = next(self._model.parameters()).device
            pixel_values = inputs.pixel_values.to(device)
            with torch.no_grad():
                generated = self._model.generate(pixel_values)
            return self._processor.batch_decode(generated, skip_special_tokens=True)[0].strip()
        except Exception as exc:
            raise RuntimeError(f"تشخیص دست‌خط با مدل {self.model_name} انجام نشد: {exc}") from exc
