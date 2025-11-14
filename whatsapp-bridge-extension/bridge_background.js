// Background script - bridges analytics page and WhatsApp Web

console.log('🌉 WhatsApp Analytics Bridge - Background Service Worker started');

// Store tab IDs
let analyticsTabId = null;
let whatsappTabId = null;

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 Background received:', request.type, 'from tab:', sender.tab?.id);

    // Register tabs
    if (request.type === 'analytics_ready') {
        analyticsTabId = sender.tab.id;
        console.log('✅ Analytics tab registered:', analyticsTabId);
        sendResponse({ registered: true });

        // Notify analytics if WhatsApp is already connected
        if (whatsappTabId) {
            chrome.tabs.sendMessage(analyticsTabId, {
                type: 'whatsapp_connected',
                tabId: whatsappTabId
            });
        }
    }

    else if (request.type === 'whatsapp_ready') {
        whatsappTabId = sender.tab.id;
        console.log('✅ WhatsApp tab registered:', whatsappTabId);
        sendResponse({ registered: true });

        // Notify analytics
        if (analyticsTabId) {
            chrome.tabs.sendMessage(analyticsTabId, {
                type: 'whatsapp_connected',
                tabId: whatsappTabId
            });
        }
    }

    // Forward messages from analytics to WhatsApp
    else if (request.type === 'send_to_whatsapp') {
        if (whatsappTabId) {
            chrome.tabs.sendMessage(whatsappTabId, request.data, (response) => {
                sendResponse(response);
            });
            return true; // Keep channel open for async response
        } else {
            sendResponse({ error: 'WhatsApp Web not open' });
        }
    }

    // Forward messages from WhatsApp to analytics
    else if (request.type === 'send_to_analytics') {
        if (analyticsTabId) {
            chrome.tabs.sendMessage(analyticsTabId, request.data, (response) => {
                sendResponse(response);
            });
            return true;
        } else {
            sendResponse({ error: 'Analytics page not open' });
        }
    }

    // Check connection status
    else if (request.type === 'check_connection') {
        sendResponse({
            analytics: !!analyticsTabId,
            whatsapp: !!whatsappTabId
        });
    }
});

// Clean up when tabs are closed
chrome.tabs.onRemoved.addListener((tabId) => {
    if (tabId === analyticsTabId) {
        console.log('Analytics tab closed');
        analyticsTabId = null;
    }
    if (tabId === whatsappTabId) {
        console.log('WhatsApp tab closed');
        whatsappTabId = null;
        // Notify analytics
        if (analyticsTabId) {
            chrome.tabs.sendMessage(analyticsTabId, {
                type: 'whatsapp_disconnected'
            });
        }
    }
});
