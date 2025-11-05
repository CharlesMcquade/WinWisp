@echo off
echo Installing WindowsWhisper...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Installation complete!
echo.
echo IMPORTANT: Make sure FFmpeg is installed and in your PATH
echo Download FFmpeg from: https://ffmpeg.org/download.html
echo.
echo To run the application, execute: python main.py
echo.
pause
