# Browser-Based WhatsApp Automation with PyScript

## Concept: PyScript + WhatsApp Web in Browser

**User's Brilliant Idea:** Instead of backend server controlling WhatsApp Web, use PyScript (Python in browser) to interact directly with WhatsApp Web that user has already opened!

## ✅ Feasibility Analysis

**CAN THIS WORK?**
- ✅ **YES!** - If PyScript code runs on the same page as WhatsApp Web
- ❌ **NO** - If PyScript runs on different domain (blocked by CORS/same-origin policy)

## Three Viable Approaches

| Approach | Difficulty | Reliability | User Setup |
|----------|------------|-------------|------------|
| **1. Browser Extension** | Medium | ⭐⭐⭐⭐⭐ High | Install once |
| **2. Bookmarklet** | Easy | ⭐⭐⭐⭐ Good | Click bookmark |
| **3. Tampermonkey UserScript** | Easy | ⭐⭐⭐⭐ Good | Install script |

---

## Approach 1: Browser Extension (RECOMMENDED) ⭐

### Why Browser Extension?

- ✅ Can inject code into WhatsApp Web page
- ✅ Access to full DOM
- ✅ No same-origin restrictions
- ✅ Persistent across sessions
- ✅ Can communicate with other tabs

### Architecture

```
┌──────────────────────────────────┐
│   Tab 1: web.whatsapp.com        │
│   - Content Script (PyScript)    │
│   - Reads/Sends messages          │
│   - DOM manipulation              │
└────────────┬─────────────────────┘
             │ chrome.runtime.sendMessage
             ▼
┌──────────────────────────────────┐
│   Background Script              │
│   - Manages game state           │
│   - Coordinates messages         │
└────────────┬─────────────────────┘
             │ chrome.tabs.sendMessage
             ▼
┌──────────────────────────────────┐
│   Tab 2: kahoot_live.html        │
│   - Game UI & Leaderboard        │
│   - Control Panel                │
└──────────────────────────────────┘
```

### Implementation

**manifest.json** (Chrome Extension Manifest V3)

```json
{
  "manifest_version": 3,
  "name": "WhatsApp Quiz Game",
  "version": "1.0",
  "description": "Run Kahoot-like quiz games via WhatsApp",
  "permissions": [
    "tabs",
    "storage",
    "activeTab"
  ],
  "host_permissions": [
    "https://web.whatsapp.com/*"
  ],
  "background": {
    "service_worker": "background.js"
  },
  "content_scripts": [
    {
      "matches": ["https://web.whatsapp.com/*"],
      "js": [
        "pyscript_loader.js",
        "whatsapp_handler.js"
      ],
      "run_at": "document_idle"
    }
  ],
  "action": {
    "default_popup": "popup.html",
    "default_icon": {
      "16": "icon16.png",
      "48": "icon48.png",
      "128": "icon128.png"
    }
  },
  "web_accessible_resources": [
    {
      "resources": [
        "https://pyscript.net/releases/2024.1.1/core.css",
        "https://pyscript.net/releases/2024.1.1/core.js"
      ],
      "matches": ["https://web.whatsapp.com/*"]
    }
  ]
}
```

**pyscript_loader.js** (Load PyScript into WhatsApp Web)

```javascript
// Inject PyScript into WhatsApp Web page
(function() {
    console.log('🚀 Loading PyScript into WhatsApp Web...');

    // Add PyScript CSS
    const pyScriptCSS = document.createElement('link');
    pyScriptCSS.rel = 'stylesheet';
    pyScriptCSS.href = 'https://pyscript.net/releases/2024.1.1/core.css';
    document.head.appendChild(pyScriptCSS);

    // Add PyScript JavaScript
    const pyScriptJS = document.createElement('script');
    pyScriptJS.type = 'module';
    pyScriptJS.src = 'https://pyscript.net/releases/2024.1.1/core.js';
    document.head.appendChild(pyScriptJS);

    // Wait for PyScript to load, then inject Python code
    pyScriptJS.onload = function() {
        console.log('✅ PyScript loaded!');
        injectPythonCode();
    };
})();

function injectPythonCode() {
    // Create <script type="py"> tag
    const pyScript = document.createElement('script');
    pyScript.type = 'py';
    pyScript.textContent = `
