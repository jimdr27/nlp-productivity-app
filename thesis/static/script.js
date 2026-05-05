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

async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");
    const button = document.getElementById("sendBtn");

    const message = inputField.value.trim();
    if (!message) return;

    // Disable button
    button.disabled = true;

    // Add user message
    chatbox.insertAdjacentHTML("beforeend", `
        <div class="user-message">
            <span class="label">You</span>
            <div class="bubble">${escapeHTML(message)}</div>
        </div>
    `);

    inputField.value = "";
    inputField.focus();
    chatbox.scrollTop = chatbox.scrollHeight;

    // Typing indicator
    const typingId = "typing-" + Date.now();

    chatbox.insertAdjacentHTML("beforeend", `
        <div class="bot-message typing-indicator" id="${typingId}">
            <span class="label">Assistant</span>
            <div class="bubble">Typing...</div>
        </div>
    `);

    chatbox.scrollTop = chatbox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Simulate thinking delay
        await new Promise(r => setTimeout(r, 300));

        document.getElementById(typingId)?.remove();

        chatbox.insertAdjacentHTML("beforeend", `
            <div class="bot-message">
                <span class="label">Assistant</span>
                <div class="bubble">${data.response}</div>
            </div>
        `);

    } catch (error) {
        document.getElementById(typingId)?.remove();

        chatbox.insertAdjacentHTML("beforeend", `
            <div class="error-message">System: Could not connect to the server.</div>
        `);
    }

    button.disabled = false;
    chatbox.scrollTop = chatbox.scrollHeight;
}

// Events
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("userInput");
    const button = document.getElementById("sendBtn");

    input.focus();

    input.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    button.addEventListener("click", sendMessage);
});
