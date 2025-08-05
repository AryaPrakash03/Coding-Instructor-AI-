document.addEventListener("DOMContentLoaded", () => {
    const messageInput = document.getElementById("message-input");
    const sendBtn = document.getElementById("send-btn");
    const chatWindow = document.getElementById("chat-window");
    const uploadBtn = document.getElementById("upload-btn"); // ### NEW ###
    const fileInput = document.getElementById("file-input"); // ### NEW ###

    // Function to add a message to the chat window
    function addMessage(message, sender) {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", `${sender}-message`);
        
        // Use innerHTML to render markdown-like formatting from the model
        const p = document.createElement("p");
        p.innerHTML = message; // Use innerHTML to correctly render newlines, etc.
        messageElement.appendChild(p);
        
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Function to send a text message to the backend
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (message === "") return;

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
            addMessage(data.response, "model");
        } catch (error) {
            console.error("Error:", error);
            addMessage("Sorry, something went wrong with the chat. Please try again.", "model");
        }
    }

    // ### NEW ### Function to upload a file and get a summary
    async function summarizeFile() {
        const file = fileInput.files[0];
        if (!file) return;

        addMessage(`Summarizing "${file.name}"...`, "user");

        const formData = new FormData();
        formData.append("file", file);

        // Add a temporary "thinking" message
        const thinkingMsg = document.createElement("div");
        thinkingMsg.classList.add("message", "model-message");
        thinkingMsg.innerHTML = "<p><i>Processing file...</i></p>";
        chatWindow.appendChild(thinkingMsg);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            const response = await fetch("/summarize", {
                method: "POST",
                body: formData, // No 'Content-Type' header needed; browser sets it for FormData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Network response was not ok");
            }

            const data = await response.json();
            // Replace "thinking" message with the actual response
            thinkingMsg.innerHTML = `<p>${data.response}</p>`;
        } catch (error) {
            console.error("Error:", error);
            // Replace "thinking" message with an error message
            thinkingMsg.innerHTML = `<p>Sorry, I couldn't summarize that file. Error: ${error.message}</p>`;
        } finally {
            // Reset file input to allow uploading the same file again
            fileInput.value = "";
        }
    }
    // ### END NEW ###

    // Event listeners
    sendBtn.addEventListener("click", sendMessage);
    messageInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendMessage();
        }
    });

    // ### NEW Event Listeners ###
    uploadBtn.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", summarizeFile);
    // ### END NEW ###
});