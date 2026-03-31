import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///srishti.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init DB
db = SQLAlchemy(app)

# Enable CORS
CORS(app)

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.FileHandler("logs/srishti.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ======================
# SIMPLE MODEL (SAFE)
# ======================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))

# ======================
# ROUTES
# ======================

@app.route("/")
def home():
    return jsonify({
        "name": "Srishti AI",
        "status": "running"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "time": datetime.utcnow().isoformat()
    })

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    return jsonify({
        "reply": f"You said: {message}"
    })

# ======================
# ERROR HANDLING
# ======================

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500

# ======================
# RUN
# ======================

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
