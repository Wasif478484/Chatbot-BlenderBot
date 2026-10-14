# BlenderBot Chatbot

ChatGPT-style web chatbot: Flask backend + facebook/blenderbot-400M-distill (Hugging Face Transformers).

## Setup
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt

## Run
    python src/app.py

Open http://127.0.0.1:5000. The first run downloads the model (about 1.5 GB).
