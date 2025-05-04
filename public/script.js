// /public/script.js

document.getElementById("submitButton").addEventListener("click", async () => {
    const userInput = document.getElementById("userInput").value;
    const responseContainer = document.getElementById("response");
    const chatBox = document.getElementById("chatBox");

    if (userInput.trim() === "") {
        return; // Prevent empty input
    }

    // Add user message to the chat box
    chatBox.innerHTML += `<div class="user-message">You: ${userInput}</div>`;
    document.getElementById("userInput").value = ""; // Clear input box

    // Show loading message while waiting for AI response
    responseContainer.textContent = "AI is thinking...";

    try {
        // Send user input to backend (Vercel serverless function)
        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ input: userInput }),
        });

        const data = await response.json();

        // Display AI's response
        if (data.response) {
            chatBox.innerHTML += `<div class="ai-message">AI: ${data.response}</div>`;
        } else {
            chatBox.innerHTML += `<div class="ai-message">AI: No response.</div>`;
        }

        // Scroll to the bottom of the chat
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        console.error("Error:", error);
        chatBox.innerHTML += `<div class="ai-message">AI: Something went wrong.</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
