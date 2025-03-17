#!/bin/bash

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Please install Python 3.6 or later."
    exit 1
fi

# Check if pip is installed
python3 -m ensurepip --upgrade

# Install Python packages
echo "Installing required Python packages..."
pip3 install --upgrade pip
pip3 install pygame python-kasa Pillow pywin32 setuptools

# Check if dependencies are installed successfully
python3 -c "import pygame, kasa, PIL; print('pygame:', pygame.__version__); print('kasa:', kasa.__version__); print('PIL:', PIL.__version__)" && echo "All required packages installed successfully."

# End