# Python code running in WhatsApp Web!
from js import document, console, chrome
import json

console.log("🐍 Python is running in WhatsApp Web!")

class WhatsAppController:
    """Control WhatsApp Web from Python"""

    def __init__(self):
        self.current_chat = None
        console.log("WhatsApp Controller initialized")

    def find_chat(self, name):
        """Find chat by name"""
        # Find search box
        search_box = document.querySelector('[data-testid="search"]')
        if not search_box:
            search_box = document.querySelector('input[title="Search or start new chat"]')

        if search_box:
            search_box.click()
            search_box.value = name
            # Trigger input event
            evt = document.createEvent("HTMLEvents")
            evt.initEvent("input", True, True)
            search_box.dispatchEvent(evt)

            console.log(f"Searching for: {name}")
            return True
        return False

    def send_message(self, message):
        """Send message to current chat"""
        # Find message input box
        message_box = document.querySelector('[data-testid="conversation-compose-box-input"]')

        if not message_box:
            message_box = document.querySelector('div[contenteditable="true"][data-tab="10"]')

        if message_box:
            # Set message
            message_box.textContent = message

            # Trigger input event
            evt = document.createEvent("HTMLEvents")
            evt.initEvent("input", True, True)
            message_box.dispatchEvent(evt)

            # Find and click send button
            send_btn = document.querySelector('[data-testid="send"]')
            if send_btn:
                send_btn.click()
                console.log(f"✅ Sent: {message}")
                return True

        console.log("❌ Failed to send message")
        return False

    def get_latest_messages(self, count=10):
        """Get latest messages from current chat"""
        messages = document.querySelectorAll('[data-testid="msg-container"]')
        result = []

        for i in range(max(0, len(messages) - count), len(messages)):
            msg_el = messages[i]
            text_el = msg_el.querySelector('.selectable-text')
            if text_el:
                result.append(text_el.textContent)

        return result

    def listen_for_new_messages(self, callback):
        """Listen for new incoming messages"""
        # Use MutationObserver to detect new messages
        from js import MutationObserver

        def on_mutation(mutations, observer):
            for mutation in mutations:
                if mutation.type == "childList":
                    for node in mutation.addedNodes:
                        if node.nodeType == 1:  # Element node
                            # Check if it's a message
                            msg = node.querySelector('[data-testid="msg-container"]')
                            if msg:
                                text_el = msg.querySelector('.selectable-text')
                                if text_el:
                                    callback(text_el.textContent)

        # Observe message container
        target = document.querySelector('[data-testid="conversation-panel-messages"]')
        if target:
            observer = MutationObserver.new(on_mutation)
            config = {"childList": True, "subtree": True}
            observer.observe(target, config)
            console.log("👂 Listening for new messages...")

# Create global instance
wa_controller = WhatsAppController()

# Expose to JavaScript
from js import window
window.waController = wa_controller

console.log("✅ WhatsApp Controller ready!")

# Send message to extension background script
if hasattr(chrome, 'runtime'):
    chrome.runtime.sendMessage({
        "type": "python_ready",
        "message": "PyScript is ready in WhatsApp Web"
    })
`;

    document.body.appendChild(pyScript);
    console.log('✅ Python code injected!');
}
```

**whatsapp_handler.js** (Bridge between PyScript and Extension)

```javascript
// Listen for messages from extension popup/background
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('📨 Received message:', request);

    if (request.action === 'send_message') {
        // Call Python function via window object
        if (window.waController) {
            window.waController.find_chat(request.chat);

            setTimeout(() => {
                const success = window.waController.send_message(request.message);
                sendResponse({ success: success });
            }, 1000);

            return true; // Keep channel open for async response
        }
    }

    else if (request.action === 'get_messages') {
        if (window.waController) {
            const messages = window.waController.get_latest_messages(10);
            sendResponse({ messages: messages });
        }
    }

    else if (request.action === 'listen_answers') {
        if (window.waController) {
            window.waController.listen_for_new_messages((message) => {
                // Forward message to background script
                chrome.runtime.sendMessage({
                    type: 'new_message',
                    message: message,
                    timestamp: Date.now()
                });
            });
            sendResponse({ listening: true });
        }
    }
});

// Notify extension that content script is ready
chrome.runtime.sendMessage({
    type: 'content_script_ready',
    url: window.location.href
});
```

