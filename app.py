from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = "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"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")
    brain = data.get("brain", "gpt")

    model_map = {
        "gpt": "openai/gpt-4o-mini",
        "claude": "anthropic/claude-3-haiku",
        "deepseek": "deepseek/deepseek-chat",
        "llama": "meta-llama/llama-3-8b-instruct",
        "mistral": "mistralai/mistral-7b-instruct"
    }

    model = model_map.get(brain)

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [{"role": "user", "content": message}]
        }
    )

    result = response.json()

    reply = result["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "AI BRAIN LIVE"

app.run(host="0.0.0.0", port=10000)
