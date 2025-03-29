import os
import logging
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)

def configure_model():
    """Configure the generative AI model with the API key."""
    try:
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        logging.info("Model configured successfully.")
    except KeyError:
        logging.error("API key not found in environment variables.")
        raise

def start_chat_session():
    """Start a chat session with a predefined history."""
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    try:
        model = genai.GenerativeModel(
            model_name="tunedModels/tasnimdisha-sp48u93mq7rt",
            generation_config=generation_config,
        )

        history = [
            {"role": "user", "parts": ["Hi there, what are you doing today?"]},
            {"role": "model", "parts": ["I'm working on improving my SEO and content marketing skills to help businesses rank higher on search engines."]},
            {"role": "user", "parts": ["What is your name?"]},
            {"role": "model", "parts": ["My name is Tasnim Disha. I'm a digital marketer and SEO expert."]},
        ]
        
        return model.start_chat(history=history)
    except Exception as e:
        logging.error(f"Error starting chat session: {e}")
        raise

def send_user_message(chat_session, message):
    """Send a message to the chatbot and return the response."""
    try:
        response = chat_session.send_message(message)
        return response.text
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        return "Sorry, I couldn't process your request at the moment."

@app.route('/chat', methods=['POST'])
def chat():
    """Handle the chat request from the user."""
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    chat_session = start_chat_session()
    bot_response = send_user_message(chat_session, user_message)
    
    return jsonify({"response": bot_response})

@app.route('/')
def home():
    """Serve the front-end chat page."""
    return render_template("index.html")

if __name__ == "__main__":
    configure_model()
    app.run(debug=True)
