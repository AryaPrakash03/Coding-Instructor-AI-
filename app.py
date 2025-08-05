import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import pdfplumber
from PIL import Image
from werkzeug.utils import secure_filename
import io
# ### THE DEFINITIVE FIX: Import the correct exceptions module ###
from google.api_core import exceptions

# --- Configuration ---
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("No GEMINI_API_KEY found. Please set it as an environment variable.")
genai.configure(api_key=API_KEY)

# --- App Initialization ---
app = Flask(__name__)
model = genai.GenerativeModel('gemini-1.5-flash')
coding_chat = model.start_chat(history=[])

# --- Helper Function ---
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Context Storage ---
user_context = { "document_content": None, "chat_history": [] }

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.json.get("message")
    if not user_input: return jsonify({"error": "No message provided."}), 400

    if user_input.strip().lower() == '/new':
        user_context.update({"document_content": None, "chat_history": []})
        global coding_chat
        coding_chat = model.start_chat(history=[])
        return jsonify({"response": "Context cleared. Let's talk about code!"})
    
    try:
        if user_context['document_content']:
            history_string = "\n".join(user_context['chat_history'])
            prompt = [
                "Use the following document content and conversation history to answer the user's new question.",
                "--- DOCUMENT ---", user_context['document_content'], "--- END DOCUMENT ---",
                "--- HISTORY ---", history_string, "--- END HISTORY ---",
                "User's new question: " + user_input
            ]
            response = model.generate_content(prompt)
            model_response = response.text
            user_context['chat_history'].extend([f"User: {user_input}", f"AI: {model_response}"])
            return jsonify({"response": model_response})
        else:
            response = coding_chat.send_message(user_input)
            return jsonify({"response": response.text})

    # ### THE DEFINITIVE FIX: Catch the correct exception type ###
    except exceptions.ResourceExhausted as e:
        print(f"RATE LIMIT EXCEEDED: {e}")
        return jsonify({"error": "The API request limit has been reached. Please check your billing details or try again later."}), 429
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": f"An error occurred while communicating with the AI: {e}"}), 500

@app.route("/summarize", methods=["POST"])
def summarize():
    if 'file' not in request.files: return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '': return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        try:
            user_context.update({"document_content": None, "chat_history": []})

            if file.filename.lower().endswith('.pdf'):
                with pdfplumber.open(file) as pdf:
                    text_content = "".join(page.extract_text() for page in pdf.pages if page.extract_text())
                user_context['document_content'] = text_content
            else:
                img = Image.open(file); img.thumbnail((1024, 1024)); user_context['document_content'] = img
            
            if not user_context['document_content']:
                 return jsonify({"error": "Could not extract content from the file."}), 400

            prompt = ["Please summarize this document.", user_context['document_content']]
            response = model.generate_content(prompt)
            summary = response.text
            user_context['chat_history'].extend([f"User: Summarize this document.", f"AI: {summary}"])
            return jsonify({"response": summary})

        # ### THE DEFINITIVE FIX: Catch the correct exception type ###
        except exceptions.ResourceExhausted as e:
            print(f"RATE LIMIT EXCEEDED: {e}")
            return jsonify({"error": "The API request limit has been reached. Please check your billing details or try again later."}), 429
        except Exception as e:
            print(f"An error occurred during summarization: {e}")
            user_context.update({"document_content": None, "chat_history": []})
            return jsonify({"error": f"Failed to process the file: {e}"}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

if __name__ == "__main__":
    app.run(debug=True)