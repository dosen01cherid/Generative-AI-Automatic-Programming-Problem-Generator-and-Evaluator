# Kahoot-like WhatsApp Quiz Game Setup Guide

This system combines **browser-based frontend** (HTML/JavaScript) with **Node.js backend** for WhatsApp integration.

## 🏗️ Architecture

```
┌──────────────────────────────────────┐
│   Frontend (Browser)                 │
│   - kahoot_live.html                 │
│   - Game UI & Leaderboard            │
│   - Reuses analytics UI styling      │
└────────────┬─────────────────────────┘
             │ WebSocket (ws://localhost:3001)
             │ HTTP API (http://localhost:3000)
             ▼
┌──────────────────────────────────────┐
│   Backend (Node.js)                  │
│   - whatsapp_server.js               │
│   - WhatsApp connection management   │
│   - Answer processing                │
│   - Score calculation                │
└────────────┬─────────────────────────┘
             │ whatsapp-web.js
             ▼
┌──────────────────────────────────────┐
│   WhatsApp                           │
│   - Send questions to group          │
│   - Receive answers from students    │
│   - Send results                     │
└──────────────────────────────────────┘
```

## 📦 Installation

### Prerequisites
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **npm** (comes with Node.js)
- **WhatsApp** account with phone

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd /path/to/project

# Install Node.js packages
npm install
```

This will install:
- `whatsapp-web.js` - WhatsApp client library
- `ws` - WebSocket server
- `express` - HTTP server
- `cors` - Cross-origin resource sharing
- `qrcode-terminal` - Display QR codes in terminal

### Step 2: Start the Backend Server

```bash
# Start the WhatsApp backend server
npm start

# Or for development with auto-reload:
npm run dev
```

You should see:
```
🚀 Initializing WhatsApp client...
📡 WebSocket server listening on ws://localhost:3001
🌐 HTTP server listening on http://localhost:3000

📱 Scan this QR code with WhatsApp:
[QR CODE appears here]
```

### Step 3: Connect WhatsApp

1. Open WhatsApp on your phone
2. Go to **Settings** → **Linked Devices**
3. Tap **Link a Device**
4. Scan the QR code shown in terminal

Once connected, you'll see:
```
✅ WhatsApp client is ready!
```

### Step 4: Open the Frontend

Open `kahoot_live.html` in your browser:

```bash
# Option 1: Direct file
open kahoot_live.html

# Option 2: Local server (recommended)
python3 -m http.server 8000
# Then visit: http://localhost:8000/kahoot_live.html
```

## 🎮 How to Use

### For Teachers (Game Host):

1. **Connect WhatsApp**
   - Click "📱 Connect WhatsApp" button
   - Wait for connection status to show "WhatsApp Connected"

2. **Select WhatsApp Group** (via API or manually set in code)
   ```javascript
   // In browser console or code:
   fetch('http://localhost:3000/api/whatsapp/groups')
     .then(r => r.json())
     .then(data => console.log(data.groups));
   ```

3. **Start Game**
   - Click "▶️ Start Game"
   - First question automatically sent to WhatsApp group
   - Watch real-time answers come in!

4. **Next Question**
   - Click "⏭️ Next Question" when ready
   - New question sent to WhatsApp
   - Previous scores preserved

5. **End Game**
   - Click "⏹️ End Game"
   - Final results sent to WhatsApp group
   - Leaderboard frozen

### For Students:

1. **Join the WhatsApp group** that teacher is using

2. **Wait for question** - Teacher sends from the web interface

3. **Reply with answer** - Simply type:
   - `A`, `B`, `C`, or `D`
   - Or `1`, `2`, `3`, or `4`

4. **See results** - Final leaderboard sent to group at end

## 🔧 Configuration

### Change Ports

Edit `whatsapp_server.js`:

```javascript
const HTTP_PORT = 3000;  // HTTP API port
const WS_PORT = 3001;    // WebSocket port
```

### Customize Scoring

In `whatsapp_server.js`, find the scoring logic:

```javascript
// Points: 1000 base + speed bonus (max 500 points)
const speedBonus = Math.max(0, 500 - Math.floor(speed * 10));
player.score += 1000 + speedBonus;
```

Adjust values as needed:
- Base points per correct answer: `1000`
- Speed bonus: `500 - Math.floor(speed * 10)`
  - Answer in 1 sec = +490 bonus
  - Answer in 10 sec = +400 bonus
  - Answer in 50+ sec = +0 bonus

### Set Target WhatsApp Group

#### Method 1: Via API

```javascript
// Get list of groups
fetch('http://localhost:3000/api/whatsapp/groups')
  .then(r => r.json())
  .then(data => {
    console.log('Available groups:', data.groups);
    // Pick one and use its ID when starting game
  });

