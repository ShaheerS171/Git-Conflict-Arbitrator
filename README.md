# ⚡ Git-Conflict Arbitrator

> **The Team Collaboration Shield** — A production-ready Streamlit application that uses Mistral AI (specifically `mistral-large-latest`) to automatically arbitrate and merge conflicting code implementations based on developer intent.

This tool helps developers resolve git merge conflicts by evaluating both developer's functional intent and their conflicting code implementations, and then code-generating a single unified, syntax-correct code block alongside architectural analysis and recommendations.

---

## 🚀 Key Features

*   **Structured Pydantic Response Schema**: Standardizes output formatting by forcing the LLM to reply with a schema containing:
    *   `conflict_analysis`: An explanation of why the conflict exists and how it was resolved.
    *   `resolved_code`: A production-ready, merged code implementation.
    *   `architectural_notes`: Design decisions, warnings, or performance recommendations.
*   **Dual-Column Configuration Input**: Allows entering Developer A and Developer B's author names, feature intents, and raw conflict code side-by-side.
*   **Demo Mode (Mock Simulation)**: A sidebar toggle that allows running the application and evaluating pre-defined conflicts offline when no Mistral API key is available.
*   **Sleek Modern UI/UX**: Centered headers, gradient accents, clear code block displays, and colored callout boxes for structured reading of analytical results.

---

## 📁 Repository Structure

```plaintext
git-conflict-arbitrator/
│
├── app.py               <-- Main Streamlit UI & Core Python Backend Logic
├── requirements.txt     <-- System dependencies
├── .env                 <-- Local environment variables (DO NOT commit to Git)
└── README.md            <-- Project documentation report
```

---

## 🛠️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/git-conflict-arbitrator.git
cd git-conflict-arbitrator
```

### 2. Set Up a Virtual Environment & Install Dependencies
Ensure you have Python 3.10+ installed:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Setup Environment Variables
Create a `.env` file in the root directory:
```bash
touch .env
```
Store your Mistral API key (from Mistral Console) inside:
```env
MISTRAL_API_KEY="your_actual_mistral_api_key"
```

---

## 💻 Running the App

Start the Streamlit development server locally:
```bash
streamlit run app.py
```
By default, the application will launch at `http://localhost:8501`.

### Verification via Demo Mode
If you do not have a live `MISTRAL_API_KEY`, simply check the **"Demo Mode (Mock Simulation)"** toggle in the left sidebar configuration panel. Click the **"Analyze & Arbitrate Conflicts"** button, and the application will instantly demonstrate its capabilities using predefined conflict variables.

---

## 🚀 Cloud Deployment

### 1. Streamlit Community Cloud
1. Push the code to a public GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io).
3. Connect your repository and deploy `app.py`.
4. In the app settings on Streamlit, add `MISTRAL_API_KEY` under the secrets dashboard.

### 2. Render
1. Deploy a new Web Service linked to your GitHub repository.
2. Set the build command: `pip install -r requirements.txt`
3. Set the start command: `python -m streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
4. Add the `MISTRAL_API_KEY` environment variable in Render's dashboard.
# Git-Conflict-Arbitrator
