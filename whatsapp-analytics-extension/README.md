# WhatsApp Analytics Extension

A Chrome/Edge browser extension that automatically captures student progress reports from WhatsApp Web and integrates with the Analytics App.

## Features

- **Auto-Capture**: Automatically detects and captures base64-encoded progress reports from WhatsApp messages
- **Real-time Monitoring**: Scans messages in real-time as they arrive
- **Phone Number Detection**: Extracts student phone numbers from chat context
- **🆕 Auto-Inject Mode**: Enable continuous automatic injection - reports inject instantly when captured!
- **Smart Tab Detection**: Finds open Analytics App or opens it automatically
- **One-Click Export**: Export captured reports directly to the Analytics App
- **Privacy-Focused**: All data stays local, no external servers
- **Easy Toggle**: Enable/disable auto-capture and auto-inject with one click

## Installation

### Method 1: Load Unpacked Extension (Development Mode)

1. **Download the Extension**
   - The extension files are in the `whatsapp-analytics-extension` folder

2. **Open Chrome/Edge Extensions Page**
   - Chrome: Navigate to `chrome://extensions`
   - Edge: Navigate to `edge://extensions`

3. **Enable Developer Mode**
   - Toggle the "Developer mode" switch in the top-right corner

4. **Load the Extension**
   - Click "Load unpacked"
   - Select the `whatsapp-analytics-extension` folder
   - The extension should now appear in your extensions list

5. **Pin the Extension** (Optional)
   - Click the puzzle piece icon in the toolbar
   - Click the pin icon next to "WhatsApp Analytics"

6. **Enable File Access** (Required for Auto-Inject with local files)
   - Click "Details" on the extension card
   - Scroll down and enable "Allow access to file URLs"
   - This lets the extension inject data into `file:///` Analytics App pages

### Method 2: Generate Better Icons (Optional)

The extension includes placeholder icons. For better-looking icons:

1. Open `whatsapp-analytics-extension/icons/generate-icons.html` in your browser
2. Right-click each generated icon and "Save Image As..."
3. Save as `icon16.png`, `icon48.png`, and `icon128.png` in the `icons` folder
4. Reload the extension in Chrome

## Setup

### 1. Configure Analytics App URL

1. Click the extension icon in your browser toolbar
2. In the "Settings" section, enter your Analytics App URL
   - For local file: `file:///path/to/analytics_for_problem.html`
   - For web server: `http://localhost:8000/analytics_for_problem.html`
3. Click "Save Settings"

### 2. Open WhatsApp Web

1. Navigate to https://web.whatsapp.com
2. Scan the QR code to login
3. The extension will automatically start monitoring

## Usage

### Automatic Capture

1. **Monitor is Active**: The extension automatically scans all messages
2. **Detection**: When a student sends a progress report (base64-encoded data), it's captured automatically
3. **Notification**: You'll see a notification when new reports are captured
4. **Badge**: The extension icon shows the number of captured reports

### View Captured Reports

1. Click the extension icon
2. See the count of captured reports in the dashboard
3. View recent reports in the "Recent Reports" section
4. Click "View Captured Reports" for detailed view

### Export to Analytics App

**Method 1: 🆕🆕 AUTO-INJECT MODE (FULLY AUTOMATIC!)**

Enable continuous automatic injection:

1. Click the extension icon
2. Toggle "🚀 Auto-Inject Mode" to **ON**
3. That's it! Now:
   - Every new report is **instantly injected**
   - No clicks needed
   - Completely hands-free
   - Works 24/7 while enabled

**To disable:** Toggle "Auto-Inject Mode" to OFF

**Method 2: Manual Inject (One-Click)**

1. Click the extension icon
2. Click "🚀 Manual Inject Now"
3. Done! The extension:
   - Finds or opens Analytics App
   - Injects data directly into the page
   - Automatically starts analysis
   - No copy/paste needed!

**Method 3: Copy & Paste**

1. Click the extension icon
2. Click "📤 Copy & Open Analytics"
3. Reports are copied to clipboard and Analytics App opens
4. Paste (Ctrl+V) into the text area
5. Click "Analyze & Add Submissions"

**Method 3: Manual Process**

1. Click "View Captured Reports"
2. Copy individual or all reports
3. Open Analytics App
4. Paste and analyze

**Note:** Auto-Inject is the fastest and easiest method! See [AUTO-INJECT-GUIDE.md](AUTO-INJECT-GUIDE.md) for detailed information.

### Clear Reports

1. Click the extension icon
2. Click "Clear All Reports"
3. Confirm the action

## How It Works

### Technical Flow

1. **Content Script** (`content.js`)
   - Runs on WhatsApp Web
   - Monitors DOM for new messages
   - Extracts base64-encoded data (100+ characters)
   - Captures phone numbers and timestamps