// Start game with specific group
fetch('http://localhost:3000/api/game/start', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    groupId: '123456789-1234567890@g.us',  // Group ID from above
    questions: [...] // Your questions
  })
});
```

#### Method 2: Hardcode in server

In `whatsapp_server.js`:

```javascript
gameState.targetGroupId = '123456789-1234567890@g.us';
```

## 📊 API Endpoints

### HTTP API (Port 3000)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Check server status |
| GET | `/api/game` | Get current game state |
| POST | `/api/game/start` | Start new game |
| POST | `/api/game/next` | Move to next question |
| POST | `/api/game/end` | End current game |
| GET | `/api/whatsapp/groups` | List all WhatsApp groups |

### WebSocket (Port 3001)

Connect to `ws://localhost:3001` to receive real-time updates:

**Server → Client Messages:**
- `qr_code` - QR code for WhatsApp login
- `whatsapp_connected` - WhatsApp ready
- `whatsapp_disconnected` - WhatsApp disconnected
- `game_started` - Game has started
- `next_question` - New question available
- `game_ended` - Game finished
- `player_joined` - New player joined
- `answer_received` - Student answered question

## 🎨 UI Customization

The frontend reuses the analytics UI styling from `shared_analytics_styles.css`.

### Modify Colors

Edit `kahoot_live.html` or add to your own CSS file:

```css
/* Change header gradient */
header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Change button colors */
.control-btn-start {
  background: #10b981; /* Green */
}
```

### Modify Leaderboard

In `kahoot_live.html`, find the `updateLeaderboard()` function:

```javascript
function updateLeaderboard() {
  // Sort players by score, correct answers, and speed
  playerArray.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    if (b.correct !== a.correct) return b.correct - a.correct;
    return (a.avgSpeed || 999) - (b.avgSpeed || 999);
  });
  // ... render table
}
```

## 🐛 Troubleshooting

### "WhatsApp authentication failed"

**Solution:** Delete the `.wwebjs_auth` folder and restart:
```bash
rm -rf .wwebjs_auth
npm start
```
Then scan QR code again.

### "Cannot connect to WebSocket"

**Check:**
1. Backend server is running: `http://localhost:3000/api/health`
2. WebSocket port not blocked by firewall
3. Correct WebSocket URL in `kahoot_live.html`:
   ```javascript
   const ws = new WebSocket('ws://localhost:3001');
   ```

### "Questions not sending to WhatsApp"

**Check:**
1. WhatsApp is connected (green dot in UI)
2. Target group ID is set correctly
3. Check server logs for errors
4. Verify group exists: `/api/whatsapp/groups`

### Players not being recognized

**Check:**
1. Game status is "active"
2. Students are in the correct WhatsApp group
3. Students reply with valid answers (A, B, C, D or 1, 2, 3, 4)
4. Check server logs to see received messages

## 📁 File Structure

```
project/
├── kahoot_live.html           # Frontend (browser UI)
├── shared_analytics_styles.css  # Shared CSS from analytics
├── whatsapp_server.js         # Backend (Node.js + WhatsApp)
├── package.json               # Node.js dependencies
├── KAHOOT_SETUP.md           # This file
│
├── .wwebjs_auth/             # WhatsApp session (auto-created)
│   └── session/              # Don't delete this while running
│
└── node_modules/             # Installed packages (auto-created)
```

## 🚀 Production Deployment

### For Local Network Use:

1. **Find your local IP:**
   ```bash
   # Linux/Mac
   ifconfig | grep "inet "

   # Windows
   ipconfig
   ```

2. **Update WebSocket URL** in `kahoot_live.html`:
   ```javascript
   const ws = new WebSocket('ws://192.168.1.100:3001');
   //                              ↑ Your local IP
   ```

3. **Allow firewall access** to ports 3000 and 3001

4. **Access from other devices:**
   ```
   http://192.168.1.100:3000/kahoot_live.html
   ```

### For Cloud Deployment:

Use services like:
- **DigitalOcean** - $5/month droplet
- **AWS EC2** - Free tier available
- **Heroku** - Free tier (with limitations)
- **Railway** - Easy deployment

**Note:** WhatsApp Web sessions expire after ~2 weeks of inactivity. You'll need to rescan QR code.

## 🎯 Next Steps

1. ✅ Test with sample data (built-in demo mode)
2. ✅ Connect to real WhatsApp account
3. ✅ Create question bank
4. ✅ Test with small group
5. 📚 Add question import from file
6. 📊 Add export results to CSV
7. 🔔 Add sound effects for answers
8. 📱 Add QR code display in web UI

## 💡 Tips

- **Test first** without WhatsApp by using the demo mode in UI
- **Prepare questions** in advance (JSON format)
- **Have backup plan** if WhatsApp disconnects mid-game
- **Limit group size** to ~50 students for best performance
- **Close other Chrome/Chromium** instances to avoid conflicts

## 📞 Support

If you need help:
1. Check server console logs for errors
2. Check browser console (F12) for frontend errors
3. Verify all files are in correct locations
4. Ensure Node.js version is 16+

---

**Happy Quizzing! 🎉**
