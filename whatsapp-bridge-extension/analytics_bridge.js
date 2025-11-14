// Injected into analytics_for_problem.html - connects to WhatsApp via extension

console.log('📊 Analytics Bridge - Content Script loaded');

// Notify background that analytics is ready
chrome.runtime.sendMessage({ type: 'analytics_ready' }, (response) => {
    console.log('Analytics registered with background:', response);
});

// Create global WhatsApp interface for PyScript to use
window.WhatsAppBridge = {
    connected: false,

    async sendToChat(chatName, message) {
        console.log('📤 Sending to WhatsApp:', chatName, message);

        return new Promise((resolve) => {
            // First, find the chat
            chrome.runtime.sendMessage({
                type: 'send_to_whatsapp',
                data: {
                    action: 'find_chat',
                    chatName: chatName
                }
            }, (response) => {
                // Wait a bit for chat to open, then send message
                setTimeout(() => {
                    chrome.runtime.sendMessage({
                        type: 'send_to_whatsapp',
                        data: {
                            action: 'send_message',
                            message: message
                        }
                    }, (msgResponse) => {
                        resolve(msgResponse);
                    });
                }, 1500);
            });
        });
    },

    async getMessages(count = 10) {
        return new Promise((resolve) => {
            chrome.runtime.sendMessage({
                type: 'send_to_whatsapp',
                data: {
                    action: 'get_messages',
                    count: count
                }
            }, (response) => {
                resolve(response.messages || []);
            });
        });
    },

    startListening() {
        console.log('👂 Starting to listen for WhatsApp messages');
        chrome.runtime.sendMessage({
            type: 'send_to_whatsapp',
            data: {
                action: 'start_listening'
            }
        });
    },

    onMessage(callback) {
        // Store callback for incoming messages
        this.messageCallback = callback;
    }
};

// Listen for messages from WhatsApp (via background)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 Analytics received:', request.type);

    if (request.type === 'whatsapp_connected') {
        console.log('✅ WhatsApp Web is connected!');
        window.WhatsAppBridge.connected = true;

        // Notify PyScript
        if (window.dispatchEvent) {
            window.dispatchEvent(new CustomEvent('whatsapp-connected'));
        }

        sendResponse({ ok: true });
    }

    else if (request.type === 'whatsapp_disconnected') {
        console.log('❌ WhatsApp Web disconnected');
        window.WhatsAppBridge.connected = false;

        // Notify PyScript
        if (window.dispatchEvent) {
            window.dispatchEvent(new CustomEvent('whatsapp-disconnected'));
        }

        sendResponse({ ok: true });
    }

    else if (request.type === 'whatsapp_message') {
        console.log('📥 New message from WhatsApp:', request.message);

        // Call the callback if set
        if (window.WhatsAppBridge.messageCallback) {
            window.WhatsAppBridge.messageCallback(request.message, request.timestamp);
        }

        // Also dispatch event for PyScript
        if (window.dispatchEvent) {
            window.dispatchEvent(new CustomEvent('whatsapp-message', {
                detail: {
                    message: request.message,
                    timestamp: request.timestamp
                }
            }));
        }

        sendResponse({ ok: true });
    }

    return true;
});

// Add status indicator to page
const statusDiv = document.createElement('div');
statusDiv.id = 'whatsapp-status';
statusDiv.style.cssText = `
    position: fixed;
    top: 10px;
    right: 10px;
    background: #fee2e2;
    color: #991b1b;
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    z-index: 10000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
`;
statusDiv.textContent = '⚠️ WhatsApp Not Connected';
document.body.appendChild(statusDiv);

// Update status when connected
window.addEventListener('whatsapp-connected', () => {
    statusDiv.style.background = '#dcfce7';
    statusDiv.style.color = '#166534';
    statusDiv.textContent = '✅ WhatsApp Connected';
});

window.addEventListener('whatsapp-disconnected', () => {
    statusDiv.style.background = '#fee2e2';
    statusDiv.style.color = '#991b1b';
    statusDiv.textContent = '⚠️ WhatsApp Disconnected';
});

console.log('✅ Analytics Bridge ready - WhatsAppBridge available to PyScript');