**background.js** (Extension Background Script - Game Logic)

```javascript
// Game state
const gameState = {
    status: 'waiting',
    currentQuestion: 0,
    questions: [],
    targetChat: '',
    players: new Map(),
    answers: new Map()
};

// Listen for messages from content scripts and popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    console.log('Background received:', request);

    if (request.type === 'python_ready') {
        console.log('✅ PyScript ready in WhatsApp Web');
        broadcastToPopup({ type: 'whatsapp_connected' });
    }

    else if (request.type === 'new_message') {
        // New message from WhatsApp
        handleWhatsAppMessage(request.message);
    }

    else if (request.action === 'start_game') {
        startGame(request.questions, request.chat);
        sendResponse({ started: true });
    }

    else if (request.action === 'next_question') {
        nextQuestion();
        sendResponse({ ok: true });
    }
});

function startGame(questions, chatName) {
    gameState.status = 'active';
    gameState.currentQuestion = 1;
    gameState.questions = questions;
    gameState.targetChat = chatName;
    gameState.answers.clear();

    // Send first question to WhatsApp
    sendQuestionToWhatsApp(0);

    // Start listening for answers
    sendToWhatsApp({
        action: 'listen_answers'
    });
}

function sendQuestionToWhatsApp(index) {
    const q = gameState.questions[index];

    const message = `
🎮 *Question ${index + 1}/${gameState.questions.length}*

${q.question}

${q.options.join('\\n')}

Reply with A, B, C, or D!
⏱️ Timer started!
    `.trim();

    sendToWhatsApp({
        action: 'send_message',
        chat: gameState.targetChat,
        message: message
    });
}

function sendToWhatsApp(message) {
    // Find WhatsApp Web tab
    chrome.tabs.query({ url: 'https://web.whatsapp.com/*' }, (tabs) => {
        if (tabs.length > 0) {
            chrome.tabs.sendMessage(tabs[0].id, message);
        }
    });
}

function handleWhatsAppMessage(message) {
    if (gameState.status !== 'active') return;

    // Parse answer (A, B, C, D)
    const answer = message.trim().toUpperCase();
    if (!/^[ABCD]$/.test(answer)) return;

    // Record answer
    const questionIndex = gameState.currentQuestion - 1;
    const q = gameState.questions[questionIndex];
    const isCorrect = answer === q.correctAnswer;

    // Broadcast to popup
    broadcastToPopup({
        type: 'answer_received',
        answer: answer,
        correct: isCorrect,
        message: message
    });
}

function broadcastToPopup(data) {
    // Send to all open popups/tabs
    chrome.runtime.sendMessage(data);
}
```

**popup.html** (Extension Popup - Control Panel)

```html
<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Quiz Control</title>
    <link rel="stylesheet" href="../shared_analytics_styles.css">
    <style>
        body {
            width: 400px;
            padding: 16px;
            font-family: sans-serif;
        }
        .status {
            padding: 8px;
            border-radius: 4px;
            margin-bottom: 12px;
            text-align: center;
            font-weight: 600;
        }
        .status.connected {
            background: #dcfce7;
            color: #166534;
        }
        .status.disconnected {
            background: #fee2e2;
            color: #991b1b;
        }
        input, button {
            width: 100%;
            padding: 8px;
            margin: 4px 0;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        button {
            background: #3b82f6;
            color: white;
            cursor: pointer;
            font-weight: 600;
        }
        button:hover {
            background: #2563eb;
        }
    </style>
</head>
<body>
    <h2>🎮 WhatsApp Quiz</h2>

    <div class="status disconnected" id="status">
        ⚠️ WhatsApp Web not connected
    </div>

    <div>
        <label>Chat Name / Group:</label>
        <input type="text" id="chatName" placeholder="Linear Algebra 08.00">
    </div>

    <div>
        <label>Question:</label>
        <textarea id="question" rows="3" placeholder="What is 2+2?" style="width:100%"></textarea>
    </div>

    <button id="btnSend">📤 Send Question</button>
    <button id="btnOpenGame" style="background:#10b981;">🎮 Open Game Dashboard</button>

    <hr>

    <div id="log" style="max-height: 200px; overflow-y: auto; font-size: 12px; background: #f9fafb; padding: 8px; border-radius: 4px;">
        <div style="color: #9ca3af;">Waiting for connection...</div>
    </div>

    <script src="popup.js"></script>
</body>
</html>
```

