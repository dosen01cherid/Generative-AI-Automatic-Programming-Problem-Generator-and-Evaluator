/**
 * WhatsApp Backend Server for Kahoot-like Quiz Game
 *
 * This Node.js server:
 * 1. Manages WhatsApp connection using whatsapp-web.js
 * 2. Sends questions to WhatsApp group
 * 3. Receives answers from students
 * 4. Broadcasts updates to frontend via WebSocket
 *
 * Usage:
 *   npm install whatsapp-web.js ws qrcode-terminal express cors
 *   node whatsapp_server.js
 */

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const WebSocket = require('ws');
const express = require('express');
const cors = require('cors');

// =========================================
// CONFIGURATION
// =========================================
const HTTP_PORT = 3000;
const WS_PORT = 3001;

// =========================================
// EXPRESS HTTP SERVER (for API endpoints)
// =========================================
const app = express();
app.use(cors());
app.use(express.json());

// Game state
const gameState = {
  status: 'waiting', // waiting, active, ended
  currentQuestion: 0,
  questions: [],
  targetGroupId: null, // WhatsApp group ID to send messages to
  players: new Map(), // phone -> player data
  currentAnswers: new Map() // phone -> answer for current question
};

// =========================================
// WHATSAPP CLIENT INITIALIZATION
// =========================================
console.log('🚀 Initializing WhatsApp client...');

const whatsappClient = new Client({
  authStrategy: new LocalAuth(),
  puppeteer: {
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  }
});

// WhatsApp events
whatsappClient.on('qr', (qr) => {
  console.log('\n📱 Scan this QR code with WhatsApp:');
  qrcode.generate(qr, { small: true });
  console.log('\nOr open WhatsApp Web and scan the QR code displayed above.\n');

  // Broadcast QR to all connected WebSocket clients
  broadcastToClients({
    type: 'qr_code',
    qr: qr
  });
});

whatsappClient.on('ready', () => {
  console.log('✅ WhatsApp client is ready!');

  broadcastToClients({
    type: 'whatsapp_connected',
    message: 'WhatsApp connected successfully'
  });
});

whatsappClient.on('authenticated', () => {
  console.log('🔐 WhatsApp authenticated');
});

whatsappClient.on('auth_failure', (msg) => {
  console.error('❌ WhatsApp authentication failed:', msg);
});

whatsappClient.on('disconnected', (reason) => {
  console.log('⚠️ WhatsApp disconnected:', reason);

  broadcastToClients({
    type: 'whatsapp_disconnected',
    reason: reason
  });
});

// Handle incoming messages
whatsappClient.on('message', async (message) => {
  // Only process messages when game is active
  if (gameState.status !== 'active') return;

  // Get sender info
  const sender = message.from;
  const contact = await message.getContact();
  const messageText = message.body.trim().toUpperCase();

  console.log(`📥 Message from ${contact.pushname || contact.number}: ${messageText}`);

  // Check if it's from the target group (if set)
  if (gameState.targetGroupId && message.from !== gameState.targetGroupId) {
    return; // Ignore messages from other chats
  }

  // Parse answer (expecting A, B, C, D, or 1, 2, 3, 4)
  const answerMatch = messageText.match(/^[ABCD1234]$/);
  if (!answerMatch) return; // Not a valid answer

  let answer = answerMatch[0];
  // Convert number to letter
  if (/[1234]/.test(answer)) {
    answer = String.fromCharCode(64 + parseInt(answer)); // 1->A, 2->B, etc
  }

  // Get or create player
  const playerPhone = contact.number;
  if (!gameState.players.has(playerPhone)) {
    gameState.players.set(playerPhone, {
      phone: playerPhone,
      name: contact.pushname || contact.number,
      score: 0,
      answered: 0,
      correct: 0,
      speeds: []
    });

    broadcastToClients({
      type: 'player_joined',
      phone: playerPhone,
      name: contact.pushname || contact.number
    });
  }

  // Check if already answered current question
  if (gameState.currentAnswers.has(playerPhone)) {
    console.log(`⚠️ ${contact.pushname} already answered this question`);
    return;
  }

  // Record answer
  const currentQ = gameState.questions[gameState.currentQuestion - 1];
  const isCorrect = answer === currentQ.correctAnswer;
  const answerTime = Date.now();
  const questionStartTime = gameState.questionStartTime || answerTime;
  const speed = (answerTime - questionStartTime) / 1000; // seconds

  gameState.currentAnswers.set(playerPhone, {
    answer,
    correct: isCorrect,
    speed,
    timestamp: answerTime
  });

  // Update player stats
  const player = gameState.players.get(playerPhone);
  player.answered++;
  player.speeds.push(speed);

  if (isCorrect) {
    player.correct++;
    // Points: 1000 base + speed bonus (max 500 points)
    const speedBonus = Math.max(0, 500 - Math.floor(speed * 10));
    player.score += 1000 + speedBonus;

    console.log(`✅ ${contact.pushname} answered correctly! (+${1000 + speedBonus} points)`);
  } else {
    console.log(`❌ ${contact.pushname} answered incorrectly`);
  }

  // Broadcast to frontend
  broadcastToClients({
    type: 'answer_received',
    phone: playerPhone,
    name: player.name,
    answer,
    correct: isCorrect,
    speed,
    score: player.score,
    totalAnswered: gameState.currentAnswers.size,
    totalPlayers: gameState.players.size
  });
});

