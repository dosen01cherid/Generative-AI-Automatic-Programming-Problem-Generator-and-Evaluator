/**
 * WhatsApp Analytics Extension - Content Script
 * Monitors WhatsApp Web messages and captures student progress reports
 */

console.log('🔧 WhatsApp Analytics Extension loaded');

// Configuration
const CONFIG = {
    BASE64_MIN_LENGTH: 100,
    BASE64_PATTERN: /[A-Za-z0-9+/]{100,}={0,2}/g,
    SCAN_INTERVAL: 2000, // Check every 2 seconds
    DEBOUNCE_DELAY: 500
};

// State
let processedMessages = new Set();
let isEnabled = true;
let capturedReports = [];

// Load settings from storage
chrome.storage.sync.get(['enabled', 'autoSend'], (result) => {
    isEnabled = result.enabled !== false; // Default to true
    console.log('📊 Extension enabled:', isEnabled);
});

// Listen for settings changes
chrome.storage.onChanged.addListener((changes, namespace) => {
    if (changes.enabled) {
        isEnabled = changes.enabled.newValue;
        console.log('📊 Extension enabled changed to:', isEnabled);
    }
});

/**
 * Extract base64 progress reports from message text
 */
function extractBase64Reports(messageText) {
    if (!messageText || messageText.length < CONFIG.BASE64_MIN_LENGTH) {
        return [];
    }

    const matches = messageText.match(CONFIG.BASE64_PATTERN);
    if (!matches) {
        return [];
    }

    return matches.filter(match => match.length >= CONFIG.BASE64_MIN_LENGTH);
}

/**
 * Extract phone number from chat header
 */
function extractPhoneFromChat() {
    // Try to get phone from chat header
    const headerSelectors = [
        '[data-testid="conversation-info-header"]',
        'header[data-testid="conversation-header"]',
        '._amid'
    ];

    for (const selector of headerSelectors) {
        const header = document.querySelector(selector);
        if (header) {
            const text = header.innerText || header.textContent;
            // Look for Indonesian phone patterns
            const phoneMatch = text.match(/(\+62\s?[\d\s-]{9,14}|0\d[\d\s-]{8,13})/);
            if (phoneMatch) {
                return normalizePhone(phoneMatch[1]);
            }
        }
    }

    return null;
}

/**
 * Normalize phone number to +62 format
 */
function normalizePhone(phone) {
    if (!phone) return '';

    // Remove all non-digit characters except +
    phone = phone.replace(/[^\d+]/g, '');

    // Convert Indonesian numbers to +62 format
    if (phone.startsWith('0')) {
        phone = '+62' + phone.substring(1);
    } else if (phone.startsWith('62') && !phone.startsWith('+')) {
        phone = '+' + phone;
    } else if (!phone.startsWith('+') && phone.length > 8) {
        phone = '+' + phone;
    }

    return phone;
}

/**
 * Extract sender name from message element
 */
function extractSenderName(messageElement) {
    // Look for sender name in message
    const nameSelectors = [
        '[data-testid="message-author"]',
        '._ahxt',
        '.copyable-text span[dir="auto"]'
    ];

    for (const selector of nameSelectors) {
        const nameEl = messageElement.querySelector(selector);
        if (nameEl && nameEl.textContent) {
            return nameEl.textContent.trim();
        }
    }

    return 'Unknown';
}

/**
 * Extract timestamp from message element
 */
function extractTimestamp(messageElement) {
    // Look for timestamp
    const timeSelectors = [
        '[data-testid="msg-meta"]',
        '._ahxt + span',
        '.copyable-text [data-testid="msg-meta"] span'
    ];

    for (const selector of timeSelectors) {
        const timeEl = messageElement.querySelector(selector);
        if (timeEl && timeEl.textContent) {
            return timeEl.textContent.trim();
        }
    }

    return new Date().toLocaleTimeString();
}

/**
 * Scan for new messages and extract progress reports
 */
