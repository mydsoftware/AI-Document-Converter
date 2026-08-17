# نصب خودکار محیط ویندوز
$ErrorActionPreference = "Stop"

Write-Host "=== نصب مبدل هوشمند همه‌کاره ==="

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python پیدا نشد. ابتدا Python 3.12 یا جدیدتر را نصب کنید."
}

python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".[dev]"

if (Get-Command ffmpeg -ErrorAction SilentlyContinue) {
    Write-Host "FFmpeg از قبل نصب است."
} else {
    Write-Warning "FFmpeg نصب نیست. برای پردازش صوت و ویدیو باید FFmpeg را نصب کنید."
}

if (Get-Command ollama -ErrorAction SilentlyContinue) {
    Write-Host "Ollama شناسایی شد."
} else {
    Write-Warning "Ollama نصب نیست. قابلیت‌های AI محلی بدون API به Ollama نیاز دارند."
}

Write-Host "نصب پایه تمام شد."
Write-Host "برای بررسی سیستم: .\.venv\Scripts\python.exe -m ai_document_converter.cli system --ai"