**popup.js** (Popup Logic)

```javascript
const statusEl = document.getElementById('status');
const logEl = document.getElementById('log');
const btnSend = document.getElementById('btnSend');
const btnOpenGame = document.getElementById('btnOpenGame');

// Check if WhatsApp Web is open
chrome.tabs.query({ url: 'https://web.whatsapp.com/*' }, (tabs) => {
    if (tabs.length > 0) {
        statusEl.className = 'status connected';
        statusEl.textContent = '✅ WhatsApp Web connected';
        log('Connected to WhatsApp Web');
    }
});

// Listen for messages
chrome.runtime.onMessage.addListener((request) => {
    if (request.type === 'whatsapp_connected') {
        statusEl.className = 'status connected';
        statusEl.textContent = '✅ PyScript ready!';
        log('PyScript initialized in WhatsApp Web');
    }

    else if (request.type === 'answer_received') {
        log(`📥 Answer: ${request.answer} ${request.correct ? '✓' : '✗'}`);
    }

    else if (request.type === 'new_message') {
        log(`💬 ${request.message}`);
    }
});

// Send question button
btnSend.addEventListener('click', () => {
    const chat = document.getElementById('chatName').value;
    const question = document.getElementById('question').value;

    if (!chat || !question) {
        alert('Please fill in chat name and question');
        return;
    }

    chrome.runtime.sendMessage({
        action: 'send_message',
        chat: chat,
        message: question
    }, (response) => {
        if (response && response.success) {
            log(`✅ Sent: ${question}`);
        } else {
            log(`❌ Failed to send`);
        }
    });
});

// Open game dashboard
btnOpenGame.addEventListener('click', () => {
    chrome.tabs.create({ url: 'kahoot_live.html' });
});

function log(message) {
    const div = document.createElement('div');
    div.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    div.style.borderBottom = '1px solid #e5e7eb';
    div.style.padding = '4px 0';
    logEl.appendChild(div);
    logEl.scrollTop = logEl.scrollHeight;
}
```

### Installation

1. **Save all files** in folder structure:
```
whatsapp-quiz-extension/
├── manifest.json
├── background.js
├── pyscript_loader.js
├── whatsapp_handler.js
├── popup.html
├── popup.js
├── icon16.png
├── icon48.png
└── icon128.png
```

2. **Load extension in Chrome:**
   - Open `chrome://extensions/`
   - Enable "Developer mode"
   - Click "Load unpacked"
   - Select `whatsapp-quiz-extension` folder

3. **Use the extension:**
   - Open WhatsApp Web in one tab
   - Click extension icon
   - Enter chat name and question
   - Click "Send Question"

---

## Approach 2: Bookmarklet (EASIEST FOR USERS)

### Concept

User drags a bookmark to their browser, then clicks it while on WhatsApp Web to inject PyScript.

### Implementation

**bookmarklet.js** (Minified for bookmark)

```javascript
javascript:(function(){
  var s=document.createElement('script');
  s.src='https://pyscript.net/releases/2024.1.1/core.js';
  s.type='module';
  document.head.appendChild(s);
  s.onload=function(){
    var p=document.createElement('script');
    p.type='py';
    p.text='from js import document,console\nconsole.log("PyScript loaded!");';
    document.body.appendChild(p);
  };
})();
```

**Full bookmarklet with WhatsApp controller:**

Create an HTML page for users to drag the bookmark:

**bookmarklet_page.html**

