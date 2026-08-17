# ساخت نسخه گرافیکی ویندوز
$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
python -m pip install -e .
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --name AI-Document-Converter-GUI --windowed src/ai_document_converter/gui/app.py
Write-Host "ساخت نسخه گرافیکی تمام شد: dist/AI-Document-Converter-GUI"
