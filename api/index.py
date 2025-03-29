from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "Hello from Flask on Vercel!"})

@app.route("/chat", methods=["POST"])
def chat():
    return jsonify({"message": "Chat endpoint will go here"})
