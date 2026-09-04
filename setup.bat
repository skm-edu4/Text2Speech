
---

### 3. `setup.bat` (For Windows Users)
*Save this in your project root. It automates the entire setup process for Windows.*

```bat
@echo off
echo =========================================
echo   TTS Project Setup (Windows)
echo =========================================

REM Create directories
echo Creating directories...
if not exist output mkdir output
if not exist logs mkdir logs

REM Check Python
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    echo Try running: pip install --upgrade pip
    pause
    exit /b 1
)

echo.
echo =========================================
echo   Setup Complete!
echo =========================================
echo.
echo Edge-TTS requires NO local model downloads.
echo You are ready to generate high-quality audio!
echo.
echo Usage:
echo   1. Web Interface: uvicorn app:app --reload
echo   2. CLI Mode:      python main.py
echo.
pause
