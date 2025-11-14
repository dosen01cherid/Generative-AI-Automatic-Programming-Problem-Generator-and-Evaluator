const analyticsStatus = document.getElementById('analyticsStatus');
const whatsappStatus = document.getElementById('whatsappStatus');
const btnOpenAnalytics = document.getElementById('btnOpenAnalytics');
const btnOpenWhatsApp = document.getElementById('btnOpenWhatsApp');

// Check connection status
function updateStatus() {
    chrome.runtime.sendMessage({ type: 'check_connection' }, (response) => {
        if (response) {
            // Update Analytics status
            if (response.analytics) {
                analyticsStatus.className = 'status connected';
                analyticsStatus.textContent = '✅ Analytics: Connected';
            } else {
                analyticsStatus.className = 'status disconnected';
                analyticsStatus.textContent = '⚠️ Analytics: Not Connected';
            }

            // Update WhatsApp status
            if (response.whatsapp) {
                whatsappStatus.className = 'status connected';
                whatsappStatus.textContent = '✅ WhatsApp: Connected';
            } else {
                whatsappStatus.className = 'status disconnected';
                whatsappStatus.textContent = '⚠️ WhatsApp: Not Connected';
            }
        }
    });
}

// Update status every second
updateStatus();
setInterval(updateStatus, 1000);

// Open analytics page
btnOpenAnalytics.addEventListener('click', () => {
    // Try to find if already open
    chrome.tabs.query({}, (tabs) => {
        const analyticsTab = tabs.find(tab =>
            tab.url && tab.url.includes('analytics_for_problem.html')
        );

        if (analyticsTab) {
            // Focus existing tab
            chrome.tabs.update(analyticsTab.id, { active: true });
        } else {
            // Open new tab
            // Get the extension's base URL
            const extensionUrl = chrome.runtime.getURL('');

            // Prompt user for file location
            const html = `
                <html>
                <head><title>Open Analytics</title></head>
                <body style="font-family:sans-serif;padding:40px;max-width:600px;margin:auto;">
                    <h2>Open Analytics Page</h2>
                    <p>Please open <code>analytics_for_problem.html</code> manually:</p>
                    <ol>
                        <li>Open the file in your browser</li>
                        <li>Or use a local server: <code>python3 -m http.server</code></li>
                    </ol>
                    <p>The extension will automatically detect when it's open.</p>
                </body>
                </html>
            `;

            const blob = new Blob([html], { type: 'text/html' });
            const url = URL.createObjectURL(blob);
            chrome.tabs.create({ url });
        }
    });
});

// Open WhatsApp Web
btnOpenWhatsApp.addEventListener('click', () => {
    // Try to find if already open
    chrome.tabs.query({ url: 'https://web.whatsapp.com/*' }, (tabs) => {
        if (tabs.length > 0) {
            // Focus existing tab
            chrome.tabs.update(tabs[0].id, { active: true });
        } else {
            // Open new tab
            chrome.tabs.create({ url: 'https://web.whatsapp.com' });
        }
    });
});
