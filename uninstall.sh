#!/bin/bash
# Echo Clear Uninstall Script

echo "========================================"
echo "  Echo Clear Uninstaller"
echo "========================================"
echo ""

read -p "Are you sure you want to uninstall Echo Clear? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
echo "🗑️  Removing virtual environment..."
if [ -d ".venv" ]; then
    rm -rf .venv
    echo "✅ Virtual environment removed"
fi

echo ""
echo "🗑️  Removing desktop entry..."
if [ -f "$HOME/.local/share/applications/echo-clear.desktop" ]; then
    rm "$HOME/.local/share/applications/echo-clear.desktop"
    echo "✅ Desktop entry removed"
fi

echo ""
echo "========================================"
echo "  Uninstall Complete"
echo "========================================"
echo ""
echo "The source files remain in this directory."
echo "To completely remove Echo Clear, delete this folder."
echo ""
