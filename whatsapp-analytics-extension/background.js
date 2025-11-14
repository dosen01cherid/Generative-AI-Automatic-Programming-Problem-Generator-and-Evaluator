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
        autoInjectMode: false,  // Auto-inject mode off by default
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

            // Check if auto-inject mode is enabled
            chrome.storage.sync.get(['autoInjectMode'], (result) => {
                if (result.autoInjectMode) {
                    console.log('🚀 Auto-inject mode enabled - triggering automatic injection');
                    // Automatically inject to analytics app
                    handleAutoInject(capturedReports, true, (response) => {
                        if (response && response.success) {
                            console.log('✅ Auto-injection completed successfully');
                        } else {
                            console.warn('⚠️ Auto-injection failed:', response ? response.error : 'Unknown error');
                        }
                    });
                }
            });
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

        case 'AUTO_INJECT_TO_ANALYTICS':
            // Automatically inject reports to analytics app
            handleAutoInject(message.reports, message.autoAnalyze, sendResponse);
            return true; // Keep channel open for async response

        case 'ANALYTICS_APP_LOADED':
            // Analytics app notified us it's loaded
            console.log('✅ Analytics App loaded:', message.url);
            sendResponse({ success: true });
            break;

        case 'FIND_ANALYTICS_TAB':
            // Find if analytics tab is open
            findAnalyticsTab(sendResponse);
            return true; // Keep channel open for async response

        case 'INJECT_TO_OPEN_ANALYTICS':
            // Inject to already open analytics app
            injectToOpenAnalytics(message.reports, sendResponse);
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
 * Find analytics app tab
 */
async function findAnalyticsTab(sendResponse) {
    try {
        const result = await chrome.storage.sync.get(['analyticsUrl']);
        const analyticsUrl = result.analyticsUrl || '';

        if (!analyticsUrl) {
            sendResponse({ success: false, error: 'Analytics URL not configured' });
            return;
        }

        // Get all tabs
        const tabs = await chrome.tabs.query({});

        // Find matching tab
        const analyticsTabs = tabs.filter(tab => {
            if (!tab.url) return false;

            // Check if URL matches
            if (tab.url === analyticsUrl) return true;

            // For file URLs, check filename match
            if (analyticsUrl.includes('analytics_for_problem.html') &&
                tab.url.includes('analytics_for_problem.html')) {
                return true;
            }

            // For localhost/IP, check path match
            if (tab.url.includes(analyticsUrl.split('?')[0])) {
                return true;
            }

            return false;
        });

        if (analyticsTabs.length > 0) {
            sendResponse({
                success: true,
                found: true,
                tabId: analyticsTabs[0].id,
                url: analyticsTabs[0].url
            });
        } else {
            sendResponse({ success: true, found: false });
        }
    } catch (error) {
        console.error('Error finding analytics tab:', error);
        sendResponse({ success: false, error: error.message });
    }
}

/**
 * Inject content script to analytics tab
 */
async function injectContentScriptToTab(tabId) {
    try {
        // First, check if content script is already injected
        try {
            const response = await chrome.tabs.sendMessage(tabId, { type: 'PING' });
            if (response && response.success) {
                console.log('✅ Content script already injected');
                return true;
            }
        } catch (e) {
            // Content script not injected yet, continue to inject
        }

        // Inject the content script
        await chrome.scripting.executeScript({
            target: { tabId: tabId },
            files: ['analytics-content.js']
        });

        console.log('✅ Content script injected into analytics tab');
        return true;
    } catch (error) {
        console.error('❌ Error injecting content script:', error);
        return false;
    }
}

/**
 * Inject reports to open analytics app
 */
async function injectToOpenAnalytics(reports, sendResponse) {
    try {
        // Find analytics tab
        const result = await chrome.storage.sync.get(['analyticsUrl']);
        const analyticsUrl = result.analyticsUrl || '';

        if (!analyticsUrl) {
            sendResponse({
                success: false,
                error: 'Analytics URL not configured'
            });
            return;
        }

        // Find the tab
        const tabs = await chrome.tabs.query({});
        const analyticsTab = tabs.find(tab => {
            if (!tab.url) return false;
            return tab.url === analyticsUrl ||
                   (tab.url.includes('analytics_for_problem.html') &&
                    analyticsUrl.includes('analytics_for_problem.html'));
        });

        if (!analyticsTab) {
            sendResponse({
                success: false,
                error: 'Analytics App not open. Please open it first.'
            });
            return;
        }

        // Inject content script if needed
        await injectContentScriptToTab(analyticsTab.id);

        // Wait a moment for content script to initialize
        await new Promise(resolve => setTimeout(resolve, 500));

        // Send reports to the tab
        chrome.tabs.sendMessage(
            analyticsTab.id,
            {
                type: 'INJECT_REPORTS',
                reports: reports
            },
            (response) => {
                if (chrome.runtime.lastError) {
                    console.error('Error sending to analytics:', chrome.runtime.lastError);
                    sendResponse({
                        success: false,
                        error: chrome.runtime.lastError.message
                    });
                } else {
                    console.log('✅ Reports injected to analytics app');
                    sendResponse({ success: true });
                }
            }
        );
    } catch (error) {
        console.error('Error injecting to analytics:', error);
        sendResponse({ success: false, error: error.message });
    }
}

/**
 * Handle auto-inject with optional auto-analyze
 */
async function handleAutoInject(reports, autoAnalyze, sendResponse) {
    try {
        const result = await chrome.storage.sync.get(['analyticsUrl']);
        const analyticsUrl = result.analyticsUrl || '';

        if (!analyticsUrl) {
            sendResponse({
                success: false,
                error: 'Analytics URL not configured'
            });
            return;
        }

        // Find if analytics is already open
        const tabs = await chrome.tabs.query({});
        let analyticsTab = tabs.find(tab => {
            if (!tab.url) return false;
            return tab.url === analyticsUrl ||
                   (tab.url.includes('analytics_for_problem.html') &&
                    analyticsUrl.includes('analytics_for_problem.html'));
        });

        // If not open, create new tab
        if (!analyticsTab) {
            analyticsTab = await chrome.tabs.create({ url: analyticsUrl });

            // Wait for page to load
            await new Promise((resolve) => {
                chrome.tabs.onUpdated.addListener(function listener(tabId, info) {
                    if (tabId === analyticsTab.id && info.status === 'complete') {
                        chrome.tabs.onUpdated.removeListener(listener);
                        resolve();
                    }
                });
            });

            // Additional wait for PyScript to initialize
            await new Promise(resolve => setTimeout(resolve, 3000));
        }

        // Inject content script
        await injectContentScriptToTab(analyticsTab.id);

        // Wait for content script to be ready
        await new Promise(resolve => setTimeout(resolve, 500));

        // Send reports
        const messageType = autoAnalyze ? 'AUTO_IMPORT' : 'INJECT_REPORTS';

        chrome.tabs.sendMessage(
            analyticsTab.id,
            {
                type: messageType,
                reports: reports
            },
            (response) => {
                if (chrome.runtime.lastError) {
                    console.error('Error:', chrome.runtime.lastError);
                    sendResponse({
                        success: false,
                        error: chrome.runtime.lastError.message
                    });
                } else {
                    console.log('✅ Auto-inject complete');
                    sendResponse({ success: true });
                }
            }
        );
    } catch (error) {
        console.error('Error in auto-inject:', error);
        sendResponse({ success: false, error: error.message });
    }
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
