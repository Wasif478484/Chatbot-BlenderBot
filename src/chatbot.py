import os
import threading

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL_NAME = "facebook/blenderbot-400M-distill"

print("Loading chatbot model. This may take a moment...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)
model.eval()
generation_lock = threading.Lock()
print(f"Chatbot ready on {device}.")


def build_prompt(message, history=None):
    history = list(history or [])[-6:]
    lines = history + [f"User: {message}"]
    return "\n".join(lines)


def generate_response(message, history=None):
    prompt = build_prompt(message, history)
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with generation_lock:
        with torch.no_grad():
            reply_ids = model.generate(
                **inputs,
                max_length=128,
                do_sample=True,
                top_p=0.9,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id,
            )
    reply = tokenizer.decode(reply_ids[0], skip_special_tokens=True)
    return reply.strip()


if __name__ == "__main__":
    conversation_history = []
    print("Chatbot ready! (type 'exit' to quit)\n")

    while True:
        conversation_history = conversation_history[-6:]
        history_string = "\n".join(conversation_history)

        input_text = input("> ")

        if input_text.lower() == "exit":
            break

        reply = generate_response(input_text, conversation_history)
        print("Bot:", reply)

        conversation_history.append(f"User: {input_text}")
        conversation_history.append(f"Bot: {reply}")
