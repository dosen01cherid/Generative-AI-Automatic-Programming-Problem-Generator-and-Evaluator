# WhatsApp Analytics Launcher

Simple launcher for Chrome with the WhatsApp Analytics extension pre-loaded.

**No dependencies needed!** Just portable Chrome and the extension.

## Features

- No Node.js or Python libraries required
- Simple batch/Python scripts that launch Chrome directly
- Loads extension automatically
- Opens WhatsApp Web and Analytics Dashboard
- Persists WhatsApp login between sessions
- Cross-platform (Windows, Linux, macOS)

## Requirements

- Portable Chrome/Chromium **OR** Chrome/Chromium installed on your system
- The WhatsApp Analytics extension folder

## Setup

### Get Portable Chrome (One-time setup)

**Option A: Download Portable Chromium (Recommended)**

1. Download from: https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html
   - Windows: Download `chrome-win.zip` from Win_x64 folder (latest snapshot)
   - Linux: Download `chrome-linux.zip`
   - macOS: Download `chrome-mac.zip`
2. Extract to `puppeteer-launcher/chrome-win/` (Windows) or adjust for your OS
3. Verify `chrome.exe` is at: `puppeteer-launcher/chrome-win/chrome.exe`

**Option B: Use Your Installed Chrome**

Set the `CHROMIUM_PATH` environment variable:

Windows (Command Prompt):
```cmd
set CHROMIUM_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe
```

Windows (PowerShell):
```powershell
$env:CHROMIUM_PATH="C:\Program Files\Google\Chrome\Application\chrome.exe"
```

Linux:
```bash
export CHROMIUM_PATH=/usr/bin/chromium
```

macOS:
```bash
export CHROMIUM_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```

## Quick Start

### Windows - Easiest Way

**Double-click:** `launch_chrome.bat`

Or from Command Prompt:
```cmd
cd puppeteer-launcher
launch_chrome.bat
```

### Using Python (All Platforms)

**Windows:**
```cmd
cd puppeteer-launcher
python launch_chrome.py
```

**Linux/macOS:**
```bash
cd puppeteer-launcher
python3 launch_chrome.py
```

## Options

| Command | Description |
|---------|-------------|
| `launch_chrome.bat` | Open WhatsApp + Analytics |
| `launch_chrome.bat --whatsapp-only` | WhatsApp only |
| `launch_chrome.bat --analytics-only` | Analytics only |

Same options work with Python version:
```bash
python launch_chrome.py --whatsapp-only
python launch_chrome.py --analytics-only
```

## First Time Setup

1. Download portable Chrome (see Setup above)
2. Run the launcher
3. Scan WhatsApp QR code when prompted
4. Done! Next time WhatsApp will auto-login

## Files

```
puppeteer-launcher/
├── launch_chrome.bat     # Windows launcher (SIMPLEST - NO DEPENDENCIES!)
├── launch_chrome.py      # Python launcher (also no pip dependencies!)
├── chrome-profile/       # Browser data (created on first run)
├── chrome-win/           # Portable Chrome (download separately)
│   └── chrome.exe
└── README.md             # This file

Legacy files (can be deleted):
├── launch.js             # Old Node.js version
├── launch.py             # Old pyppeteer version
├── package.json          # Old Node.js dependencies
├── requirements.txt      # Old Python dependencies
├── start.bat/sh/ps1      # Old launcher scripts
└── node_modules/         # Old Node.js packages
```

## How It Works

1. Launcher script calls Chrome with special command-line flags:
   - `--load-extension=` to load the extension
   - `--user-data-dir=` for persistent profile/login
   - `--allow-file-access-from-files` for local HTML access
2. Chrome opens with extension already loaded
3. Opens WhatsApp Web and/or Analytics Dashboard
4. Extension monitors WhatsApp for progress reports
5. Click extension icon to send reports to Analytics

## Troubleshooting

### "Chrome not found"
Either:
1. Download portable Chrome and extract to `puppeteer-launcher/chrome-win/`
2. Set `CHROMIUM_PATH` environment variable to your Chrome executable

### Extension not loading
Make sure the `whatsapp-analytics-extension` folder exists in the parent directory.

### WhatsApp asking for QR code every time
The `chrome-profile` folder stores login data. Don't delete it.

### Analytics page not loading
Make sure `analytics_for_problem.html` exists in the parent directory.

## Why This Approach?

**Previous approach (puppeteer/pyppeteer):**
- Requires Node.js or Python libraries
- 100+ MB of dependencies
- Overcomplicated for just launching a browser
- Meant for browser automation (testing, scraping, etc.)

**Current approach (direct Chrome launch):**
- **Zero dependencies** (except portable Chrome)
- Just a simple batch/Python script
- Does exactly what's needed - nothing more
- Much faster startup
- Easier to understand and modify

## Benefits

✅ **No npm install** - No Node.js needed
✅ **No pip install** - No Python packages needed
✅ **Portable** - Put on USB drive and go
✅ **Simple** - Just Chrome + extension + scripts
✅ **Fast** - Instant launch, no library overhead
✅ **Transparent** - Easy to see what's happening

---

**TL;DR:** Just run `launch_chrome.bat` on Windows. That's it!
