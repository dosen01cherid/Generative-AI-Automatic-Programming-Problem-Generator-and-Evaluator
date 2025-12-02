# WhatsApp Analytics Launcher

Automatically launches Chrome with the WhatsApp Analytics extension loaded using Puppeteer.

## Features

- Loads extension automatically (no manual developer mode needed)
- Opens WhatsApp Web and Analytics Dashboard
- Persists WhatsApp login between sessions
- Cross-platform (Linux, Windows, macOS)

## Requirements

- Node.js 18+ installed
- Internet connection (first run downloads Chromium)

## Quick Start

### Linux / macOS

```bash
cd puppeteer-launcher
./start.sh
```

### Windows (Command Prompt)

```cmd
cd puppeteer-launcher
start.bat
```

### Windows (PowerShell)

```powershell
cd puppeteer-launcher
.\start.ps1
```

### Using npm directly

```bash
cd puppeteer-launcher
npm install    # First time only
npm start
```

## Options

| Command | Description |
|---------|-------------|
| `npm start` | Open both WhatsApp + Analytics |
| `npm run whatsapp` | WhatsApp only |
| `npm run analytics` | Analytics only |

Or with scripts:

```bash
# Linux
./start.sh --whatsapp-only
./start.sh --analytics-only

# Windows
start.bat --whatsapp-only
start.bat --analytics-only
```

## First Time Setup

1. Run the launcher
2. Scan WhatsApp QR code when prompted
3. Done! Next time WhatsApp will auto-login

## Files

```
puppeteer-launcher/
├── package.json     # Dependencies
├── launch.js        # Main launcher script
├── start.sh         # Linux/macOS launcher
├── start.bat        # Windows CMD launcher
├── start.ps1        # Windows PowerShell launcher
├── chrome-profile/  # Persistent browser data (created on first run)
└── README.md        # This file
```

## How It Works

1. Puppeteer launches Chromium with extension flags
2. Extension is loaded from `../whatsapp-analytics-extension/`
3. WhatsApp Web and Analytics pages are opened
4. Extension monitors WhatsApp for progress reports
5. Click extension icon to send reports to Analytics

## Troubleshooting

### "Cannot find module 'puppeteer'"
Run `npm install` first.

### Extension not loading
Make sure the `whatsapp-analytics-extension` folder exists in the parent directory.

### WhatsApp asking for QR code every time
The `chrome-profile` folder stores login data. Don't delete it.

### Windows: "Execution policy" error with PowerShell
Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
