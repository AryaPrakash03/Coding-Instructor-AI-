import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# --- Configuration ---
# Get the API key from the environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")

# Check if the API key is available
if not API_KEY:
    raise ValueError("No GEMINI_API_KEY found. Please set it as an environment variable.")

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    print(f"Error configuring Generative AI: {e}")

# --- Flask App Initialization ---
app = Flask(__name__)

# --- AI Model and Chat Initialization ---
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="You are a friendly and helpful coding instructor. Your name is 'Codey'. You only answer questions related to programming, software development, algorithms, and other computer science topics. If a user asks about something else, politely decline and state that you are a coding assistant."
)
chat = model.start_chat(history=[])

# --- Routes ---
@app.route("/")
def index():
    """Renders the main chat webpage."""
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    """Receives user message, sends it to the AI, and returns the response."""
    user_input = request.json.get("message")

    if not user_input:
        return jsonify({"error": "No message provided."}), 400

    try:
        response = chat.send_message(user_input)
        model_response = response.text
        return jsonify({"response": model_response})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An error occurred while communicating with the AI."}), 500

# --- Main Execution ---
if __name__ == "__main__":
    app.run(debug=True)