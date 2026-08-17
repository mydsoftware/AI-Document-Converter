# نصب خودکار ابزارهای سیستم در ویندوز
$ErrorActionPreference = "Stop"

Write-Host "=== آماده‌سازی ابزارهای سیستم مبدل ==="

if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Warning "winget در این ویندوز در دسترس نیست. نصب خودکار ابزارهای سیستم ممکن نیست."
    exit 0
}

function Install-Tool($Id, $Name) {
    if (Get-Command $Name -ErrorAction SilentlyContinue) {
        Write-Host "[OK] $Name قبلاً نصب است."
        return
    }
    Write-Host "در حال نصب $Name ..."
    winget install --id $Id --exact --accept-source-agreements --accept-package-agreements
}

Install-Tool "Gyan.FFmpeg" "ffmpeg"
Install-Tool "Ollama.Ollama" "ollama"

Write-Host "=== بررسی نهایی ==="
if (Get-Command ffmpeg -ErrorAction SilentlyContinue) { Write-Host "[OK] FFmpeg" } else { Write-Warning "FFmpeg هنوز در PATH دیده نمی‌شود؛ ممکن است نیاز به بازکردن ترمینال جدید باشد." }
if (Get-Command ollama -ErrorAction SilentlyContinue) { Write-Host "[OK] Ollama" } else { Write-Warning "Ollama هنوز در PATH دیده نمی‌شود؛ ممکن است نیاز به بازکردن ترمینال جدید باشد." }