function scanMessages() {
    if (!isEnabled) {
        return;
    }

    // Find all message elements
    const messageSelectors = [
        'div[data-testid="msg-container"]',
        '.message-in, .message-out',
        '._amk4, ._amk6'
    ];

    let messages = [];
    for (const selector of messageSelectors) {
        messages = document.querySelectorAll(selector);
        if (messages.length > 0) break;
    }

    let newReportsFound = 0;

    messages.forEach(messageEl => {
        try {
            // Get message text
            const textElements = messageEl.querySelectorAll('[data-testid="msg-text"], .copyable-text, ._akbu');

            textElements.forEach(textEl => {
                const messageText = textEl.textContent || textEl.innerText;

                if (!messageText) return;

                // Create unique ID for this message
                const messageId = messageText.substring(0, 50) + messageText.length;

                // Skip if already processed
                if (processedMessages.has(messageId)) {
                    return;
                }

                // Extract base64 reports
                const base64Reports = extractBase64Reports(messageText);

                if (base64Reports.length > 0) {
                    processedMessages.add(messageId);

                    const phone = extractPhoneFromChat();
                    const sender = extractSenderName(messageEl);
                    const timestamp = extractTimestamp(messageEl);

                    base64Reports.forEach(base64Data => {
                        const report = {
                            data: base64Data,
                            phone: phone || '',
                            sender: sender,
                            timestamp: timestamp,
                            capturedAt: new Date().toISOString(),
                            messageId: messageId
                        };

                        capturedReports.push(report);
                        newReportsFound++;

                        console.log('✅ Progress report captured:', {
                            sender: sender,
                            phone: phone,
                            dataLength: base64Data.length
                        });

                        // Send to background script
                        chrome.runtime.sendMessage({
                            type: 'REPORT_CAPTURED',
                            report: report
                        });
                    });
                }
            });
        } catch (error) {
            console.error('Error processing message:', error);
        }
    });

    if (newReportsFound > 0) {
        // Show notification
        chrome.runtime.sendMessage({
            type: 'SHOW_NOTIFICATION',
            count: newReportsFound
        });

        // Update badge
        chrome.runtime.sendMessage({
            type: 'UPDATE_BADGE',
            count: capturedReports.length
        });
    }
}

/**
 * Initialize observer to watch for new messages
 */
function initializeObserver() {
    // Find the chat container
    const chatSelectors = [
        '[data-testid="conversation-panel-messages"]',
        '#main',
        '._ajyl'
    ];

    let chatContainer = null;
    for (const selector of chatSelectors) {
        chatContainer = document.querySelector(selector);
        if (chatContainer) break;
    }

    if (!chatContainer) {
        console.log('⏳ Chat container not found, retrying...');
        setTimeout(initializeObserver, 2000);
        return;
    }

    console.log('✅ Chat container found, starting observer');

    // Initial scan
    scanMessages();

    // Set up periodic scanning
    setInterval(scanMessages, CONFIG.SCAN_INTERVAL);

    // Also observe DOM changes for immediate detection
    const observer = new MutationObserver(() => {
        scanMessages();
    });

    observer.observe(chatContainer, {
        childList: true,
        subtree: true
    });

    console.log('🔍 Message observer initialized');
}

/**
 * Listen for messages from popup/background
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'GET_REPORTS') {
        sendResponse({ reports: capturedReports });
    } else if (message.type === 'CLEAR_REPORTS') {
        capturedReports = [];
        processedMessages.clear();
        sendResponse({ success: true });
    } else if (message.type === 'EXPORT_TO_ANALYTICS') {
        // This will be handled by popup opening the analytics page
        sendResponse({ success: true });
    }
});

// Start monitoring when WhatsApp loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeObserver);
} else {
    // Wait a bit for WhatsApp to fully load
    setTimeout(initializeObserver, 3000);
}

console.log('🚀 WhatsApp Analytics Extension content script initialized');
