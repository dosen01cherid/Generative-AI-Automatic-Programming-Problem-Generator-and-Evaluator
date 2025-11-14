/**
 * WhatsApp Analytics Extension - Background Service Worker
 * Handles storage, notifications, and communication between components
 */

console.log('🔧 Background service worker started');

// Storage for captured reports
let capturedReports = [];

// Initialize storage
chrome.runtime.onInstalled.addListener(() => {
    console.log('📦 Extension installed/updated');

    // Set default settings
    chrome.storage.sync.set({
        enabled: true,
        autoSend: false,
        analyticsUrl: ''
    });

    // Load any existing reports
    chrome.storage.local.get(['reports'], (result) => {
        if (result.reports) {
            capturedReports = result.reports;
            updateBadge();
        }
    });
});

/**
 * Update extension badge with report count
 */
function updateBadge() {
    const count = capturedReports.length;

    if (count > 0) {
        chrome.action.setBadgeText({ text: count.toString() });
        chrome.action.setBadgeBackgroundColor({ color: '#25D366' });
    } else {
        chrome.action.setBadgeText({ text: '' });
    }
}

/**
 * Save reports to storage
 */
function saveReports() {
    chrome.storage.local.set({ reports: capturedReports }, () => {
        console.log('💾 Reports saved to storage');
    });
}

/**
 * Show notification for new reports
 */
function showNotification(count) {
    chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: 'Progress Report Captured',
        message: `${count} new student progress ${count === 1 ? 'report' : 'reports'} captured!`,
        priority: 1
    });
}

/**
 * Handle messages from content script and popup
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log('📨 Message received:', message.type);

    switch (message.type) {
        case 'REPORT_CAPTURED':
            // Add new report
            capturedReports.push(message.report);
            saveReports();
            updateBadge();
            sendResponse({ success: true });
            break;

        case 'GET_ALL_REPORTS':
            // Send all reports to popup
            sendResponse({ reports: capturedReports });
            break;

        case 'CLEAR_REPORTS':
            // Clear all reports
            capturedReports = [];
            saveReports();
            updateBadge();
            sendResponse({ success: true });
            break;

        case 'DELETE_REPORT':
            // Delete specific report
            const index = message.index;
            if (index >= 0 && index < capturedReports.length) {
                capturedReports.splice(index, 1);
                saveReports();
                updateBadge();
                sendResponse({ success: true });
            } else {
                sendResponse({ success: false, error: 'Invalid index' });
            }
            break;

        case 'SHOW_NOTIFICATION':
            // Show notification
            showNotification(message.count);
            sendResponse({ success: true });
            break;

        case 'UPDATE_BADGE':
            // Update badge
            updateBadge();
            sendResponse({ success: true });
            break;

        case 'EXPORT_TO_ANALYTICS':
            // Export data to analytics app
            handleExportToAnalytics(message.reports, sendResponse);
            return true; // Keep channel open for async response

        default:
            console.warn('Unknown message type:', message.type);
            sendResponse({ success: false, error: 'Unknown message type' });
    }

    return true; // Keep message channel open
});

/**
 * Handle export to analytics app
 */
function handleExportToAnalytics(reports, sendResponse) {
    chrome.storage.sync.get(['analyticsUrl'], (result) => {
        const analyticsUrl = result.analyticsUrl || '';

        if (!analyticsUrl) {
            sendResponse({
                success: false,
                error: 'Please configure Analytics App URL in settings'
            });
            return;
        }

        // Prepare data for export
        const exportData = {
            reports: reports,
            exportedAt: new Date().toISOString(),
            source: 'whatsapp-extension'
        };

        // Open analytics page and send data
        chrome.tabs.create({ url: analyticsUrl }, (tab) => {
            // Wait for page to load, then send data
            chrome.tabs.onUpdated.addListener(function listener(tabId, info) {
                if (tabId === tab.id && info.status === 'complete') {
                    chrome.tabs.onUpdated.removeListener(listener);

                    // Send data to analytics page
                    chrome.tabs.sendMessage(tabId, {
                        type: 'IMPORT_REPORTS',
                        data: exportData
                    });
                }
            });

            sendResponse({ success: true });
        });
    });
}

/**
 * Load existing reports from storage on startup
 */
chrome.storage.local.get(['reports'], (result) => {
    if (result.reports) {
        capturedReports = result.reports;
        updateBadge();
        console.log(`📊 Loaded ${capturedReports.length} reports from storage`);
    }
});

console.log('✅ Background service worker initialized');
