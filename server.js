// Load environment variables from .env file
require('dotenv').config();

const express = require('express');
const http = require('http');
const path = require('path');
const { WebSocketServer } = require('ws');
const { runSyncCycle } = require('./src/anchor/orchestrator');

const app = express();
const server = http.createServer(app);
const wss = new WebSocketServer({ server });

const PORT = process.env.PORT || 3000;

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// WebSocket connection handler
wss.on('connection', (ws) => {
  console.log('Client connected');

  ws.on('message', async (message) => {
    console.log(`Received message => ${message}`);

    // Check if the message is a command to start the anchor sync
    if (message.toString() === 'injectTask') {
      // Define a callback function to send logs back to the client
      const logCallback = (logMessage) => {
        if (ws.readyState === ws.OPEN) {
          ws.send(JSON.stringify({ type: 'log', data: logMessage }));
        }
      };

      try {
        await runSyncCycle(logCallback);
      } catch (error) {
        logCallback(`[ERROR] An unexpected error occurred: ${error.message}`);
        console.error(error);
      }
    }
  });

  ws.on('close', () => {
    console.log('Client disconnected');
  });

  ws.send(JSON.stringify({ type: 'log', data: 'Welcome to the Julius Oracle WebSocket server!' }));
});

server.listen(PORT, () => {
  console.log(`Server is listening on http://localhost:${PORT}`);
});
