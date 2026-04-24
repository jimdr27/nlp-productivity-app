
async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");
    const message = inputField.value.trim();


    if (message === "") return; 

 
    chatbox.innerHTML += `
        <div style="text-align: right; margin: 10px; color: #0056b3;">
            <b>You:</b> ${message}
        </div>
    `;
    

    inputField.value = ""; 


    chatbox.scrollTop = chatbox.scrollHeight;

    try {
        
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message }) 
        });

        
        const data = await response.json();

        
        chatbox.innerHTML += `
            <div style="text-align: left; margin: 10px; color: #28a745;">
                <b>Assistant:</b> ${data.response}
            </div>
        `;
        
        
        chatbox.scrollTop = chatbox.scrollHeight;

    } catch (error) {
        console.error("Error communicating with server:", error);
        chatbox.innerHTML += `
            <div style="text-align: center; margin: 10px; color: red;">
                <i>System: Could not connect to the server.</i>
            </div>
        `;
    }
}


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("userInput").addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
});

