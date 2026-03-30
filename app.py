from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)
CORS(app)

# 🔥 LOAD BASIC BRAINS (lightweight)
text_brain = pipeline("text-generation", model="distilgpt2")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    result = text_brain(message, max_new_tokens=100)

    return jsonify({
        "reply": result[0]["generated_text"]
    })

@app.route("/")
def home():
    return "AI Brain Running 🚀"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
