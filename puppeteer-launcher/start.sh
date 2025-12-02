#!/bin/bash

# WhatsApp Analytics Launcher
# Starts Chrome with extension loaded via Puppeteer

cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Run the launcher
echo "Starting WhatsApp Analytics..."
node launch.js "$@"
