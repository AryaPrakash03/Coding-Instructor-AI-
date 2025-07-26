document.addEventListener("DOMContentLoaded", () => {
    const messageInput = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");
    const chatWindow = document.getElementById("chat-window");

    // Function to add a message to the chat window
    function addMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);
        
        const p = document.createElement("p");
        p.innerText = message;
        messageElement.appendChild(p);
        
        chatWindow.appendChild(messageElement);
        // Scroll to the bottom of the chat window
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Function to send a message to the backend
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (message === "") return;

        // Display user's message
        addMessage(message, "user");
        messageInput.value = "";

        try {
            const response = await fetch("/send_message", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();
            // Display model's response
            addMessage(data.response, "model");
        } catch (error) {
            console.error("Error:", error);
            addMessage("Sorry, something went wrong. Please try again.", "model");
        }
    }

    // Event listeners
    sendBtn.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });
});