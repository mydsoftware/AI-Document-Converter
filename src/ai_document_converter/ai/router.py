"""مسیریاب Backendهای هوش مصنوعی."""

from __future__ import annotations

from typing import Any


class AIBackendRouter:
    """یک Backend را بر اساس تنظیمات یا قابلیت درخواستی انتخاب می‌کند."""

    def __init__(self) -> None:
        self._backends: dict[str, Any] = {}

    def register(self, name: str, backend: Any) -> None:
        if not name.strip():
            raise ValueError("نام Backend نمی‌تواند خالی باشد.")
        self._backends[name] = backend

    def get(self, name: str) -> Any:
        try:
            return self._backends[name]
        except KeyError as exc:
            available = ", ".join(sorted(self._backends)) or "هیچ‌کدام"
            raise LookupError(f"Backend هوش مصنوعی پیدا نشد: {name}. موجود: {available}") from exc

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._backends))
