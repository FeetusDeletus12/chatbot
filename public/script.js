// /public/script.js

document.getElementById("submitButton").addEventListener("click", async () => {
    const userInput = document.getElementById("userInput").value;
    const responseContainer = document.getElementById("response");

    const response = await fetch('/api/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input: userInput }),
    });

    const data = await response.json();
    responseContainer.textContent = data.response || "No response from AI.";
});
