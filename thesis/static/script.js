// This function triggers when the user clicks the "Send" button
async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const chatbox = document.getElementById("chatbox");
    const message = inputField.value.trim();

    // Prevent sending empty messages
    if (message === "") return; 

    // 1. Display the User's message in the chatbox
    chatbox.innerHTML += `
        <div style="text-align: right; margin: 10px; color: #0056b3;">
            <b>You:</b> ${message}
        </div>
    `;
    
    // Clear the input field for the next message
    inputField.value = ""; 

    // Auto-scroll to the bottom of the chatbox
    chatbox.scrollTop = chatbox.scrollHeight;

    try {
        // 2. Send the message to the Flask /chat route
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message }) // Convert JS object to JSON string
        });

        // Wait for Flask to send back the response
        const data = await response.json();

        // 3. Display the Bot's response in the chatbox
        chatbox.innerHTML += `
            <div style="text-align: left; margin: 10px; color: #28a745;">
                <b>Assistant:</b> ${data.response}
            </div>
        `;
        
        // Auto-scroll to the bottom again
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

// Bonus Quality-of-Life Feature: Send message on "Enter" key press
document.getElementById("userInput").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Prevent default form submission behavior
        sendMessage();
    }
});