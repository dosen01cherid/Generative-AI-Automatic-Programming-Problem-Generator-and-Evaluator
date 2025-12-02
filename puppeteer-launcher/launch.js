const puppeteer = require('puppeteer');
const path = require('path');

// Paths
const BASE_DIR = path.resolve(__dirname, '..');
const EXTENSION_PATH = path.join(BASE_DIR, 'whatsapp-analytics-extension');
const ANALYTICS_PATH = path.join(BASE_DIR, 'analytics_for_problem.html');
const PROFILE_DIR = path.join(__dirname, 'chrome-profile');

// Parse command line args
const args = process.argv.slice(2);
const whatsappOnly = args.includes('--whatsapp-only');
const analyticsOnly = args.includes('--analytics-only');

async function launch() {
    console.log('Starting Chrome with WhatsApp Analytics extension...\n');
    console.log('Extension:', EXTENSION_PATH);
    console.log('Analytics:', ANALYTICS_PATH);
    console.log('Profile:', PROFILE_DIR);
    console.log('');

    const browser = await puppeteer.launch({
        headless: false,
        args: [
            `--disable-extensions-except=${EXTENSION_PATH}`,
            `--load-extension=${EXTENSION_PATH}`,
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--start-maximized',
            // Allow file:// access for extension
            '--allow-file-access-from-files',
            '--allow-file-access',
        ],
        defaultViewport: null,
        userDataDir: PROFILE_DIR,
        // Slow down for debugging (optional)
        // slowMo: 50,
    });

    // Get the default page that opens
    const pages = await browser.pages();
    let defaultPage = pages[0];

    if (!analyticsOnly) {
        // Open WhatsApp Web
        console.log('Opening WhatsApp Web...');
        await defaultPage.goto('https://web.whatsapp.com', {
            waitUntil: 'networkidle2',
            timeout: 60000
        });
        console.log('WhatsApp Web loaded!');

        // Check if logged in or need QR scan
        try {
            await defaultPage.waitForSelector('[data-icon="search"]', { timeout: 10000 });
            console.log('Already logged in to WhatsApp!');
        } catch {
            console.log('Please scan QR code to log in (first time only)');
        }
    }

    if (!whatsappOnly) {
        // Open Analytics page
        console.log('\nOpening Analytics Dashboard...');
        const analyticsPage = await browser.newPage();
        await analyticsPage.goto(`file://${ANALYTICS_PATH}`, {
            waitUntil: 'networkidle2',
            timeout: 60000
        });
        console.log('Analytics Dashboard loaded!');
    }

    console.log('\n========================================');
    console.log('Setup complete!');
    console.log('========================================');
    console.log('');
    console.log('The extension is now active and monitoring.');
    console.log('');
    console.log('How to use:');
    console.log('1. WhatsApp: Messages with progress reports will be captured');
    console.log('2. Click the extension icon to see captured reports');
    console.log('3. Click "Auto-Inject to Analytics" to send data');
    console.log('');
    console.log('Press Ctrl+C to close browser and exit.');
    console.log('');

    // Keep the script running
    process.on('SIGINT', async () => {
        console.log('\nClosing browser...');
        await browser.close();
        process.exit(0);
    });

    // Prevent script from exiting
    await new Promise(() => {});
}

launch().catch(err => {
    console.error('Error:', err.message);
    process.exit(1);
});
