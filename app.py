from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import sqlite3

app = Flask(__name__)

# ✅ FULL CORS FIX
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# ✅ DB SETUP
conn = sqlite3.connect("srishti.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT,
    response TEXT,
    timestamp TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT,
    timestamp TEXT
)
""")

conn.commit()

# 🔑 OPENROUTER KEY
OPENROUTER_API_KEY = "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"

# =========================
# BASIC ROUTES
# =========================

@app.route("/")
def home():
    return jsonify({"status": "Srishti AI Running"})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat()})

# =========================
# CHAT API (MAIN)
# =========================

@app.route("/api/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})

    data = request.json
    user_message = data.get("message", "")

    try:
        # 🔥 OPENROUTER CALL
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-chat",
                "messages": [
                    {"role": "user", "content": user_message}
                ]
            }
        )

        result = response.json()
        ai_reply = result["choices"][0]["message"]["content"]

    except Exception as e:
        ai_reply = str(e)

    # ✅ SAVE LOG
    cursor.execute("INSERT INTO messages (message, response, timestamp) VALUES (?, ?, ?)",
                   (user_message, ai_reply, datetime.utcnow().isoformat()))
    conn.commit()

    return jsonify({"reply": ai_reply})

# =========================
# IMAGE API
# =========================

@app.route("/api/image", methods=["POST"])
def image():
    prompt = request.json.get("prompt", "")

    # using Pollinations (free real image)
    image_url = f"https://image.pollinations.ai/prompt/{prompt}"

    return jsonify({"image_url": image_url})

# =========================
# AUDIO API (TTS BASIC)
# =========================

@app.route("/api/audio", methods=["POST"])
def audio():
    text = request.json.get("text", "")
    return jsonify({"audio": f"TTS not enabled yet: {text}"})

# =========================
# LOGS / ANALYTICS
# =========================

@app.route("/api/analytics")
def analytics():
    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]

    cursor
