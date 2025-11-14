/**
 * Analytics App Content Script
 * Receives data from extension and injects it into the Analytics App
 */

console.log('📊 Analytics App Content Script loaded');

// Listen for messages from the extension
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('📨 Analytics App received message:', message.type);

    switch (message.type) {
        case 'INJECT_REPORTS':
            injectReports(message.reports);
            sendResponse({ success: true });
            break;

        case 'PING':
            // Check if analytics app is ready
            sendResponse({
                success: true,
                ready: isAnalyticsAppReady()
            });
            break;

        case 'AUTO_IMPORT':
            // Automatically import reports
            autoImportReports(message.reports);
            sendResponse({ success: true });
            break;

        default:
            sendResponse({ success: false, error: 'Unknown message type' });
    }

    return true; // Keep channel open for async response
});

/**
 * Check if analytics app is ready
 */
function isAnalyticsAppReady() {
    // Check if the app object exists (PyScript loaded)
    if (typeof window.app !== 'undefined' && window.app) {
        return true;
    }

    // Check if textarea exists (page structure loaded)
    const textarea = document.querySelector('#pasteProgressData');
    return textarea !== null;
}

/**
 * Inject reports into the analytics app
 */
function injectReports(reports) {
    console.log('💉 Injecting reports into Analytics App:', reports.length);

    if (!reports || reports.length === 0) {
        console.warn('No reports to inject');
        return;
    }

    // Wait for page to be ready
    waitForAnalyticsApp().then(() => {
        // Combine all base64 data
        const combinedData = reports.map(r => r.data).join('\n\n');

        // Get the textarea
        const textarea = document.querySelector('#pasteProgressData');

        if (!textarea) {
            console.error('❌ Textarea not found');
            showNotification('Error: Analytics App not ready', 'error');
            return;
        }

        // Inject the data
        textarea.value = combinedData;

        // Show notification
        showNotification(
            `✅ Injected ${reports.length} progress report${reports.length > 1 ? 's' : ''}`,
            'success'
        );

        // Highlight the textarea briefly
        textarea.style.border = '3px solid #25D366';
        textarea.style.transition = 'border 0.3s';
        setTimeout(() => {
            textarea.style.border = '';
        }, 2000);

        console.log('✅ Reports injected successfully');
    });
}

/**
 * Auto-import reports (inject AND trigger analysis)
 */
function autoImportReports(reports) {
    console.log('🤖 Auto-importing reports:', reports.length);

    if (!reports || reports.length === 0) {
        return;
    }

    waitForAnalyticsApp().then(() => {
        // First inject the data
        const combinedData = reports.map(r => r.data).join('\n\n');
        const textarea = document.querySelector('#pasteProgressData');

        if (!textarea) {
            console.error('❌ Textarea not found');
            return;
        }

        textarea.value = combinedData;

        // Wait a moment, then trigger the analyze button
        setTimeout(() => {
            const analyzeBtn = document.querySelector('#analyzeBtn');

            if (analyzeBtn) {
                console.log('🔍 Triggering analysis...');
                analyzeBtn.click();

                showNotification(
                    `🤖 Auto-imported ${reports.length} reports and started analysis!`,
                    'success'
                );
            } else {
                showNotification(
                    `✅ Injected ${reports.length} reports. Click "Analyze & Add Submissions" to process.`,
                    'info'
                );
            }
        }, 500);
    });
}

/**
 * Wait for analytics app to be ready
 */
function waitForAnalyticsApp() {
    return new Promise((resolve) => {
        // Check if already ready
        if (isAnalyticsAppReady()) {
            resolve();
            return;
        }

        // Wait for app to initialize
        console.log('⏳ Waiting for Analytics App to initialize...');

        const checkInterval = setInterval(() => {
            if (isAnalyticsAppReady()) {
                console.log('✅ Analytics App ready');
                clearInterval(checkInterval);
                resolve();
            }
        }, 500);

        // Timeout after 30 seconds
        setTimeout(() => {
            clearInterval(checkInterval);
            console.warn('⚠️ Analytics App initialization timeout');
            resolve(); // Resolve anyway to avoid hanging
        }, 30000);
    });
}

/**
 * Show notification on the page
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');

    const colors = {
        success: '#10b981',
        error: '#ef4444',
        info: '#3b82f6',
        warning: '#f59e0b'
    };

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${colors[type] || colors.info};
        color: white;
        padding: 16px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        z-index: 999999;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        font-size: 14px;
        font-weight: 500;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;

    notification.textContent = message;

    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    document.body.appendChild(notification);

    // Remove after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Notify extension that analytics app is loaded
chrome.runtime.sendMessage({
    type: 'ANALYTICS_APP_LOADED',
    url: window.location.href
}, (response) => {
    console.log('✅ Notified extension that Analytics App is loaded');
});

console.log('✅ Analytics App Content Script ready');
