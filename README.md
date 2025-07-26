# Codey - The AI Coding Instructor Chatbot

Codey is a friendly and helpful AI-powered chatbot designed to be a coding instructor. Built with Flask and Google's Gemini API, it answers questions related to programming, software development, algorithms, and other computer science topics.

This project is deployed on Vercel and serves as a complete template for creating and hosting your own Python-based AI chat applications.

### ✨ [Live Demo Link](https://codey-ai-git-main-arya-prakash-shrivastavs-projects.vercel.app/)
*(Replace `your-vercel-app-url.vercel.app` with your actual Vercel project URL)*

## Features

-   **Interactive Chat Interface:** A clean and simple web interface for a real-time chat experience.
-   **AI-Powered Responses:** Utilizes the powerful Gemini 1.5 Flash model for intelligent and context-aware answers.
-   **Focused Domain:** System-instructed to only answer coding and computer science-related questions, politely declining off-topic queries.
-   **Secure API Key Handling:** Uses environment variables to keep your API key safe and out of the source code.
-   **Ready for Deployment:** Includes a `vercel.json` configuration for easy, one-click deployment to Vercel.

## Tech Stack

-   **Backend:** Python with Flask
-   **AI Model:** Google Gemini 1.5 Flash
-   **Frontend:** HTML, CSS, JavaScript (within `templates/index.html`)
-   **Deployment:** Vercel

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

-   Python 3.9 or higher
-   A Google AI Gemini API Key. You can get one from the [Google AI Studio](https://aistudio.google.com/app/apikey).

### Local Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Create and activate a virtual environment:**
    *   This is highly recommended to keep project dependencies isolated.
    ```bash
    # For Windows
    python -m venv venv
    .\venv\Scripts\Activate

    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Create an environment file:**
    *   Create a new file in the root directory named `.env`.
    *   Add your Gemini API key to this file. This file is listed in `.gitignore` and will not be committed to your repository.
    ```
    GEMINI_API_KEY="AIzaSy...your...secret...api...key"
    ```

5.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    Open your browser and navigate to `http://127.0.0.1:5000` to see your chatbot running locally!

---

## 🌐 Deploying to Vercel

This project is configured for easy deployment on Vercel's serverless platform.

### Step 1: Push to GitHub

Commit all your code (including `app.py`, `requirements.txt`, and the new `vercel.json`) to a GitHub repository. Ensure your `.gitignore` file includes `.env` to prevent your secret key from being exposed.

### Step 2: Import Project to Vercel

1.  Log in to your Vercel account.
2.  Click "Add New..." -> "Project".
3.  Select your GitHub repository. Vercel will automatically detect that it is a Python project.

### Step 3: Configure Environment Variables

This is the most important step for security.

1.  In your Vercel project dashboard, go to **Settings > Environment Variables**.
2.  Add a new variable:
    -   **Name:** `GEMINI_API_KEY`
    -   **Value:** Paste your actual Gemini API key here.
3.  Ensure the variable is available for all environments (Production, Preview, Development).
4.  Save the variable.

### Step 4: Deploy

Vercel will have already triggered a deployment. If you added the environment variable after the initial deployment, go to the "Deployments" tab and trigger a redeployment to apply the changes. The `vercel.json` file in this repository will ensure that Vercel routes all requests correctly to your Flask app.

### Step 5: Make Your Site Public

By default, Vercel protects new deployments. To make your site accessible to everyone without requiring a login:

1.  In your Vercel project settings, go to the **Security** tab.
2.  **Turn Off** the **Deployment Protection** feature.
3.  Your website will now be publicly accessible to anyone with the link!