// Initialize WhatsApp client
whatsappClient.initialize();

// =========================================
// WEBSOCKET SERVER (for real-time updates)
// =========================================
const wss = new WebSocket.Server({ port: WS_PORT });
const clients = new Set();

wss.on('connection', (ws) => {
  console.log('🔌 New WebSocket client connected');
  clients.add(ws);

  // Send current game state to new client
  ws.send(JSON.stringify({
    type: 'game_state',
    state: {
      status: gameState.status,
      currentQuestion: gameState.currentQuestion,
      players: Array.from(gameState.players.entries()).map(([phone, data]) => ({
        phone,
        ...data
      }))
    }
  }));

  ws.on('close', () => {
    console.log('🔌 WebSocket client disconnected');
    clients.delete(ws);
  });

  ws.on('error', (error) => {
    console.error('WebSocket error:', error);
    clients.delete(ws);
  });
});

function broadcastToClients(data) {
  const message = JSON.stringify(data);
  clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message);
    }
  });
}

console.log(`📡 WebSocket server listening on ws://localhost:${WS_PORT}`);

// =========================================
// HTTP API ENDPOINTS
// =========================================

// Health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    whatsapp: whatsappClient.info ? 'connected' : 'disconnected',
    game: gameState.status
  });
});

// Get game state
app.get('/api/game', (req, res) => {
  res.json({
    status: gameState.status,
    currentQuestion: gameState.currentQuestion,
    players: Array.from(gameState.players.entries()).map(([phone, data]) => ({
      phone,
      ...data
    })),
    totalAnswers: gameState.currentAnswers.size
  });
});

// Start game
app.post('/api/game/start', async (req, res) => {
  const { questions, groupId } = req.body;

  if (!questions || !Array.isArray(questions) || questions.length === 0) {
    return res.status(400).json({ error: 'Invalid questions array' });
  }

  gameState.status = 'active';
  gameState.currentQuestion = 1;
  gameState.questions = questions;
  gameState.targetGroupId = groupId || null;
  gameState.currentAnswers.clear();
  gameState.questionStartTime = Date.now();

  console.log('🎮 Game started!');

  // Send first question to WhatsApp
  if (gameState.targetGroupId) {
    await sendQuestionToWhatsApp(0);
  }

  broadcastToClients({
    type: 'game_started',
    currentQuestion: 1,
    totalQuestions: questions.length
  });

  res.json({ success: true, message: 'Game started' });
});

