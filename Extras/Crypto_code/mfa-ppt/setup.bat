@echo off
REM Setup script for PDF to PowerPoint converter

echo Installing dependencies...
python -m pip install -r requirements.txt

echo.
echo Dependencies installed successfully!
echo Run: python pdf_to_ppt.py
pause
