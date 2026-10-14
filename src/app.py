import os

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

from chatbot import generate_response

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "blenderbot-chatbot-dev-secret")
CORS(app)


def get_user_message():
    data = request.get_json(silent=True)
    if isinstance(data, dict):
        for key in ("message", "msg", "text", "user_input", "input", "prompt"):
            if key in data and str(data[key]).strip():
                return str(data[key]).strip()
    for key in ("message", "msg", "text", "user_input", "input", "prompt"):
        value = request.form.get(key) or request.args.get(key)
        if value and str(value).strip():
            return str(value).strip()
    return ""


def chat_response():
    message = get_user_message()
    if not message:
        return jsonify({"error": "No message provided."}), 400

    history = session.get("history", [])
    reply = generate_response(message, history)

    history.append(f"User: {message}")
    history.append(f"Bot: {reply}")
    session["history"] = history[-12:]

    payload = {
        "reply": reply,
        "response": reply,
        "bot": reply,
        "text": reply,
        "message": reply,
        "history": session["history"],
    }
    return jsonify(payload)


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/chat")
@app.post("/predict")
@app.post("/send")
def chat():
    return chat_response()


@app.get("/chat")
def chat_get():
    return chat_response()


@app.post("/reset")
@app.post("/new")
@app.post("/clear")
@app.get("/reset")
def reset():
    session.pop("history", None)
    return jsonify({"status": "ok", "message": "Conversation cleared."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
