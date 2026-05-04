async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");
    const message = inputField.value.trim();

    if (message === "") return;

    chatbox.innerHTML += `
        <div class="user-message">
            <span class="label">You</span>
            <div class="bubble">${message}</div>
        </div>
    `;

    inputField.value = "";
    inputField.focus();
    chatbox.scrollTop = chatbox.scrollHeight;

    // Typing indicator
    const typingId = "typing-" + Date.now();
    chatbox.innerHTML += `
        <div class="bot-message typing-indicator" id="${typingId}">
            <span class="label">Assistant</span>
            <div class="bubble"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>
        </div>
    `;
    chatbox.scrollTop = chatbox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        document.getElementById(typingId)?.remove();

        chatbox.innerHTML += `
            <div class="bot-message">
                <span class="label">Assistant</span>
                <div class="bubble">${data.response}</div>
            </div>
        `;

        chatbox.scrollTop = chatbox.scrollHeight;

    } catch (error) {
        document.getElementById(typingId)?.remove();
        chatbox.innerHTML += `
            <div class="error-message">System: Could not connect to the server.</div>
        `;
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("userInput");
    input.focus();
    input.addEventListener("keypress", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});