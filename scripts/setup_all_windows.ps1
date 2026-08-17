# نصب یک‌مرحله‌ای مبدل هوشمند همه‌کاره در ویندوز
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "=== راه‌اندازی مبدل هوشمند همه‌کاره ==="

& "$Root\scripts\install_windows.ps1"
& "$Root\scripts\install_windows_tools.ps1"

if (Get-Command ollama -ErrorAction SilentlyContinue) {
    $model = "llama3.2:3b"
    $answer = Read-Host "مدل AI محلی $model نصب شود؟ (Y/N)"
    if ($answer -match '^[Yy]$') {
        & "$Root\scripts\install_ai_model.ps1" -Model $model
    }
}

$python = "$Root\.venv\Scripts\python.exe"
$gui = "$Root\src\ai_document_converter\gui\app.py"

if (Test-Path $python) {
    $shortcutScript = Join-Path $env:TEMP "adc-shortcut.ps1"
    @"
`$shell = New-Object -ComObject WScript.Shell
`$desktop = [Environment]::GetFolderPath('Desktop')
`$shortcut = `$shell.CreateShortcut((Join-Path `$desktop 'مبدل هوشمند.lnk'))
`$shortcut.TargetPath = '$python'
`$shortcut.Arguments = '"$gui"'
`$shortcut.WorkingDirectory = '$Root'
`$shortcut.Description = 'مبدل هوشمند همه‌کاره'
`$shortcut.Save()
"@ | Set-Content -Encoding UTF8 $shortcutScript
    powershell -ExecutionPolicy Bypass -File $shortcutScript
    Remove-Item $shortcutScript -Force
}

Write-Host ""
Write-Host "=== راه‌اندازی تمام شد ==="
Write-Host "برای اجرای GUI از میانبر «مبدل هوشمند» روی دسکتاپ استفاده کنید."
