"""Backend عمومی دست‌خط مبتنی بر مدل‌های Transformers."""

from __future__ import annotations

from pathlib import Path


class TransformersHandwritingEngine:
    """یک مدل تصویر-به-متن را به قرارداد HandwritingEngine متصل می‌کند.

    نام مدل از بیرون تزریق می‌شود تا انتخاب مدل بر اساس سیستم کاربر انجام شود.
    """

    name = "transformers"

    def __init__(self, model_name: str, device: str = "auto") -> None:
        self.model_name = model_name
        self.device = device
        self._processor = None
        self._model = None

    def _load(self):
        if self._processor is not None:
            return
        try:
            from transformers import AutoProcessor, AutoModelForVision2Seq
        except ImportError as exc:
            raise RuntimeError(
                "کتابخانه Transformers نصب نیست؛ Backend دست‌خط نمی‌تواند اجرا شود."
            ) from exc

        self._processor = AutoProcessor.from_pretrained(self.model_name)
        self._model = AutoModelForVision2Seq.from_pretrained(self.model_name)
        if self.device != "auto":
            self._model.to(self.device)

    def recognize(self, image: Path, language: str = "fas") -> str:
        self._load()
        try:
            from PIL import Image
        except ImportError as exc:
            raise RuntimeError("کتابخانه Pillow نصب نیست.") from exc

        picture = Image.open(image).convert("RGB")
        inputs = self._processor(images=picture, text="", return_tensors="pt")
        generated = self._model.generate(**inputs, max_new_tokens=1024)
        return self._processor.batch_decode(generated, skip_special_tokens=True)[0].strip()