```html
<!DOCTYPE html>
<html>
<head>
    <title>WhatsApp Quiz Bookmarklet</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
        }
        .bookmark {
            display: inline-block;
            padding: 12px 24px;
            background: #3b82f6;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin: 20px 0;
        }
        .bookmark:hover {
            background: #2563eb;
        }
        pre {
            background: #f3f4f6;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>🎮 WhatsApp Quiz Bookmarklet</h1>

    <h2>Installation</h2>
    <p>Drag this button to your bookmarks bar:</p>

    <a href="javascript:(function(){var s=document.createElement('script');s.src='https://pyscript.net/releases/2024.1.1/core.js';s.type='module';document.head.appendChild(s);s.onload=function(){var p=document.createElement('script');p.type='py';p.text=`from js import document,console,window;class WA:;  def send(self,msg):;    box=document.querySelector('[data-testid=\"conversation-compose-box-input\"]');    if box:box.textContent=msg;box.dispatchEvent(document.createEvent('HTMLEvents'));window.send_btn=document.querySelector('[data-testid=\"send\"]');send_btn.click();console.log('Sent:'+msg);return True;return False;window.wa=WA();console.log('WhatsApp Controller ready!');`;document.body.appendChild(p);};})();" class="bookmark">
        📱 WhatsApp Quiz
    </a>

    <h2>Usage</h2>
    <ol>
        <li>Drag the button above to your bookmarks bar</li>
        <li>Open WhatsApp Web (web.whatsapp.com)</li>
        <li>Open a chat or group</li>
        <li>Click the bookmark</li>
        <li>Wait for "WhatsApp Controller ready!" in console (F12)</li>
        <li>Use in console: <code>wa.send("What is 2+2?")</code></li>
    </ol>

    <h2>How it works</h2>
    <p>The bookmarklet injects PyScript into WhatsApp Web, then loads Python code that can interact with the page.</p>

    <p><strong>Note:</strong> This is for educational purposes. WhatsApp may block accounts using automation.</p>
</body>
</html>
```

### Limitations of Bookmarklet

- ⚠️ User must click each time they want to use it
- ⚠️ PyScript takes 5-10 seconds to load
- ⚠️ Code is limited by bookmark URL length
- ✅ No installation required
- ✅ Works on any browser

---

## Approach 3: Tampermonkey UserScript

### Implementation

**whatsapp_quiz.user.js**

```javascript
// ==UserScript==
// @name         WhatsApp Quiz with PyScript
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Run quiz games via WhatsApp Web using PyScript
// @author       You
// @match        https://web.whatsapp.com/*
// @grant        none
// @run-at       document-idle
// ==/UserScript==

(function() {
    'use strict';

    console.log('🎮 WhatsApp Quiz UserScript loading...');

    // Inject PyScript
    const pyScriptCSS = document.createElement('link');
    pyScriptCSS.rel = 'stylesheet';
    pyScriptCSS.href = 'https://pyscript.net/releases/2024.1.1/core.css';
    document.head.appendChild(pyScriptCSS);

    const pyScriptJS = document.createElement('script');
    pyScriptJS.type = 'module';
    pyScriptJS.src = 'https://pyscript.net/releases/2024.1.1/core.js';
    document.head.appendChild(pyScriptJS);

    pyScriptJS.onload = function() {
        console.log('✅ PyScript loaded');

        // Inject Python code
        const pythonCode = document.createElement('script');
        pythonCode.type = 'py';
        pythonCode.textContent = `
from js import document, console, window
import json

console.log("🐍 Python running in WhatsApp Web!")

class QuizController:
    def __init__(self):
        self.questions = []
        self.current = 0
        self.answers = {}

    def send_message(self, text):
        """Send message in current chat"""
        box = document.querySelector('[data-testid="conversation-compose-box-input"]')
        if not box:
            return False

        box.textContent = text

        # Trigger events
        evt = document.createEvent("HTMLEvents")
        evt.initEvent("input", True, True)
        box.dispatchEvent(evt)

        # Click send
        send_btn = document.querySelector('[data-testid="send"]')
        if send_btn:
            send_btn.click()
            console.log(f"✅ Sent: {text}")
            return True
        return False

    def load_questions(self, questions_json):
        """Load quiz questions"""
        self.questions = json.loads(questions_json)
        console.log(f"Loaded {len(self.questions)} questions")

    def send_question(self, index):
        """Send question to chat"""
        if index >= len(self.questions):
            return False

        q = self.questions[index]
        msg = f"""
🎮 Question {index + 1}/{len(self.questions)}

{q['question']}

{chr(10).join(q['options'])}

Reply with A, B, C, or D!
        """.strip()

        self.send_message(msg)
        self.current = index
        return True

    def next_question(self):
        """Send next question"""
        return self.send_question(self.current + 1)

# Create global instance
quiz = QuizController()
window.quiz = quiz

console.log("✅ Quiz Controller ready! Use quiz.send_message('text')")

