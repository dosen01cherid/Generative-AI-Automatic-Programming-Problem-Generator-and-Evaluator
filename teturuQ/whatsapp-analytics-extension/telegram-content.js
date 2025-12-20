/**
 * Telegram Analytics Extension - Content Script
 * Monitors Telegram Web messages and captures student progress reports
 */

console.log('🔧 Telegram Analytics Extension loaded');

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
    console.log('📊 Telegram Extension enabled:', isEnabled);
});

// Listen for settings changes
chrome.storage.onChanged.addListener((changes, namespace) => {
    if (changes.enabled) {
        isEnabled = changes.enabled.newValue;
        console.log('📊 Telegram Extension enabled changed to:', isEnabled);
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
 * Extract username from chat header
 */
function extractUsernameFromChat() {
    // Try to get username from chat header
    const headerSelectors = [
        '.chat-info .peer-title',
        '.TopBar .peer-title',
        '.ChatInfo .chat-title',
        '.Transition .peer-title'
    ];

    for (const selector of headerSelectors) {
        const header = document.querySelector(selector);
        if (header) {
            const username = header.innerText || header.textContent;
            if (username && username.trim()) {
                return username.trim();
            }
        }
    }

    return null;
}

/**
 * Extract phone number from message if present
 * Telegram messages might include phone in the message body
 */
function extractPhoneFromMessage(messageText) {
    // Look for phone number patterns
    const phonePattern = /Phone:\s*(\+?[\d\s-]{10,15})/i;
    const match = messageText.match(phonePattern);

    if (match) {
        return normalizePhone(match[1]);
    }

    // Try Indonesian phone patterns
    const indoPattern = /(\+62\s?[\d\s-]{9,14}|0\d[\d\s-]{8,13})/;
    const indoMatch = messageText.match(indoPattern);

    if (indoMatch) {
        return normalizePhone(indoMatch[1]);
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
    const nameSelectors = [
        '.message-title .peer-title',
        '.sender-name',
        '.Message .name',
        '[data-peer-id] .peer-title'
    ];

    for (const selector of nameSelectors) {
        const nameElement = messageElement.querySelector(selector);
        if (nameElement) {
            const name = nameElement.innerText || nameElement.textContent;
            if (name && name.trim()) {
                return name.trim();
            }
        }
    }

    return 'Unknown';
}

/**
 * Scan messages in current chat
 */
function scanMessages() {
    if (!isEnabled) {
        return;
    }

    try {
        // Telegram Web message selectors
        const messageSelectors = [
            '.messages-container .message',
            '.MessageList .Message',
            '.Transition .message',
            '[data-message-id]'
        ];

        let messages = [];
        for (const selector of messageSelectors) {
            messages = document.querySelectorAll(selector);
            if (messages.length > 0) {
                break;
            }
        }

        if (messages.length === 0) {
            return;
        }

        console.log(`📨 Scanning ${messages.length} Telegram messages...`);

        messages.forEach(messageElement => {
            try {
                // Get message ID to avoid duplicates
                const messageId = messageElement.getAttribute('data-message-id') ||
                                 messageElement.getAttribute('data-mid') ||
                                 messageElement.id;

                if (!messageId || processedMessages.has(messageId)) {
                    return;
                }

                // Get message text
                const textSelectors = [
                    '.text-content',
                    '.message-text',
                    '.Message .text',
                    '.message-content'
                ];

                let messageText = '';
                for (const selector of textSelectors) {
                    const textElement = messageElement.querySelector(selector);
                    if (textElement) {
                        messageText = textElement.innerText || textElement.textContent;
                        break;
                    }
                }

                if (!messageText) {
                    return;
                }

                // Look for base64 data
                const base64Reports = extractBase64Reports(messageText);

                if (base64Reports.length > 0) {
                    console.log('🎯 Found progress report in Telegram message!', messageId);

                    // Extract metadata
                    const username = extractUsernameFromChat() || 'Unknown User';
                    const senderName = extractSenderName(messageElement) || username;
                    const phone = extractPhoneFromMessage(messageText) || '';

                    base64Reports.forEach(base64Data => {
                        const report = {
                            data: base64Data,
                            phone: phone,
                            sender: senderName,
                            username: username,
                            timestamp: new Date().toISOString(),
                            platform: 'telegram',
                            messageId: messageId
                        };

                        // Send to background script
                        chrome.runtime.sendMessage({
                            type: 'REPORT_CAPTURED',
                            report: report,
                            platform: 'telegram'
                        }, (response) => {
                            if (response && response.success) {
                                console.log('✅ Report sent to background (Telegram)');
                                processedMessages.add(messageId);
                            }
                        });
                    });
                }
            } catch (err) {
                console.error('Error processing Telegram message:', err);
            }
        });

    } catch (error) {
        console.error('❌ Error scanning Telegram messages:', error);
    }
}

/**
 * Initialize observer for dynamic content
 */
function initObserver() {
    const observer = new MutationObserver((mutations) => {
        // Debounce the scan
        clearTimeout(window.telegramScanTimeout);
        window.telegramScanTimeout = setTimeout(scanMessages, CONFIG.DEBOUNCE_DELAY);
    });

    // Observe the messages container
    const containerSelectors = [
        '.messages-container',
        '.MessageList',
        '#telegram-content',
        '.Transition'
    ];

    for (const selector of containerSelectors) {
        const container = document.querySelector(selector);
        if (container) {
            observer.observe(container, {
                childList: true,
                subtree: true
            });
            console.log('👁️ Telegram observer initialized on:', selector);
            break;
        }
    }

    // Also scan periodically
    setInterval(scanMessages, CONFIG.SCAN_INTERVAL);
}

// Wait for page to load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(initObserver, 2000);
    });
} else {
    setTimeout(initObserver, 2000);
}

// Initial scan
setTimeout(scanMessages, 3000);

console.log('✅ Telegram Analytics content script ready');
