# Auto-Inject Feature Guide

## What is Auto-Inject?

**Auto-Inject** is the NEW automated way to send captured reports from the extension directly into the Analytics App **without any manual steps**!

Instead of copying and pasting, the extension now **directly injects** the data into the Analytics App page.

## How It Works

```
WhatsApp Web (Extension captures reports)
           ↓
Extension Background Script
           ↓
Finds/Opens Analytics App tab
           ↓
Injects Content Script into Analytics page
           ↓
Sends reports via Chrome messaging
           ↓
Analytics App receives data automatically
           ↓
Data appears in textarea + Analysis starts!
```

## Technical Architecture

### 1. **Content Script Injection**

The extension injects `analytics-content.js` into the Analytics App page. This script:
- Listens for messages from the extension
- Has full access to the Analytics App's DOM
- Can read and modify the page

### 2. **Tab Communication**

```javascript
// Background script finds the analytics tab
chrome.tabs.query({}) → Find analytics_for_problem.html

// Inject content script
chrome.scripting.executeScript({
    target: { tabId: analyticsTab.id },
    files: ['analytics-content.js']
})

// Send message to content script
chrome.tabs.sendMessage(tabId, {
    type: 'AUTO_IMPORT',
    reports: capturedReports
})
```

### 3. **Data Injection**

```javascript
// In analytics-content.js
chrome.runtime.onMessage.addListener((message) => {
    if (message.type === 'AUTO_IMPORT') {
        // Get textarea
        const textarea = document.querySelector('#pasteProgressData');

        // Inject data
        textarea.value = combinedBase64Data;

        // Click analyze button
        document.querySelector('#analyzeBtn').click();
    }
});
```

## Usage Modes

### Mode 1: Auto-Inject (Fully Automatic)

**What happens:**
1. Click "🚀 Auto-Inject to Analytics"
2. Extension finds if Analytics App is open
   - If yes: Injects data into open tab
   - If no: Opens new tab, waits for load, then injects
3. Data appears in textarea
4. **Analysis starts automatically!**
5. Done!

**Code Flow:**
```
Popup → Background (AUTO_INJECT_TO_ANALYTICS)
     → Find/Create Analytics Tab
     → Inject Content Script
     → Send (AUTO_IMPORT message)
     → Content Script injects data
     → Content Script clicks Analyze button
```

### Mode 2: Manual Inject (Data Only)

**What happens:**
1. Extension injects data
2. You manually click "Analyze & Add Submissions"

**Code Flow:**
```
Background (INJECT_REPORTS message)
→ Content Script injects data
→ Shows notification
→ User clicks analyze manually
```

### Mode 3: Copy & Paste (Old Way)

Still available as "📤 Copy & Open Analytics":
1. Copies to clipboard
2. Opens Analytics App
3. You paste and analyze

## Permissions Required

The auto-inject feature requires these Chrome permissions:

```json
"permissions": [
    "tabs",          // Query and find tabs
    "scripting"      // Inject content scripts
],
"host_permissions": [
    "http://*/*",    // Access localhost
    "https://*/*",   // Access HTTPS sites
    "file:///*"      // Access local files
]
```

### Why These Permissions?

- **tabs**: To find which tab has Analytics App open
- **scripting**: To inject the content script into Analytics page
- **host_permissions**: To access the page regardless of where it's hosted

## File URLs Special Handling

Chrome restricts file:// URLs by default. To enable:

1. Go to `chrome://extensions`
2. Find "WhatsApp Analytics"
3. Click "Details"
4. Enable "Allow access to file URLs"

Without this, the extension can't inject into `file:///...analytics_for_problem.html`

## Message Types

### From Popup/Background to Analytics Content Script:

**INJECT_REPORTS** - Inject data only
```javascript
{
    type: 'INJECT_REPORTS',
    reports: [{data: '...', phone: '...', ...}]
}
```

**AUTO_IMPORT** - Inject data + trigger analysis
```javascript
{
    type: 'AUTO_IMPORT',
    reports: [{data: '...', phone: '...', ...}]
}
```

**PING** - Check if content script is loaded
```javascript
{
    type: 'PING'
}
// Response: {success: true, ready: true}
```

### From Analytics Content Script to Background:

**ANALYTICS_APP_LOADED** - Notify extension that page loaded
```javascript
{
    type: 'ANALYTICS_APP_LOADED',
    url: window.location.href
}
```

## Error Handling

### Common Errors:

**"Analytics URL not configured"**
- Solution: Set Analytics App URL in extension settings

**"Analytics App not open"**
- Solution: Extension will try to open it automatically
- If it fails, manually open the Analytics App first

**"Could not inject content script"**
- Solution: Check if file:// access is enabled (chrome://extensions)
- Solution: Reload the Analytics App page

**"Receiving end does not exist"**
- Cause: Content script not loaded yet
- Solution: Extension retries automatically after 500ms

### Debug Mode:

Open DevTools on both pages:

**WhatsApp Web:**
```
F12 → Console
Look for: "✅ Content script ready"
```

**Analytics App:**
```
F12 → Console
Look for: "📊 Analytics App Content Script loaded"
Look for: "💉 Injecting reports..."
```

**Extension Background:**
```
chrome://extensions → Service Worker → Inspect
Look for: "✅ Reports injected to analytics app"
```

## Security Considerations

### What the Extension Can Do:

✅ Read messages on WhatsApp Web
✅ Inject scripts into Analytics App (if URL matches settings)
✅ Read/write data to Analytics App page
✅ Store data in browser local storage

### What the Extension CANNOT Do:

❌ Access other websites
❌ Send data to external servers
❌ Access files outside browser
❌ Modify system settings

### Privacy:

- All data stays in your browser
- No external API calls
- No tracking
- No analytics sent anywhere
- Data only goes to the Analytics App YOU configured

## Troubleshooting

### Auto-Inject Not Working?

**Step 1: Check Console Logs**
- WhatsApp tab: F12 → Console
- Analytics tab: F12 → Console
- Extension background: chrome://extensions → Service Worker

**Step 2: Verify Settings**
- Extension popup → Settings
- Make sure Analytics URL is correct
- Try both file:// and http:// versions

**Step 3: Check Permissions**
- chrome://extensions
- Find extension
- Check "Allow access to file URLs" is ON

**Step 4: Reload Everything**
- Reload extension (chrome://extensions → Reload)
- Reload WhatsApp Web
- Reload Analytics App

**Step 5: Try Manual Mode**
- Use "Copy & Open Analytics" button
- If this works, it's an injection issue
- If this doesn't work, it's a data issue

### Data Not Appearing?

**Check textarea:**
```javascript
// In Analytics App console:
document.querySelector('#pasteProgressData').value
// Should show base64 data
```

**Check if PyScript loaded:**
```javascript
// In Analytics App console:
typeof window.app
// Should be 'object', not 'undefined'
```

### Analysis Not Starting?

The auto-inject waits for:
1. Page to finish loading (status: 'complete')
2. Additional 3 seconds for PyScript to initialize
3. Content script to confirm it's ready

If it still doesn't work:
- Increase wait time in background.js line 385
- Or use manual injection mode

## Advanced: Custom Integration

### Want to customize the injection?

**Edit `analytics-content.js`:**

```javascript
// Change what happens after injection
function autoImportReports(reports) {
    // ... inject data ...

    // Custom actions:
    // - Show custom notification
    // - Scroll to results
    // - Highlight something
    // - Send confirmation back
}
```

### Want to inject into a different page?

**Edit `background.js`:**

```javascript
// Change tab matching logic
function findAnalyticsTab(sendResponse) {
    const analyticsTabs = tabs.filter(tab => {
        // Add your custom matching logic
        return tab.url.includes('your-custom-page.html');
    });
}
```

## Comparison: Old vs New

| Feature | Copy & Paste | Auto-Inject |
|---------|-------------|-------------|
| Steps | 5+ clicks | 1 click |
| Speed | ~10 seconds | ~2 seconds |
| Manual work | Yes | No |
| Errors | Paste mistakes | None |
| Tab switching | Yes | No |
| Works offline | Yes | Yes |
| Requires Analytics open | No | Opens automatically |

## Future Enhancements

Possible improvements:
- [ ] Real-time streaming (inject as reports arrive)
- [ ] Bi-directional sync (get results back from Analytics)
- [ ] Multiple Analytics instances support
- [ ] Inject to specific problem set
- [ ] Custom injection templates
- [ ] Keyboard shortcuts for inject

## Summary

**Auto-Inject** makes the workflow completely seamless:

**Before:**
1. Capture reports
2. Click export
3. Switch to Analytics
4. Paste
5. Click analyze

**After:**
1. Click "Auto-Inject"
2. Done!

That's the power of direct tab communication! 🚀