# Add UI button
button = document.createElement("button")
button.textContent = "🎮 Quiz"
button.style.cssText = "position:fixed;top:10px;right:10px;z-index:9999;padding:12px 20px;background:#3b82f6;color:white;border:none;border-radius:8px;cursor:pointer;font-weight:600;"
button.onclick = lambda e: console.log("Quiz button clicked!")
document.body.appendChild(button)
`;

        document.body.appendChild(pythonCode);
    };

    // Add control panel UI
    setTimeout(() => {
        addControlPanel();
    }, 5000);

    function addControlPanel() {
        const panel = document.createElement('div');
        panel.style.cssText = `
            position: fixed;
            top: 60px;
            right: 10px;
            width: 300px;
            background: white;
            border: 2px solid #3b82f6;
            border-radius: 12px;
            padding: 16px;
            z-index: 9998;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-family: sans-serif;
        `;

        panel.innerHTML = `
            <h3 style="margin:0 0 12px 0; color:#3b82f6;">🎮 Quiz Control</h3>
            <textarea id="quizQuestion" placeholder="Enter question..." style="width:100%; padding:8px; border:1px solid #ccc; border-radius:4px; margin-bottom:8px;"></textarea>
            <button id="sendQuiz" style="width:100%; padding:10px; background:#3b82f6; color:white; border:none; border-radius:6px; cursor:pointer; font-weight:600;">
                📤 Send Question
            </button>
            <div id="quizLog" style="margin-top:12px; max-height:150px; overflow-y:auto; font-size:12px; background:#f9fafb; padding:8px; border-radius:4px;">
                <div style="color:#9ca3af;">Ready...</div>
            </div>
        `;

        document.body.appendChild(panel);

        // Event listeners
        document.getElementById('sendQuiz').addEventListener('click', () => {
            const question = document.getElementById('quizQuestion').value;
            if (question && window.quiz) {
                window.quiz.send_message(question);
                log('Sent: ' + question);
                document.getElementById('quizQuestion').value = '';
            }
        });
    }

    function log(msg) {
        const logEl = document.getElementById('quizLog');
        if (logEl) {
            const div = document.createElement('div');
            div.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
            div.style.borderBottom = '1px solid #e5e7eb';
            div.style.padding = '4px 0';
            logEl.appendChild(div);
            logEl.scrollTop = logEl.scrollHeight;
        }
    }
})();
```

### Installation

1. Install Tampermonkey extension
2. Create new userscript
3. Paste code above
4. Save
5. Open WhatsApp Web
6. See control panel appear!

---

## Comparison Summary

| Feature | Extension | Bookmarklet | Tampermonkey |
|---------|-----------|-------------|--------------|
| **Setup** | Install once | Drag bookmark | Install script |
| **Persistence** | ✅ Always active | ❌ Click each time | ✅ Always active |
| **UI** | ✅ Popup panel | ❌ Console only | ✅ Injected panel |
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ (slow load) | ⭐⭐⭐⭐ |
| **Reliability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cross-tab** | ✅ Yes | ❌ No | ❌ No |

---

## Critical Limitations & Warnings

### ⚠️ WhatsApp Web Changes

WhatsApp Web frequently updates DOM structure. Selectors may break!

**Current selectors (as of 2024):**
- Search: `[data-testid="search"]`
- Message input: `[data-testid="conversation-compose-box-input"]`
- Send button: `[data-testid="send"]`
- Messages: `[data-testid="msg-container"]`

### ⚠️ Account Ban Risk

WhatsApp may detect automation and ban your account!

**Safer alternatives:**
- Use WhatsApp Cloud API (official, no risk)
- Test with secondary number
- Add delays between messages

### ⚠️ PyScript Load Time

PyScript takes 5-15 seconds to load initially.

**Solutions:**
- Show loading indicator
- Cache PyScript files
- Use service worker

---

## Recommended Approach

**For Production:** Browser Extension (most reliable)

**For Testing:** Tampermonkey (easiest to update)

**For Demo:** Bookmarklet (no installation)

---

## Next Steps

1. Choose approach (Extension recommended)
2. Implement code
3. Test with small group
4. Add error handling
5. Deploy to users

---

**Last Updated:** 2025-01-14
**Status:** ✅ Ready for implementation
**Recommended:** Browser Extension with PyScript
