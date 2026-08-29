const chatLog = document.getElementById("chat-log");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");

const history = [];

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.textContent = text;
  chatLog.appendChild(div);
  chatLog.scrollTop = chatLog.scrollHeight;
  return div;
}

chatForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = chatInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  history.push({ role: "user", content: message });
  chatInput.value = "";

  const submitButton = chatForm.querySelector("button");
  submitButton.disabled = true;
  const pending = appendMessage("bot", "생각 중...");

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history }),
    });
    const data = await res.json();

    if (!res.ok) {
      pending.className = "message error";
      pending.textContent = data.error || "오류가 발생했습니다.";
      return;
    }

    pending.textContent = data.reply;
    history.push({ role: "assistant", content: data.reply });
  } catch (err) {
    pending.className = "message error";
    pending.textContent = "서버에 연결할 수 없습니다.";
  } finally {
    submitButton.disabled = false;
    chatInput.focus();
  }
});