// Next question
app.post('/api/game/next', async (req, res) => {
  if (gameState.status !== 'active') {
    return res.status(400).json({ error: 'Game is not active' });
  }

  if (gameState.currentQuestion >= gameState.questions.length) {
    return res.status(400).json({ error: 'No more questions' });
  }

  gameState.currentQuestion++;
  gameState.currentAnswers.clear();
  gameState.questionStartTime = Date.now();

  console.log(`📝 Moving to question ${gameState.currentQuestion}`);

  // Send question to WhatsApp
  if (gameState.targetGroupId) {
    await sendQuestionToWhatsApp(gameState.currentQuestion - 1);
  }

  broadcastToClients({
    type: 'next_question',
    currentQuestion: gameState.currentQuestion
  });

  res.json({ success: true, currentQuestion: gameState.currentQuestion });
});

// End game
app.post('/api/game/end', async (req, res) => {
  gameState.status = 'ended';

  console.log('🏁 Game ended!');

  // Send results to WhatsApp
  if (gameState.targetGroupId) {
    await sendResultsToWhatsApp();
  }

  broadcastToClients({
    type: 'game_ended'
  });

  res.json({ success: true, message: 'Game ended' });
});

// Get WhatsApp groups
app.get('/api/whatsapp/groups', async (req, res) => {
  try {
    const chats = await whatsappClient.getChats();
    const groups = chats.filter(chat => chat.isGroup).map(group => ({
      id: group.id._serialized,
      name: group.name,
      participants: group.participants ? group.participants.length : 0
    }));

    res.json({ groups });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// =========================================
// WHATSAPP MESSAGE SENDING FUNCTIONS
// =========================================
async function sendQuestionToWhatsApp(index) {
  if (!gameState.targetGroupId) {
    console.log('⚠️ No target group set');
    return;
  }

  const question = gameState.questions[index];
  if (!question) return;

  const message = `
🎮 *Question ${index + 1}/${gameState.questions.length}*

${question.question}

${question.options.join('\n')}

Reply with A, B, C, or D to answer!
⏱️ Timer started!
  `.trim();

  try {
    await whatsappClient.sendMessage(gameState.targetGroupId, message);
    console.log('📤 Question sent to WhatsApp group');
  } catch (error) {
    console.error('❌ Error sending question:', error);
  }
}

async function sendResultsToWhatsApp() {
  if (!gameState.targetGroupId) return;

  // Sort players by score
  const playerArray = Array.from(gameState.players.values());
  playerArray.sort((a, b) => {
    if (b.score !== a.score) return b.score - a.score;
    return b.correct - a.correct;
  });

  let message = '🏆 *FINAL RESULTS* 🏆\n\n';

  playerArray.slice(0, 10).forEach((player, index) => {
    const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : `${index + 1}.`;
    const avgSpeed = player.speeds.length > 0
      ? (player.speeds.reduce((a, b) => a + b, 0) / player.speeds.length).toFixed(1)
      : '—';

    message += `${medal} *${player.name}*\n`;
    message += `   Score: ${player.score} | Correct: ${player.correct}/${player.answered} | Avg: ${avgSpeed}s\n\n`;
  });

  message += '\nThank you for playing! 🎉';

  try {
    await whatsappClient.sendMessage(gameState.targetGroupId, message);
    console.log('📤 Results sent to WhatsApp group');
  } catch (error) {
    console.error('❌ Error sending results:', error);
  }
}

// =========================================
// START HTTP SERVER
// =========================================
app.listen(HTTP_PORT, () => {
  console.log(`🌐 HTTP server listening on http://localhost:${HTTP_PORT}`);
  console.log('\nAvailable endpoints:');
  console.log(`  GET  /api/health - Check server status`);
  console.log(`  GET  /api/game - Get current game state`);
  console.log(`  POST /api/game/start - Start game`);
  console.log(`  POST /api/game/next - Next question`);
  console.log(`  POST /api/game/end - End game`);
  console.log(`  GET  /api/whatsapp/groups - List WhatsApp groups`);
  console.log('\nWebSocket server: ws://localhost:' + WS_PORT);
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n\n👋 Shutting down gracefully...');
  await whatsappClient.destroy();
  process.exit(0);
});
