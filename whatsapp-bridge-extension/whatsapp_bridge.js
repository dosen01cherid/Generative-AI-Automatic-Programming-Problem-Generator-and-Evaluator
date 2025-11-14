// Injected into WhatsApp Web - controls WhatsApp from extension

console.log('📱 WhatsApp Bridge - Content Script loaded');

// Notify background that WhatsApp is ready
chrome.runtime.sendMessage({ type: 'whatsapp_ready' }, (response) => {
    console.log('WhatsApp registered with background:', response);
});

// WhatsApp Web controller
const WhatsAppController = {
    findChat(name) {
        console.log('🔍 Finding chat:', name);

        // Click search box
        const searchBox = document.querySelector('[data-testid="chat-list-search"]') ||
                         document.querySelector('input[title*="Search"]');

        if (searchBox) {
            searchBox.click();
            searchBox.value = name;

            // Trigger input event
            const event = new Event('input', { bubbles: true });
            searchBox.dispatchEvent(event);

            // Wait and click first result
            setTimeout(() => {
                const firstResult = document.querySelector('[data-testid="cell-frame-container"]');
                if (firstResult) {
                    firstResult.click();
                    console.log('✅ Chat selected:', name);
                }
            }, 500);

            return true;
        }
        return false;
    },

    sendMessage(text) {
        console.log('📤 Sending message:', text);

        // Find message input
        const messageBox = document.querySelector('[data-testid="conversation-compose-box-input"]') ||
                          document.querySelector('div[contenteditable="true"][data-tab="10"]');

        if (!messageBox) {
            console.error('❌ Message box not found');
            return false;
        }

        // Set message text
        messageBox.textContent = text;

        // Trigger input event
        const inputEvent = new Event('input', { bubbles: true });
        messageBox.dispatchEvent(inputEvent);

        // Find and click send button
        setTimeout(() => {
            const sendButton = document.querySelector('[data-testid="send"]') ||
                             document.querySelector('button[aria-label*="Send"]');

            if (sendButton) {
                sendButton.click();
                console.log('✅ Message sent');
                return true;
            } else {
                console.error('❌ Send button not found');
                return false;
            }
        }, 100);

        return true;
    },

    getLatestMessages(count = 10) {
        const messages = document.querySelectorAll('[data-testid="msg-container"]');
        const result = [];

        const start = Math.max(0, messages.length - count);
        for (let i = start; i < messages.length; i++) {
            const msgEl = messages[i];
            const textEl = msgEl.querySelector('.selectable-text');
            const timeEl = msgEl.querySelector('[data-testid="msg-meta"]');

            if (textEl) {
                result.push({
                    text: textEl.textContent,
                    time: timeEl ? timeEl.textContent : '',
                    incoming: msgEl.classList.contains('message-in')
                });
            }
        }

        return result;
    },

    listenForNewMessages(callback) {
        console.log('👂 Setting up message listener...');

        // Use MutationObserver to detect new messages
        const targetNode = document.querySelector('[data-testid="conversation-panel-messages"]') ||
                          document.querySelector('#main');

        if (!targetNode) {
            console.error('❌ Cannot find message container');
            return;
        }

        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeType === 1) {
                        // Check if it's a message
                        const msgContainer = node.querySelector('[data-testid="msg-container"]') ||
                                           (node.getAttribute('data-testid') === 'msg-container' ? node : null);

                        if (msgContainer) {
                            const textEl = msgContainer.querySelector('.selectable-text');
                            const isIncoming = msgContainer.classList.contains('message-in');

                            if (textEl && isIncoming) {
                                const messageText = textEl.textContent;
                                console.log('📥 New incoming message:', messageText);
                                callback(messageText);
                            }
                        }
                    }
                });
            });
        });

        observer.observe(targetNode, {
            childList: true,
            subtree: true
        });

        console.log('✅ Message listener active');
        return observer;
    }
};

// Listen for commands from analytics (via background)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 WhatsApp received command:', request.action);

    if (request.action === 'find_chat') {
        const success = WhatsAppController.findChat(request.chatName);
        sendResponse({ success });
    }

    else if (request.action === 'send_message') {
        const success = WhatsAppController.sendMessage(request.message);
        sendResponse({ success });
    }

    else if (request.action === 'get_messages') {
        const messages = WhatsAppController.getLatestMessages(request.count || 10);
        sendResponse({ messages });
    }

    else if (request.action === 'start_listening') {
        WhatsAppController.listenForNewMessages((message) => {
            // Forward message to analytics via background
            chrome.runtime.sendMessage({
                type: 'send_to_analytics',
                data: {
                    type: 'whatsapp_message',
                    message: message,
                    timestamp: Date.now()
                }
            });
        });
        sendResponse({ listening: true });
    }

    return true; // Keep channel open for async
});

console.log('✅ WhatsApp Bridge ready');
