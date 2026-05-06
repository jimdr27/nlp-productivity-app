function escapeHTML(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function sanitizeResponse(str) {
    return escapeHTML(str).replace(/\n/g, "<br>");
}

function addMessage(type, text) {
    const chatbox = document.getElementById("chatbox");

    const safeText = type === "bot"
        ? sanitizeResponse(text)
        : escapeHTML(text);

    chatbox.insertAdjacentHTML("beforeend", `
        <div class="${type}-message">
            <div class="bubble">${safeText}</div>
        </div>
    `);

    chatbox.scrollTop = chatbox.scrollHeight;
}

function addTaskMessage(task) {
    const chatbox = document.getElementById("chatbox");

    chatbox.insertAdjacentHTML("beforeend", `
        <div class="bot-message">
            <div class="bubble">
                • ${escapeHTML(task.title)}
                <div class="message-actions">
                    <button onclick="sendMessage('complete task ${task.id}')" class="action-btn complete-btn">✓</button>
                    <button onclick="sendMessage('delete task ${task.id}')" class="action-btn delete-btn">✕</button>
                </div>
            </div>
        </div>
    `);

    chatbox.scrollTop = chatbox.scrollHeight;
}

async function sendMessage(forcedMessage = null) {
    const input = document.getElementById("userInput");
    const btn = document.getElementById("sendBtn");

    const message = forcedMessage || input.value.trim();
    if (!message) return;

    if (!forcedMessage) {
        addMessage("user", message);
        input.value = "";
    }

    btn.disabled = true;
    btn.innerHTML = "⏳";

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message})
        });

        const data = await res.json();

        addMessage("bot", data.response);

    } catch {
        addMessage("bot", "⚠️ Server error");
    }

    btn.disabled = false;
    btn.innerHTML = "Send";
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("userInput");
    const btn = document.getElementById("sendBtn");

    input.focus();

    input.addEventListener("keydown", e => {
        if (e.key === "Enter") sendMessage();
    });

    btn.addEventListener("click", sendMessage);

    document.getElementById("clearChat").onclick = () => {
        document.getElementById("chatbox").innerHTML = "";
    };
});
