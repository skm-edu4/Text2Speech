#!/bin/bash
# setup.sh - Project Setup Script for Edge-TTS

echo "========================================="
echo "  TTS Project Setup (Edge-TTS)"
echo "========================================="

# Create directories (No 'models' folder needed anymore!)
echo "Creating directories..."
mkdir -p output
mkdir -p logs

# Check Python version
echo "Checking Python version..."
python3 --version

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "✅ Edge-TTS requires NO local model downloads."
echo "   You are ready to generate high-quality audio!"
echo ""
echo "Usage Options:"
echo "  1. CLI Mode:       python3 main.py"
echo "  2. Web Interface:  uvicorn app:app --reload"
echo ""
echo "========================================="
