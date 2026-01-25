// Base URL of the FastAPI backend
const API_BASE_URL = '/api/v1';

// DOM elements for the simple chat UI
const youtubeUrlInput = document.getElementById('youtube-url');
const initBtn = document.getElementById('init-btn');
const statusMessage = document.getElementById('status-message');
const chatHistory = document.getElementById('chat-history');
const userMessageInput = document.getElementById('user-message');
const sendBtn = document.getElementById('send-btn');

// Tracks whether the backend has finished building the vector store
let isInitialized = false;
// Reference to the temporary "bot is typing" message
let loadingMessageEl = null;

/**
 * Update the small status banner under the URL input.
 * @param {string} message
 * @param {'success' | 'error' | 'loading' | ''} type
 */
function setStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status ${type}`;
}

/**
 * Append a chat message bubble to the chat history.
 * @param {string} text
 * @param {'user' | 'bot' | 'system' | 'error'} sender
 */
function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.textContent = text;
    chatHistory.appendChild(messageDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

/**
 * Call the /init endpoint to ingest a YouTube URL and build the vector store.
 */
async function initializeChat() {
    const url = youtubeUrlInput.value.trim();
    if (!url) {
        setStatus('Please enter a YouTube URL', 'error');
        return;
    }

    setStatus('Initializing knowledge base... This may take a moment.', 'loading');
    initBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/init`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });

        if (!response.ok) {
            throw new Error('Failed to initialize chat');
        }

        const data = await response.json();
        // Indicate that the backend is ready to answer questions
        setStatus(data.message || 'Ready to chat!', 'success');
        isInitialized = true;
        userMessageInput.disabled = false;
        sendBtn.disabled = false;

        // Clear previous chat
        chatHistory.innerHTML = '';
        appendMessage('Knowledge base initialized. You can now ask questions about the video.', 'system');

    } catch (error) {
        setStatus(`Error: ${error.message}`, 'error');
    } finally {
        initBtn.disabled = false;
    }
}

/**
 * Send the user message to the backend and render the bot answer.
 */
async function sendMessage() {
    if (!isInitialized) return;

    const text = userMessageInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user');
    userMessageInput.value = '';
    userMessageInput.disabled = true;
    sendBtn.disabled = true;

    // Show loading "bot is typing" message while we wait for the backend
    loadingMessageEl = document.createElement('div');
    loadingMessageEl.className = 'message bot loading';
    loadingMessageEl.textContent = 'Thinking...';
    chatHistory.appendChild(loadingMessageEl);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    try {
        const response = await fetch(`${API_BASE_URL}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: text }),
        });

        if (!response.ok) {
            throw new Error('Failed to send message');
        }

        const data = await response.json();

        console.log('API Response:', data);

        // Try to normalize different possible API response shapes to a string
        let botResponse = "I couldn't understand the response.";
        if (typeof data === 'string') {
            botResponse = data;
        } else if (data.answer) {
            botResponse = data.answer;
        } else if (data.response) {
            botResponse = data.response;
        } else if (data.content) {
            botResponse = data.content;
        } else {
            // Fallback: try to dump the object
            botResponse = JSON.stringify(data);
        }

        appendMessage(botResponse, 'bot');

    } catch (error) {
        appendMessage(`Error: ${error.message}`, 'error');
    } finally {
        // Remove loading message if it exists
        if (loadingMessageEl && loadingMessageEl.parentNode) {
            loadingMessageEl.parentNode.removeChild(loadingMessageEl);
        }
        loadingMessageEl = null;

        userMessageInput.disabled = false;
        sendBtn.disabled = false;
        userMessageInput.focus();
    }
}

initBtn.addEventListener('click', initializeChat);

sendBtn.addEventListener('click', sendMessage);

userMessageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});
