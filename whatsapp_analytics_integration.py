# ADD THIS PYTHON CODE TO analytics_for_problem.html
# Place it in a <script type="py"> tag AFTER your existing PyScript code

from js import WhatsAppBridge, window, document, console
import asyncio

class WhatsAppQuizManager:
    """
    Manages WhatsApp quiz integration from analytics page.
    Uses browser extension bridge to send questions and receive answers.
    """

    def __init__(self, app):
        self.app = app
        self.current_question_index = 0
        self.questions = []
        self.target_chat = ""
        self.is_listening = False
        self.answer_mapping = {}  # Map student phones to answers

        # Listen for WhatsApp connection
        window.addEventListener("whatsapp-connected", self.on_whatsapp_connected)
        window.addEventListener("whatsapp-disconnected", self.on_whatsapp_disconnected)
        window.addEventListener("whatsapp-message", self.on_whatsapp_message)

        console.log("WhatsApp Quiz Manager initialized")

    def on_whatsapp_connected(self, event):
        """Called when WhatsApp Web connects"""
        console.log("✅ WhatsApp connected event received")
        self.update_status("WhatsApp Connected")

        # Add send question button if not exists
        self.add_whatsapp_controls()

    def on_whatsapp_disconnected(self, event):
        """Called when WhatsApp Web disconnects"""
        console.log("❌ WhatsApp disconnected")
        self.update_status("WhatsApp Disconnected")

    def on_whatsapp_message(self, event):
        """Called when new message arrives from WhatsApp"""
        message = event.detail.message
        timestamp = event.detail.timestamp

        console.log(f"📥 Received WhatsApp message: {message}")

        # Parse answer (A, B, C, D or 1, 2, 3, 4)
        answer = message.strip().upper()

        # Convert numbers to letters
        if answer in ["1", "2", "3", "4"]:
            answer = chr(64 + int(answer))  # 1->A, 2->B, etc.

        # Validate answer
        if answer not in ["A", "B", "C", "D"]:
            return  # Ignore non-answer messages

        # Process answer (you can get student phone from WhatsApp later)
        self.process_answer("unknown_phone", answer, timestamp)

    def add_whatsapp_controls(self):
        """Add WhatsApp control buttons to analytics UI"""
        # Check if already added
        if document.getElementById("whatsappControls"):
            return

        # Create control panel
        controls_html = """
        <div id="whatsappControls" class="panel" style="background: linear-gradient(135deg, #10b981, #059669); color: white; margin-bottom: 16px;">
            <h3 style="margin-top: 0; color: white;">📱 WhatsApp Quiz Control</h3>

            <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 12px; margin-bottom: 12px;">
                <input type="text" id="whatsappChatName" placeholder="Chat/Group Name (e.g., Linear Algebra 08.00)"
                       style="padding: 10px; border-radius: 6px; border: none;">
                <button id="btnTestWhatsApp" class="btn" style="background: white; color: #059669;">
                    🧪 Test Send
                </button>
            </div>

            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
                <button id="btnSendQuestion" class="btn" style="background: #1e40af; border: 2px solid white;">
                    📤 Send Question
                </button>
                <button id="btnNextQuestion" class="btn" style="background: #7c3aed; border: 2px solid white;">
                    ⏭️ Next Question
                </button>
                <button id="btnStartListening" class="btn" style="background: #dc2626; border: 2px solid white;">
                    👂 Start Listening
                </button>
            </div>

            <div id="whatsappLog" style="margin-top: 12px; background: rgba(255,255,255,0.2); padding: 12px; border-radius: 6px; max-height: 150px; overflow-y: auto; font-size: 12px;">
                <div style="color: rgba(255,255,255,0.9);">Ready to send questions...</div>
            </div>
        </div>
        """

        # Insert at top of analytics results
        results_div = document.getElementById("analyticsResults")
        if results_div:
            temp_div = document.createElement("div")
            temp_div.innerHTML = controls_html
            results_div.insertBefore(temp_div.firstChild, results_div.firstChild)

            # Attach event listeners
            document.getElementById("btnTestWhatsApp").addEventListener("click", self.test_whatsapp)
            document.getElementById("btnSendQuestion").addEventListener("click", self.send_current_question)
            document.getElementById("btnNextQuestion").addEventListener("click", self.next_question)
            document.getElementById("btnStartListening").addEventListener("click", self.start_listening)

    def test_whatsapp(self, event):
        """Test WhatsApp connection by sending a message"""
        chat_name = document.getElementById("whatsappChatName").value

        if not chat_name:
            window.alert("Please enter chat/group name")
            return

        self.target_chat = chat_name
        self.log_whatsapp("Testing connection...")

        # Send test message
        asyncio.ensure_future(self.send_to_whatsapp("🧪 Test message from Analytics!"))

    async def send_to_whatsapp(self, message):
        """Send message to WhatsApp using bridge"""
        try:
            if not WhatsAppBridge.connected:
                self.log_whatsapp("❌ WhatsApp not connected!")
                return False

            self.log_whatsapp(f"Sending: {message[:50]}...")

            # Use the bridge
            result = await WhatsAppBridge.sendToChat(self.target_chat, message)

            if result.get("success"):
                self.log_whatsapp("✅ Message sent!")
                return True
            else:
                self.log_whatsapp("❌ Failed to send")
                return False

        except Exception as e:
            console.error("Error sending to WhatsApp:", e)
            self.log_whatsapp(f"❌ Error: {str(e)}")
            return False

    def send_current_question(self, event):
        """Send current question to WhatsApp"""
        if not self.target_chat:
            chat_name = document.getElementById("whatsappChatName").value
            if not chat_name:
                window.alert("Please enter chat/group name")
                return
            self.target_chat = chat_name

        # Example question (you should customize this based on your quiz)
        question_text = f"""
🎮 *Question {self.current_question_index + 1}*

What is 2 + 2?

A. 3
B. 4
C. 5
D. 6

Reply with A, B, C, or D!
⏱️ Timer started!
""".strip()

        asyncio.ensure_future(self.send_to_whatsapp(question_text))

    def next_question(self, event):
        """Move to next question"""
        self.current_question_index += 1
        self.log_whatsapp(f"Moving to question {self.current_question_index + 1}")
        self.send_current_question(event)

    def start_listening(self, event):
        """Start listening for WhatsApp messages"""
        if self.is_listening:
            self.log_whatsapp("Already listening...")
            return

        WhatsAppBridge.startListening()
        self.is_listening = True
        self.log_whatsapp("👂 Listening for answers...")

        # Update button
        btn = document.getElementById("btnStartListening")
        btn.textContent = "✅ Listening..."
        btn.disabled = True

    def process_answer(self, phone, answer, timestamp):
        """Process incoming answer"""
        self.log_whatsapp(f"📥 Answer: {answer} from {phone}")

        # Here you can integrate with your existing analytics
        # For example, update player scores, leaderboard, etc.

        # Example: Add to answer mapping
        self.answer_mapping[phone] = {
            "answer": answer,
            "timestamp": timestamp,
            "question_index": self.current_question_index
        }

    def log_whatsapp(self, message):
        """Log message to WhatsApp log panel"""
        log_div = document.getElementById("whatsappLog")
        if log_div:
            import datetime
            time_str = datetime.datetime.now().strftime("%H:%M:%S")

            entry = document.createElement("div")
            entry.style.cssText = "border-bottom: 1px solid rgba(255,255,255,0.2); padding: 4px 0; color: rgba(255,255,255,0.95);"
            entry.textContent = f"[{time_str}] {message}"

            log_div.appendChild(entry)
            log_div.scrollTop = log_div.scrollHeight

    def update_status(self, message):
        """Update status display"""
        console.log(f"WhatsApp Status: {message}")
        # You can add UI status indicator here


# Initialize WhatsApp Quiz Manager
# Add this line after your analytics app is initialized
# whatsapp_quiz = WhatsAppQuizManager(app)
