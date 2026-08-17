"""پشتیبانی اختیاری Drag & Drop در ویندوز."""

from __future__ import annotations

from pathlib import Path


def install_drop_support(widget, on_files) -> bool:
    """در صورت نصب tkinterdnd2، فایل‌های رهاشده را به رابط تحویل می‌دهد."""
    try:
        from tkinterdnd2 import DND_FILES
    except ImportError:
        return False

    def dropped(event) -> None:
        paths = widget.tk.splitlist(event.data)
        on_files([Path(item) for item in paths])

    widget.drop_target_register(DND_FILES)
    widget.dnd_bind("<<Drop>>", dropped)
    return True
