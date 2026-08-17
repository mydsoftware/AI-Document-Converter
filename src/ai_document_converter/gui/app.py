"""رابط گرافیکی فارسی برای مبدل همه‌کاره."""

from __future__ import annotations

import queue
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from ai_document_converter.core.conversion_router import ConversionRouter
from ai_document_converter.core.executor import ConversionExecutor
from .drop import install_drop_support
from .settings import AppSettings, SettingsStore


class ConverterApp(tk.Tk):
    """رابط دسکتاپ فارسی با صف چندفایلی، تنظیمات و Drag & Drop."""

    def __init__(self) -> None:
        super().__init__()
        self.title("مبدل هوشمند همه‌کاره")
        self.geometry("900x650")
        self.minsize(760, 540)
        self.files: list[Path] = []
        self.jobs: queue.Queue[tuple[Path, str]] = queue.Queue()
        self.running = False
        self.settings_store = SettingsStore()
        self.settings = self.settings_store.load()
        self._build()
        install_drop_support(self, self.add_paths)

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="مبدل هوشمند همه‌کاره", font=("Segoe UI", 20, "bold")).pack(pady=(0, 8))
        ttk.Label(frame, text="فایل را انتخاب یا روی پنجره رها کنید؛ موتور مناسب به‌صورت خودکار انتخاب می‌شود.").pack(pady=(0, 15))

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=8)
        ttk.Button(buttons, text="افزودن فایل", command=self.add_files).pack(side="left", padx=5)
        ttk.Button(buttons, text="پاک کردن فهرست", command=self.clear_files).pack(side="left", padx=5)
        ttk.Button(buttons, text="تنظیمات", command=self.open_settings).pack(side="right", padx=5)

        self.file_list = tk.Listbox(frame, height=12)
        self.file_list.pack(fill="both", expand=True, pady=10)

        options = ttk.Frame(frame)
        options.pack(fill="x", pady=8)
        ttk.Label(options, text="فرمت خروجی:").pack(side="left", padx=5)
        self.format_var = tk.StringVar(value=self.settings.output_format)
        ttk.Combobox(options, textvariable=self.format_var, values=("docx", "txt", "srt", "md"), state="readonly", width=12).pack(side="left")
        ttk.Label(options, text="زبان:").pack(side="left", padx=(25, 5))
        self.language_var = tk.StringVar(value=self.settings.language)
        ttk.Combobox(options, textvariable=self.language_var, values=("fa", "en", "ar"), state="readonly", width=10).pack(side="left")

        self.progress = ttk.Progressbar(frame, mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=12)
        self.status = ttk.Label(frame, text="آماده")
        self.status.pack(pady=5)
        ttk.Button(frame, text="شروع تبدیل همه فایل‌ها", command=self.start).pack(pady=8)

    def add_paths(self, paths: list[Path]) -> None:
        for path in paths:
            if path.is_file() and path not in self.files:
                self.files.append(path)
                self.file_list.insert(tk.END, str(path))
        if paths:
            self.status.config(text=f"{len(self.files)} فایل در صف قرار گرفت")

    def add_files(self) -> None:
        selected = filedialog.askopenfilenames(title="انتخاب فایل‌ها")
        self.add_paths([Path(item) for item in selected])

    def clear_files(self) -> None:
        if self.running:
            return
        self.files.clear()
        self.file_list.delete(0, tk.END)
        self.progress["value"] = 0
        self.status.config(text="فهرست پاک شد")

    def open_settings(self) -> None:
        window = tk.Toplevel(self)
        window.title("تنظیمات مبدل")
        window.geometry("430x320")
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="تنظیمات هوش مصنوعی و خروجی", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Label(frame, text="حالت AI:").pack(anchor="w")
        ai_var = tk.StringVar(value=self.settings.ai_mode)
        ttk.Combobox(frame, textvariable=ai_var, values=("خودکار", "محلی", "خاموش"), state="readonly").pack(fill="x", pady=5)
        ttk.Label(frame, text="OCR:").pack(anchor="w")
        ocr_var = tk.StringVar(value=self.settings.ocr_mode)
        ttk.Combobox(frame, textvariable=ocr_var, values=("خودکار", "محلی", "خاموش"), state="readonly").pack(fill="x", pady=5)
        ttk.Label(frame, text="دست‌خط:").pack(anchor="w")
        htr_var = tk.StringVar(value=self.settings.handwriting_mode)
        ttk.Combobox(frame, textvariable=htr_var, values=("خودکار", "محلی", "خاموش"), state="readonly").pack(fill="x", pady=5)

        def save() -> None:
            self.settings.ai_mode = ai_var.get()
            self.settings.ocr_mode = ocr_var.get()
            self.settings.handwriting_mode = htr_var.get()
            self.settings.output_format = self.format_var.get()
            self.settings.language = self.language_var.get()
            self.settings_store.save(self.settings)
            window.destroy()
            self.status.config(text="تنظیمات ذخیره شد")

        ttk.Button(frame, text="ذخیره تنظیمات", command=save).pack(pady=12)

    def start(self) -> None:
        if self.running:
            return
        if not self.files:
            messagebox.showwarning("فهرست فایل", "ابتدا حداقل یک فایل انتخاب کنید.")
            return
        target_format = self.format_var.get()
        valid: list[Path] = []
        for source in self.files:
            try:
                ConversionRouter().route(source, target_format)
                valid.append(source)
            except Exception as exc:
                self.status.config(text=f"رد شد: {source.name} — {exc}")
        if not valid:
            return
        self.jobs = queue.Queue()
        for source in valid:
            self.jobs.put((source, target_format))
        self.running = True
        self.progress["value"] = 0
        self.progress["maximum"] = len(valid)
        threading.Thread(target=self._worker, args=(self.language_var.get(),), daemon=True).start()

    def _worker(self, language: str) -> None:
        total = self.jobs.qsize()
        done = 0
        while not self.jobs.empty():
            source, target_format = self.jobs.get()
            target = source.with_suffix("." + target_format)
            try:
                ConversionExecutor().execute(source, target, target_format, language=language)
                done += 1
                self.after(0, self._progress, done, total, source.name)
            except Exception as exc:
                self.after(0, self._failed_item, source.name, str(exc))
        self.after(0, self._finished, done, total)

    def _progress(self, done: int, total: int, name: str) -> None:
        self.progress["value"] = done
        self.status.config(text=f"{done} از {total}: {name}")

    def _failed_item(self, name: str, error: str) -> None:
        self.status.config(text=f"خطا در {name}: {error}")

    def _finished(self, done: int, total: int) -> None:
        self.running = False
        self.status.config(text=f"پردازش پایان یافت: {done} از {total} موفق")
        messagebox.showinfo("پایان تبدیل", f"پردازش تمام شد.\nموفق: {done}\nکل: {total}")


def main() -> None:
    ConverterApp().mainloop()


if __name__ == "__main__":
    main()
