const messagesEl = document.getElementById("messages");
const typingEl = document.getElementById("typing");
const formEl = document.getElementById("chat-form");
const inputEl = document.getElementById("input");
const sendBtn = document.getElementById("send-btn");
const newChatBtn = document.getElementById("new-chat");

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

function addMessage(role, text) {
  const row = document.createElement("div");
  row.className = `message ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "U" : "B";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = escapeHtml(text).replace(/\n/g, "<br>");

  row.appendChild(avatar);
  row.appendChild(bubble);
  messagesEl.appendChild(row);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function setTyping(visible) {
  typingEl.classList.toggle("hidden", !visible);
  if (visible) {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }
}

function autoResize() {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 180) + "px";
}

async function sendMessage(text) {
  if (!text.trim()) return;
  addMessage("user", text);
  inputEl.value = "";
  autoResize();
  sendBtn.disabled = true;
  setTyping(true);

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    });

    if (!res.ok) {
      throw new Error(`Request failed (${res.status})`);
    }

    const data = await res.json();
    const reply = data.reply || data.response || data.bot || data.text || data.message || "";
    addMessage("assistant", reply || "I didn't get a reply.");
  } catch (err) {
    addMessage("assistant", `Error: ${err.message}`);
  } finally {
    setTyping(false);
    sendBtn.disabled = false;
    inputEl.focus();
  }
}

formEl.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(inputEl.value);
});

inputEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage(inputEl.value);
  }
});

inputEl.addEventListener("input", autoResize);

newChatBtn.addEventListener("click", async () => {
  try {
    await fetch("/reset", { method: "POST" });
  } catch (_) {}
  messagesEl.innerHTML = "";
  addMessage("assistant", "Hi! I'm BlenderBot. How can I help you today?");
});

// Welcome message
addMessage("assistant", "Hi! I'm BlenderBot. How can I help you today?");
