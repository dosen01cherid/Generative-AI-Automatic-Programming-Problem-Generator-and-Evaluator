#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Chrome Launcher with WhatsApp Analytics Extension
No browser automation library needed - just launches Chrome directly
"""

import os
import sys
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent.resolve()
EXTENSION_PATH = BASE_DIR / 'whatsapp-analytics-extension'
ANALYTICS_PATH = BASE_DIR / 'analytics_for_problem.html'
PROFILE_DIR = Path(__file__).parent / 'chrome-profile'

# Portable Chrome path - adjust this to your portable Chrome location
CHROME_PATH = os.environ.get('CHROMIUM_PATH') or str(Path(__file__).parent / 'chrome-win' / 'chrome.exe')

# Parse command line args
args = sys.argv[1:]
whatsapp_only = '--whatsapp-only' in args
analytics_only = '--analytics-only' in args


def main():
    print('Starting Chrome with WhatsApp Analytics extension...\n')
    print(f'Chrome: {CHROME_PATH}')
    print(f'Extension: {EXTENSION_PATH}')
    print(f'Analytics: {ANALYTICS_PATH}')
    print(f'Profile: {PROFILE_DIR}')
    print('')

    # Check if Chrome exists
    if not os.path.exists(CHROME_PATH):
        print(f'ERROR: Chrome not found at: {CHROME_PATH}')
        print('\nPlease either:')
        print(f'1. Download portable Chrome and extract it to: {Path(CHROME_PATH).parent}')
        print('   Download from: https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html')
        print('2. Or set the CHROMIUM_PATH environment variable to your Chrome executable')
        print('   Example (Windows): set CHROMIUM_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe')
        sys.exit(1)

    # Check if extension exists
    if not os.path.exists(EXTENSION_PATH):
        print(f'ERROR: Extension not found at: {EXTENSION_PATH}')
        print('Make sure the whatsapp-analytics-extension folder exists in the parent directory')
        sys.exit(1)

    # Create profile directory if it doesn't exist
    PROFILE_DIR.mkdir(exist_ok=True)

    # Build Chrome command-line arguments
    chrome_args = [
        CHROME_PATH,
        f'--load-extension={EXTENSION_PATH}',
        f'--user-data-dir={PROFILE_DIR}',
        '--no-first-run',
        '--no-default-browser-check',
        '--start-maximized',
        '--allow-file-access-from-files',
        '--allow-file-access',
    ]

    # Add URLs to open
    urls = []
    if not analytics_only:
        urls.append('https://web.whatsapp.com')

    if not whatsapp_only:
        # Convert Windows path to file:/// URL
        analytics_url = f'file:///{ANALYTICS_PATH}'.replace('\\', '/')
        urls.append(analytics_url)

    # Add URLs to command
    chrome_args.extend(urls)

    print('Launching Chrome...')
    print('')
    print('========================================')
    print('Chrome will open with:')
    if not analytics_only:
        print('  - WhatsApp Web')
    if not whatsapp_only:
        print('  - Analytics Dashboard')
    print('  - Extension loaded and active')
    print('========================================')
    print('')
    print('How to use:')
    print('1. WhatsApp: Messages with progress reports will be captured')
    print('2. Click the extension icon to see captured reports')
    print('3. Click "Auto-Inject to Analytics" to send data')
    print('')
    print('Note: Close Chrome when done (this script will exit immediately)')
    print('')

    try:
        # Launch Chrome (non-blocking)
        if sys.platform == 'win32':
            # Windows: use CREATE_NEW_PROCESS_GROUP to detach
            subprocess.Popen(chrome_args,
                           creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                           close_fds=True)
        else:
            # Linux/macOS: use nohup equivalent
            subprocess.Popen(chrome_args,
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL,
                           start_new_session=True)

        print('Chrome launched successfully!')
        print('You can close this window - Chrome will keep running.')

    except Exception as e:
        print(f'ERROR: Failed to launch Chrome: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()
