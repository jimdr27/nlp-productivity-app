function escapeHTML(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
}

function sanitizeResponse(str) {
    return escapeHTML(str)
        .replace(/\n/g, "<br>")
        .replace(/&lt;br&gt;/gi, "<br>");
}

function addMessage(type, text) {
    const chatbox = document.getElementById("chatbox");
    const safeText = type === "bot" ? sanitizeResponse(text) : escapeHTML(text);

    chatbox.insertAdjacentHTML("beforeend", `
        <div class="${type}-message">
            <div class="bubble">${safeText}</div>
        </div>
    `);

    chatbox.scrollTop = chatbox.scrollHeight;
}

async function loadTasks() {
    try {
        const res = await fetch("/api/tasks");
        const data = await res.json(); 
        const tasks = data.tasks; // <-- Extract the array from the JSON response!

        const taskList = document.getElementById("task-list");
        const taskCount = document.getElementById("task-count");

        taskCount.textContent = tasks.length;

        if (tasks.length === 0) {
            taskList.innerHTML = `<p class="empty-msg">No pending tasks</p>`;
            return;
        }

        taskList.innerHTML = tasks.map(task => {
            let dateHtml = "";
            if (task.due_date) {
                // Just use the clean string Python already formatted for us!
                dateHtml = `<span class="task-due">⏰ ${escapeHTML(task.due_date)}</span>`;
            }

            return `
                <div class="task-card">
                    <div class="task-info">
                        <span class="task-title">${escapeHTML(task.title)}</span>
                        ${dateHtml}
                    </div>
                    <div class="task-actions">
                        <button class="action-btn complete-btn" onclick="quickAction('complete task ${task.id}')">✓</button>
                        <button class="action-btn delete-btn" onclick="quickAction('delete task ${task.id}')">✕</button>
                    </div>
                </div>
            `;
        }).join("");

    } catch (error) {
        console.error("Could not load tasks", error);
    }
}

async function quickAction(message) {
    await sendMessage(message);
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
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        addMessage("bot", data.response);
        await loadTasks();  // refresh panel after every message

    } catch {
        addMessage("bot", "⚠️ Server error");
    }

    btn.disabled = false;
    btn.innerHTML = "Send";
    input.focus();
}

document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("userInput");
    const btn = document.getElementById("sendBtn");

    // Initial greeting
    addMessage("bot", "Hello! I'm your task assistant.<br><br>You can try:<br>• add buy groceries<br>• show tasks<br>• complete task 1<br>• delete task 2<br>• show tasks today");

    input.focus();

    input.addEventListener("keydown", e => {
        if (e.key === "Enter") sendMessage();
    });

    btn.addEventListener("click", sendMessage);

    document.getElementById("clearChat").onclick = () => {
        document.getElementById("chatbox").innerHTML = "";
        addMessage("bot", "Chat cleared! How can I help you?");
    };

    loadTasks();
});

