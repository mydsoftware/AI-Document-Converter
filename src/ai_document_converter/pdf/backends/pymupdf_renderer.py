"""رندر صفحات PDF به تصویر با PyMuPDF."""

from __future__ import annotations

from pathlib import Path
import tempfile


class PyMuPDFRenderer:
    """صفحات PDF را برای OCR به PNG تبدیل می‌کند."""

    name = "pymupdf"

    def render(self, source: Path, page_number: int) -> Path:
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError("کتابخانه PyMuPDF نصب نشده است.") from exc

        document = fitz.open(str(source))
        try:
            page = document.load_page(page_number)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
            output = Path(tempfile.mkstemp(prefix="adc-page-", suffix=".png")[1])
            pixmap.save(str(output))
            return output
        finally:
            document.close()
