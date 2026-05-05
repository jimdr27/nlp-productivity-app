function escapeHTML(str) {
    return str.replace(/[&<>"']/g, function (match) {
        const escape = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return escape[match];
    });
}

function sanitizeResponse(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/&lt;br&gt;/g, "<br>");
}

function addMessage(type, text) {
    const chatbox = document.getElementById("chatbox");

    const html = `
        <div class="${type}-message">
            <span class="label">${type === "user" ? "You" : "Assistant"}</span>
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

        addMessage("bot", sanitizeResponse(data.response));

    } catch (error) {
        document.getElementById(typingId)?.remove();

        addMessage("bot", "⚠️ Could not connect to server.");
    }

    button.disabled = false;
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
});
