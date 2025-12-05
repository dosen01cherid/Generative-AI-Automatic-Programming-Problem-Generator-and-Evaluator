import asyncio
import os
import sys
from pathlib import Path
from pyppeteer import launch

# Paths
BASE_DIR = Path(__file__).parent.parent.resolve()
EXTENSION_PATH = BASE_DIR / 'whatsapp-analytics-extension'
ANALYTICS_PATH = BASE_DIR / 'analytics_for_problem.html'
PROFILE_DIR = Path(__file__).parent / 'chrome-profile'

# Portable Chromium path - adjust this to your portable Chromium location
PORTABLE_CHROMIUM_PATH = os.environ.get('CHROMIUM_PATH') or str(Path(__file__).parent / 'chrome-win' / 'chrome.exe')

# Parse command line args
args = sys.argv[1:]
whatsapp_only = '--whatsapp-only' in args
analytics_only = '--analytics-only' in args


async def main():
    print('Starting Chrome with WhatsApp Analytics extension...\n')
    print(f'Extension: {EXTENSION_PATH}')
    print(f'Analytics: {ANALYTICS_PATH}')
    print(f'Profile: {PROFILE_DIR}')
    print(f'Chromium: {PORTABLE_CHROMIUM_PATH}')
    print('')

    # Check if portable Chromium exists
    if not os.path.exists(PORTABLE_CHROMIUM_PATH):
        print(f'ERROR: Portable Chromium not found at: {PORTABLE_CHROMIUM_PATH}')
        print('\nPlease either:')
        print(f'1. Download portable Chromium and extract it to: {Path(PORTABLE_CHROMIUM_PATH).parent}')
        print('   Download from: https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html')
        print('2. Or set the CHROMIUM_PATH environment variable to your Chromium executable')
        print('   Example: set CHROMIUM_PATH=C:\\path\\to\\chrome.exe')
        sys.exit(1)

    # Create profile directory if it doesn't exist
    PROFILE_DIR.mkdir(exist_ok=True)

    browser = await launch(
        executablePath=PORTABLE_CHROMIUM_PATH,
        headless=False,
        args=[
            f'--disable-extensions-except={EXTENSION_PATH}',
            f'--load-extension={EXTENSION_PATH}',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--start-maximized',
            # Allow file:// access for extension
            '--allow-file-access-from-files',
            '--allow-file-access',
        ],
        defaultViewport=None,
        userDataDir=str(PROFILE_DIR),
    )

    # Get the default page that opens
    pages = await browser.pages()
    default_page = pages[0]

    if not analytics_only:
        # Open WhatsApp Web
        print('Opening WhatsApp Web...')
        await default_page.goto('https://web.whatsapp.com', {
            'waitUntil': 'networkidle2',
            'timeout': 60000
        })
        print('WhatsApp Web loaded!')

        # Check if logged in or need QR scan
        try:
            await default_page.waitForSelector('[data-icon="search"]', {'timeout': 10000})
            print('Already logged in to WhatsApp!')
        except:
            print('Please scan QR code to log in (first time only)')

    if not whatsapp_only:
        # Open Analytics page
        print('\nOpening Analytics Dashboard...')
        analytics_page = await browser.newPage()
        await analytics_page.goto(f'file:///{ANALYTICS_PATH}', {
            'waitUntil': 'networkidle2',
            'timeout': 60000
        })
        print('Analytics Dashboard loaded!')

    print('\n========================================')
    print('Setup complete!')
    print('========================================')
    print('')
    print('The extension is now active and monitoring.')
    print('')
    print('How to use:')
    print('1. WhatsApp: Messages with progress reports will be captured')
    print('2. Click the extension icon to see captured reports')
    print('3. Click "Auto-Inject to Analytics" to send data')
    print('')
    print('Press Ctrl+C to close browser and exit.')
    print('')

    # Keep the script running
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print('\nClosing browser...')
        await browser.close()
        sys.exit(0)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as err:
        print(f'Error: {err}')
        sys.exit(1)
