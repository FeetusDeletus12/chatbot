async function sendPrompt() {
  const prompt = document.getElementById("prompt").value;
  const responseEl = document.getElementById("response");

  responseEl.textContent = "Thinking...";

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ prompt })
  });

  const data = await res.text();
  responseEl.textContent = data;
}
