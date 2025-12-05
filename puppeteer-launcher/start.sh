#!/bin/bash
# WhatsApp Analytics Launcher - Linux/macOS Script
# Installs dependencies and launches Chrome with extension

set -e

cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.7+ from your package manager"
    exit 1
fi

echo "Found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    echo "Please install pip3 from your package manager"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import pyppeteer" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
fi

# Launch the browser
echo ""
python3 launch.py "$@"
