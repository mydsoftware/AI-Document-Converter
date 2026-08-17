param(
    [string]$Model = "llama3.2:3b"
)

$ErrorActionPreference = "Stop"

if (-not (Get-Command ollama -ErrorAction SilentlyContinue)) {
    Write-Error "Ollama نصب نیست. ابتدا scripts/install_windows_tools.ps1 را اجرا کنید."
}

Write-Host "در حال آماده‌سازی مدل محلی: $Model"
ollama pull $Model
Write-Host "مدل محلی آماده شد: $Model"
