#!/bin/bash
# Echo Cleaner Installation Script

set -e

echo "========================================"
echo "  Echo Cleaner Installation"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3.10 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required"
    echo "You have Python $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION detected"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# Activate virtual environment and install dependencies
echo "📥 Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"

echo ""

# Make launcher executable
chmod +x echo-cleaner.py

echo "========================================"
echo "  Installation Complete! ✨"
echo "========================================"
echo ""
echo "To run Echo Cleaner:"
echo "  ./echo-cleaner.py"
echo ""
echo "Or:"
echo "  python3 app/main.py"
echo ""
echo "For development:"
echo "  source .venv/bin/activate"
echo "  python app/main.py"
echo ""
