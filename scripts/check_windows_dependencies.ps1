# بررسی وابستگی‌های محلی ویندوز
$ErrorActionPreference = "Continue"

Write-Host "=== بررسی وابستگی‌ها ==="

$tools = @("python", "ffmpeg", "ollama")
foreach ($tool in $tools) {
    if (Get-Command $tool -ErrorAction SilentlyContinue) {
        Write-Host "[OK] $tool"
    } else {
        Write-Host "[نیازمند نصب] $tool"
    }
}

if (Test-Path ".venv\Scripts\python.exe") {
    & .\.venv\Scripts\python.exe -m ai_document_converter.cli system --ai
} else {
    Write-Host "محیط Python پروژه هنوز ساخته نشده است."
}
