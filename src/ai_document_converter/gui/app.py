"""رابط گرافیکی فارسی برای مبدل همه‌کاره."""

from __future__ import annotations

import queue
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from ai_document_converter.core.conversion_router import ConversionRouter
from ai_document_converter.core.executor import ConversionExecutor


class ConverterApp(tk.Tk):
    """رابط دسکتاپ فارسی با صف چندفایلی و پردازش پس‌زمینه."""

    def __init__(self) -> None:
        super().__init__()
        self.title("مبدل هوشمند همه‌کاره")
        self.geometry("860x600")
        self.minsize(720, 500)
        self.files: list[Path] = []
        self.jobs: queue.Queue[tuple[Path, str]] = queue.Queue()
        self.running = False
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self, padding=24)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="مبدل هوشمند همه‌کاره", font=("Segoe UI", 20, "bold")).pack(pady=(0, 8))
        ttk.Label(frame, text="چند فایل را انتخاب کنید و هرکدام را به فرمت مناسب تبدیل کنید.").pack(pady=(0, 15))

        buttons = ttk.Frame(frame)
        buttons.pack(fill="x", pady=8)
        ttk.Button(buttons, text="افزودن فایل", command=self.add_files).pack(side="left", padx=5)
        ttk.Button(buttons, text="پاک کردن فهرست", command=self.clear_files).pack(side="left", padx=5)

        self.file_list = tk.Listbox(frame, height=12)
        self.file_list.pack(fill="both", expand=True, pady=10)

        options = ttk.Frame(frame)
        options.pack(fill="x", pady=8)
        ttk.Label(options, text="فرمت خروجی:").pack(side="left", padx=5)
        self.format_var = tk.StringVar(value="docx")
        ttk.Combobox(options, textvariable=self.format_var, values=("docx", "txt", "srt", "md"), state="readonly", width=12).pack(side="left")

        self.progress = ttk.Progressbar(frame, mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=12)
        self.status = ttk.Label(frame, text="آماده")
        self.status.pack(pady=5)
        ttk.Button(frame, text="شروع تبدیل همه فایل‌ها", command=self.start).pack(pady=8)

    def add_files(self) -> None:
        selected = filedialog.askopenfilenames(title="انتخاب فایل‌ها")
        for item in selected:
            path = Path(item)
            if path not in self.files:
                self.files.append(path)
                self.file_list.insert(tk.END, str(path))
        if selected:
            self.status.config(text=f"{len(self.files)} فایل در صف قرار گرفت")

    def clear_files(self) -> None:
        if self.running:
            return
        self.files.clear()
        self.file_list.delete(0, tk.END)
        self.progress["value"] = 0
        self.status.config(text="فهرست پاک شد")

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
                messagebox.showwarning("فایل رد شد", f"{source.name}: {exc}")
        if not valid:
            return
        self.jobs = queue.Queue()
        for source in valid:
            self.jobs.put((source, target_format))
        self.running = True
        self.progress["value"] = 0
        self.progress["maximum"] = len(valid)
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self) -> None:
        total = self.jobs.qsize()
        done = 0
        while not self.jobs.empty():
            source, target_format = self.jobs.get()
            target = source.with_suffix("." + target_format)
            try:
                ConversionExecutor().execute(source, target, target_format)
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
