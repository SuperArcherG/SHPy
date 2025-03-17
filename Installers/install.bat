@echo off
:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.6 or later.
    exit /b
)

:: Check if pip is installed
python -m ensurepip --upgrade

:: Install Python packages
echo Installing required Python packages...
pip install --upgrade pip
pip install pygame python-kasa Pillow pywin32 setuptools playsound SpeechRecognition pvporcupine pyaudio
@REM speechrecognition pyaudio porcupine

:: Check if dependencies are installed successfully
python -c "import pygame, kasa, PIL; print('pygame:', pygame.__version__); print('kasa:', kasa.__version__); print('PIL:', PIL.__version__)" && echo All required packages installed successfully.

:: End
pause
