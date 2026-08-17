"""رابط گرافیکی فارسی و سبک برای مبدل."""

from __future__ import annotations

import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from ai_document_converter.core.conversion_router import ConversionRouter
from ai_document_converter.core.executor import ConversionExecutor


class ConverterApp(tk.Tk):
    """رابط دسکتاپ فارسی با انتخاب فایل و نمایش وضعیت."""

    def __init__(self) -> None:
        super().__init__()
        self.title("مبدل هوشمند همه‌کاره")
        self.geometry("720x460")
        self.minsize(620, 400)
        self.source: Path | None = None
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="مبدل هوشمند همه‌کاره", font=("Segoe UI", 20, "bold")).pack(pady=(0, 18))
        ttk.Label(frame, text="PDF، تصویر، صوت و ویدیو را به خروجی مناسب تبدیل کنید.").pack(pady=(0, 20))

        self.file_label = ttk.Label(frame, text="هنوز فایلی انتخاب نشده است")
        self.file_label.pack(pady=8)
        ttk.Button(frame, text="انتخاب فایل", command=self.select_file).pack(pady=8)

        options = ttk.Frame(frame)
        options.pack(pady=18)
        ttk.Label(options, text="فرمت خروجی:").grid(row=0, column=0, padx=8)
        self.format_var = tk.StringVar(value="docx")
        ttk.Combobox(options, textvariable=self.format_var, values=("docx", "txt", "srt", "md"), state="readonly", width=12).grid(row=0, column=1)

        self.progress = ttk.Progressbar(frame, mode="indeterminate")
        self.progress.pack(fill="x", pady=15)
        self.status = ttk.Label(frame, text="آماده")
        self.status.pack(pady=8)
        ttk.Button(frame, text="شروع تبدیل", command=self.start).pack(pady=10)

    def select_file(self) -> None:
        selected = filedialog.askopenfilename(title="انتخاب فایل")
        if selected:
            self.source = Path(selected)
            self.file_label.config(text=str(self.source))
            self.status.config(text="فایل انتخاب شد")

    def start(self) -> None:
        if not self.source:
            messagebox.showwarning("انتخاب فایل", "ابتدا یک فایل انتخاب کنید.")
            return
        target_format = self.format_var.get()
        try:
            ConversionRouter().route(self.source, target_format)
        except Exception as exc:
            messagebox.showerror("خطا", str(exc))
            return
        target = self.source.with_suffix("." + target_format)
        self.progress.start(10)
        self.status.config(text="در حال پردازش...")
        threading.Thread(target=self._run, args=(target, target_format), daemon=True).start()

    def _run(self, target: Path, target_format: str) -> None:
        try:
            result = ConversionExecutor().execute(self.source, target, target_format)
        except Exception as exc:
            self.after(0, self._failed, str(exc))
            return
        self.after(0, self._done, result)

    def _done(self, result: Path) -> None:
        self.progress.stop()
        self.status.config(text=f"تکمیل شد: {result}")
        messagebox.showinfo("تبدیل کامل شد", f"فایل خروجی ساخته شد:\n{result}")

    def _failed(self, error: str) -> None:
        self.progress.stop()
        self.status.config(text="تبدیل ناموفق بود")
        messagebox.showerror("خطا در تبدیل", error)


def main() -> None:
    ConverterApp().mainloop()


if __name__ == "__main__":
    main()
