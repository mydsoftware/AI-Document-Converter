# ساخت بسته اجرایی ویندوز
$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --name AI-Document-Converter --console src/ai_document_converter/cli.py
Write-Host "ساخت نسخه ویندوز تمام شد: dist/AI-Document-Converter"
