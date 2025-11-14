# Quick Start Guide

Get up and running with the WhatsApp Analytics Extension in 5 minutes!

## 🆕 NEW: Auto-Inject Mode

**The easiest way ever - completely automatic!**

Once configured, just:
1. Toggle "Auto-Inject Mode" ON
2. Open WhatsApp Web
3. Done! Reports inject automatically as students send them!

No clicks, no waiting, no manual work!

## Step 1: Install the Extension (2 minutes)

1. Open Chrome or Edge browser
2. Go to `chrome://extensions` (or `edge://extensions`)
3. Enable "Developer mode" (toggle in top-right)
4. Click "Load unpacked"
5. Select the `whatsapp-analytics-extension` folder
6. Done! You should see the extension icon (📊) in your toolbar

## Step 2: Configure Settings (1 minute)

1. Click the extension icon in your toolbar
2. Scroll to "Settings" section
3. Enter your Analytics App URL:
   ```
   file:///path/to/your/analytics_for_problem.html
   ```
   Or if using a web server:
   ```
   http://localhost:8000/analytics_for_problem.html
   ```
4. Click "Save Settings"

## Step 3: Open WhatsApp Web (30 seconds)

1. Go to https://web.whatsapp.com
2. Scan QR code to login
3. Open a chat (individual or group)
4. The extension starts monitoring automatically!

## Step 4: Capture Reports (Automatic!)

When students send progress reports:
- The extension detects them automatically
- A notification pops up
- The badge shows the count

## Step 5: Choose Your Workflow

### Option A: Auto-Inject Mode (RECOMMENDED - Zero clicks!)

1. Click the extension icon
2. Toggle "🚀 Auto-Inject Mode" to **ON**
3. Done! Reports now inject automatically!

### Option B: Manual Inject (One click when ready)

1. Click the extension icon
2. Click "🚀 Manual Inject Now"
3. Done!

### Option C: Copy & Paste (Traditional)

1. Click the extension icon
2. Click "📤 Copy & Open Analytics"
3. Press Ctrl+V to paste
4. Click "Analyze & Add Submissions"

## Visual Guide

```
Student sends message with base64 data
          ↓
Extension detects it automatically
          ↓
Notification: "1 new progress report captured!"
          ↓
Click extension icon → See count
          ↓
Click "Export to Analytics App"
          ↓
Data copied → Analytics App opens
          ↓
Paste → Analyze → View results!
```

## Tips

- **Keep it enabled**: The auto-capture toggle should stay ON
- **Check regularly**: Click the icon to see how many reports captured
- **Export often**: Clear old reports after analyzing
- **Reload if needed**: Refresh WhatsApp Web if extension stops working

## Common Questions

**Q: How do I know it's working?**
A: The extension icon shows a badge with the number of captured reports.

**Q: Can I use it on multiple chats?**
A: Yes! It monitors whichever chat is currently open.

**Q: Will it capture old messages?**
A: Yes, when you open a chat, it scans all visible messages once.

**Q: How do I stop it?**
A: Click the extension icon and toggle "Auto-capture enabled" to OFF.

**Q: Where is the data stored?**
A: Locally in your browser. Nothing is sent to any server.

## Need Help?

- See the full README.md for detailed documentation
- Check browser console (F12) for error messages
- Make sure WhatsApp Web is fully loaded
- Verify the Analytics App URL is correct

## That's It!

You're ready to automatically capture and analyze student progress reports from WhatsApp! 🎉
