#!/bin/bash
echo "========================================="
echo "  TTS Project Setup (Mac/Linux)"
echo "========================================="

# Create directories
echo "Creating directories..."
mkdir -p output
mkdir -p logs

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "[ERROR] Python3 is not installed."
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies."
    echo "Try running: pip3 install --upgrade pip"
    exit 1
fi

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "✅ Edge-TTS requires NO local model downloads."
echo "   You are ready to generate high-quality audio!"
echo ""
echo "Usage Options:"
echo "  1. Web Interface:  uvicorn app:app --reload"
echo "  2. CLI Mode:       python3 main.py"
echo ""
echo "========================================="