2. **Background Worker** (`background.js`)
   - Stores captured reports
   - Manages notifications
   - Handles data persistence

3. **Popup UI** (`popup.html` + `popup.js`)
   - Shows statistics and controls
   - Manages settings
   - Handles export functionality

### What Gets Captured

For each progress report, the extension captures:
- **Base64 Data**: The encoded progress report
- **Sender Name**: Student's WhatsApp display name
- **Phone Number**: Extracted from chat header or sender info
- **Timestamp**: When the message was sent
- **Capture Time**: When the extension detected it

### Privacy & Security

- **Local Storage Only**: All data stored in browser's local storage
- **No External Servers**: No data sent anywhere except when you export
- **User Control**: You control when to export and where
- **Permissions**: Only accesses WhatsApp Web, nothing else

## Troubleshooting

### Extension Not Detecting Messages

1. **Check if enabled**: Make sure auto-capture toggle is ON
2. **Refresh WhatsApp**: Reload WhatsApp Web page
3. **Check console**: Open DevTools (F12) and check for errors
4. **Verify format**: Make sure messages contain base64 data (100+ chars)

### No Phone Numbers Captured

- Phone numbers are extracted from chat headers
- For individual chats, the number usually appears in the header
- For group chats, individual numbers may not be available
- Fallback: Extension marks as "Unknown phone"

### Export Not Working

1. **Check URL**: Verify Analytics App URL is correct in settings
2. **Test clipboard**: Make sure clipboard access is allowed
3. **Try manual**: Copy reports manually and paste into Analytics App

### Icons Not Showing

1. Use the icon generator: Open `icons/generate-icons.html`
2. Download the generated icons
3. Replace the placeholder files
4. Reload the extension

## File Structure

```
whatsapp-analytics-extension/
├── manifest.json          # Extension configuration
├── content.js            # WhatsApp Web page monitor
├── background.js         # Background service worker
├── popup.html            # Extension popup UI
├── popup.js              # Popup functionality
├── README.md             # This file
└── icons/
    ├── icon16.png        # 16x16 icon
    ├── icon48.png        # 48x48 icon
    ├── icon128.png       # 128x128 icon
    ├── icon.svg          # SVG icon source
    └── generate-icons.html  # Icon generator tool
```

## Permissions Explained

The extension requests the following permissions:

- **storage**: To save captured reports and settings locally
- **activeTab**: To access the current tab when you click the extension
- **notifications**: To show alerts when reports are captured
- **host_permissions** (web.whatsapp.com): To monitor WhatsApp Web messages

## Development

### Testing

1. Make changes to the code
2. Go to `chrome://extensions`
3. Click the refresh icon on the extension card
4. Test on WhatsApp Web

### Debugging

- **Content Script**: Open DevTools on WhatsApp Web page, check Console
- **Background Worker**: Go to `chrome://extensions`, click "service worker" link
- **Popup**: Right-click extension icon → Inspect popup

## Version History

### v1.3.0 (2024-11-14)
- **🆕 NEW: Real-Time Dashboard Support** - Extension triggers live updates in Analytics App
- **Event Dispatching** - Notifies real-time views when new submissions arrive
- **Timed-Quiz Integration** - Automatic leaderboard updates during quiz mode
- **Live Updates** - Dashboard and leaderboard refresh automatically with new data
- **Enhanced Auto-Inject** - Now includes event dispatching for live features

### v1.2.0 (2024-11-14)
- **🆕🆕 NEW: Auto-Inject Mode** - Continuous automatic injection!
- **Toggle-Activated** - One switch to enable/disable continuous injection
- **Instant Injection** - Reports inject automatically when captured
- **Status Indicator** - Visual feedback when auto-inject mode is active
- **Zero-Click Workflow** - Completely hands-free operation
- **Validation** - Prevents enabling without Analytics URL configured

### v1.1.0 (2024-11-14)
- **🆕 NEW: Auto-Inject Feature** - Direct data injection into Analytics App
- **Tab Communication** - Extension can now communicate with Analytics App page
- **Smart Tab Detection** - Automatically finds or opens Analytics App
- **Auto-Analysis** - Optionally trigger analysis automatically after injection
- **Content Script Injection** - Dynamic script injection into Analytics page
- Added comprehensive AUTO-INJECT-GUIDE.md documentation

### v1.0.0 (2024-11-14)
- Initial release
- Auto-capture progress reports from WhatsApp
- Phone number and timestamp extraction
- One-click export to Analytics App
- Local storage persistence

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review console logs for errors
3. Ensure WhatsApp Web is fully loaded before use

## License

Created for educational use with the Generative-AI-Automatic-Programming-Problem-Generator-and-Evaluator project.

## Credits

Developed to enhance the student analytics workflow for the Programming Problem Generator project.
