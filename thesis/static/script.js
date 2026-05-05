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
        .replace(/&lt;br&gt;/gi, '<br>')  // Restore intentional breaks
        .replace(/&lt;b&gt;/gi, '<b>')    // Allow bold tags
        .replace(/&lt;\/b&gt;/gi, '</b>'); // Allow closing bold tags
}

// Add interactive elements to bot messages
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
    chatbox.scrollTo({
        top: chatbox.scrollHeight,
        behavior: "smooth"
    });
}

async function completeTask(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}/complete`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            addMessage("bot", `✅ Task ${taskId} marked as complete!`);
        } else {
            addMessage("bot", "❌ Couldn't complete that task.");
        }
    } catch (error) {
        addMessage("bot", "⚠️ Network error.");
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            addMessage("bot", `🗑️ Task ${taskId} deleted.`);
        } else {
            addMessage("bot", "❌ Couldn't delete that task.");
        }
    } catch (error) {
        addMessage("bot", "⚠️ Network error.");
    }
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
    chatbox.scrollTo({
        top: chatbox.scrollHeight,
        behavior: "smooth"
    });
}

async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const button = document.getElementById("sendBtn");

    const message = inputField.value.trim();
    if (!message) return;

    button.disabled = true;
    button.textContent = '...';
    inputField.disabled = true;

    addMessage("user", escapeHTML(message));

    inputField.value = "";

    const typingId = "typing-" + Date.now();

    document.getElementById("chatbox").insertAdjacentHTML("beforeend", `
        <div class="bot-message typing-indicator" id="${typingId}">
            <span class="label">Assistant</span>
            <div class="bubble">Typing</div>
        </div>
    `);

     try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        await new Promise(r => setTimeout(r, 300));

        document.getElementById(typingId)?.remove();

        // Use enhanced message if task data exists
        if (data.task) {
            addBotMessageWithActions(data.response, data.task);
        } else {
            addMessage("bot", sanitizeResponse(data.response));
        }

    } catch (error) {
        document.getElementById(typingId)?.remove();

        addMessage("bot", "⚠️ Could not connect to server.");
    }

    button.disabled = false;
    button.textContent = 'Send';  // Restore
    inputField.disabled = false;
    inputField.focus();
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("userInput");
    const button = document.getElementById("sendBtn");

    // Initial bot message
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

    // Add keyboard shortcut for focusing input
    document.addEventListener("keydown", (e) => {
        // Press '/' to focus input (like Slack/Discord)
        if (e.key === '/' && document.activeElement !== input) {
            e.preventDefault();
            input.focus();
        }
        
        // Press 'Escape' to blur input
        if (e.key === 'Escape' && document.activeElement === input) {
            input.blur();
        }
    });


    document.getElementById("clearChat").addEventListener("click", () => {
        const chatbox = document.getElementById("chatbox");
        chatbox.innerHTML = '';
        addMessage("bot", "Chat cleared! How can I help you?");
    });

});
