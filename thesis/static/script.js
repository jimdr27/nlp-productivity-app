function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function sanitizeResponse(str) {
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;')
        .replace(/&lt;br&gt;/gi, '<br>')
        .replace(/&lt;b&gt;/gi, '<b>')
        .replace(/&lt;\/b&gt;/gi, '</b>');
}

// Buttons now send natural-language commands to /chat
function completeTask(taskId) {
    sendMessage(`complete task ${taskId}`);
}

function deleteTask(taskId) {
    sendMessage(`delete task ${taskId}`);
}

// Bot message with optional action buttons
function addBotMessageWithActions(text, taskData = null) {
    const chatbox = document.getElementById("chatbox");
    const messageId = 'msg-' + Date.now();

    let actionsHtml = '';
    if (taskData && taskData.id) {
        actionsHtml = `
            <div class="message-actions">
                <button onclick="completeTask(${taskData.id})" class="action-btn complete-btn">
                    ✓ Complete
                </button>
                <button onclick="deleteTask(${taskData.id})" class="action-btn delete-btn">
                    ✕ Delete
                </button>
            </div>
        `;
    }

    const html = `
        <div class="bot-message" id="${messageId}">
            <span class="label">Assistant</span>
            <div class="bubble">
                ${sanitizeResponse(text)}
                ${actionsHtml}
            </div>
        </div>
    `;

    chatbox.insertAdjacentHTML("beforeend", html);
    chatbox.scrollTo({ top: chatbox.scrollHeight, behavior: "smooth" });
}

function addMessage(type, text) {
    const chatbox = document.getElementById("chatbox");
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    const html = `
        <div class="${type}-message">
            <div class="message-header">
                <span class="label">${type === "user" ? "You" : "Assistant"}</span>
                <span class="timestamp">${time}</span>
            </div>
            <div class="bubble">${text}</div>
        </div>
    `;

    chatbox.insertAdjacentHTML("beforeend", html);
    chatbox.scrollTo({ top: chatbox.scrollHeight, behavior: "smooth" });
}

async function sendMessage(forcedMessage = null) {
    const inputField = document.getElementById("userInput");
    const button = document.getElementById("sendBtn");

    const message = forcedMessage || inputField.value.trim();
    if (!message) return;

    button.disabled = true;
    button.textContent = '...';
    inputField.disabled = true;

    if (!forcedMessage) {
        addMessage("user", escapeHTML(message));
        inputField.value = "";
    }

    const typingId = "typing-" + Date.now();
    document.getElementById("chatbox").insertAdjacentHTML("beforeend", `
        <div class="bot-message typing-indicator" id="${typingId}">
            <span class="label">Assistant</span>
            <div class="bubble">Typing</div>
        </div>
    `);

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        await new Promise(r => setTimeout(r, 300));
        document.getElementById(typingId)?.remove();

        // ✅ CORRECT PLACEMENT: Check the data after we actually fetch it!
        if (data.tasks && data.tasks.length > 0) {
            // 1. First, show the main text list of tasks
            addMessage("bot", sanitizeResponse(data.response)); 
            
            // 2. Then, create the actionable buttons for each task
            data.tasks.forEach(task => {
                addBotMessageWithActions(`Manage Task: ${task.title}`, task);
            });
        } else {
            // Standard text response
            addMessage("bot", sanitizeResponse(data.response));
        }

    } catch (error) {
        document.getElementById(typingId)?.remove();
        addMessage("bot", "⚠️ Could not connect to server.");
    }

    button.disabled = false;
    button.textContent = 'Send';
    inputField.disabled = false;
    inputField.focus();
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("userInput");
    const button = document.getElementById("sendBtn");

    addMessage("bot", `
        Hello! I'm your task assistant.<br><br>
        Try saying:<br>
        • add buy groceries<br>
        • show tasks<br>
        • complete task 1<br>
        • delete task 2
    `);

    input.focus();

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    button.addEventListener("click", sendMessage);

    document.addEventListener("keydown", (e) => {
        if (e.key === '/' && document.activeElement !== input) {
            e.preventDefault();
            input.focus();
        }
        if (e.key === 'Escape' && document.activeElement === input) {
            input.blur();
        }
    });

    document.getElementById("clearChat").addEventListener("click", () => {
        const chatbox = document.getElementById("chatbox");
        chatbox.innerHTML = '';
        addMessage("bot", "Chat cleared! How can I help you?");
    });

    // In script.js DOMContentLoaded, test connection
    async function testConnection() {
    try {
        await fetch("/api/test-nlp", {
            method: "POST",
            headers: { "Content-Type": "application/json" },  // add this
            body: JSON.stringify({ message: "test" })
        });
        document.getElementById("status-dot").style.background = "var(--accent)";
    } catch(e) {
        document.getElementById("status-dot").style.background = "#ff4757";
    }
}
    testConnection();

});
