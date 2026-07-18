# Git-Conflict Arbitrator

**The Team Collaboration Shield**

A production-ready Streamlit application that uses Mistral AI to automatically resolve conflicting code implementations from two developers by analyzing their stated intent and generating a single, unified, production-quality code block.

---

## The Problem It Solves

Software development teams using Git regularly face merge conflicts — situations where two developers modify the same function or file with different goals in mind. Manually resolving these conflicts requires deep context about what each developer intended, which takes time and leads to mistakes when done under pressure.

**Git-Conflict Arbitrator** is built for software development teams who want an AI-assisted decision layer on top of their Git workflow. Instead of manually re-reading both branches and guessing at a merge strategy, developers paste their conflicting versions and intent descriptions into the tool and receive a merged, architecturally sound code block alongside a conflict breakdown and engineering notes.

---

## Live Deployed URL

[https://your-app-name.streamlit.app](https://your-app-name.streamlit.app](https://shaheers171-git-conflict-arbitrator-app-515lqb.streamlit.app/))

*(Replace this with your actual Streamlit Community Cloud URL once deployed)*

---

## Features

- **Side-by-side conflict input**: Two-column layout allows Developer A and Developer B to each provide their name, feature intent, and conflicting code block independently.
- **Project module context input**: A full-width text field at the top specifies the language or module being worked on (e.g., "Python FastAPI user services module") to give the AI grounding.
- **AI-powered conflict arbitration**: Sends both developer inputs and intents to Mistral AI's `mistral-large-latest` model and receives a structured JSON response containing the merged resolution.
- **Structured output display**: The resolved code block is rendered with syntax highlighting. Conflict Analysis and Architectural Notes are displayed in styled side-by-side callout panels beneath it.
- **Demo Mode (Mock Simulation)**: A sidebar toggle that bypasses the API entirely and returns a predefined mock response. This allows the app to be fully demonstrated without an active API key.
- **Safe API key handling**: The app checks for the key in environment variables and Streamlit secrets — never hardcoded in source.
- **Graceful error handling**: All API and parsing failures are caught and displayed as readable user-facing messages with no raw tracebacks exposed.

---

## AI Feature

**What it does:**

The AI feature takes the two conflicting code blocks and the stated intent of each developer, constructs a detailed arbitration prompt, and calls Mistral AI to return a three-part structured JSON response.

**Model used:** `mistral-large-latest` via the Mistral AI API

**Structured output schema (Pydantic):**

```python
class ArbitrationResponse(BaseModel):
    conflict_analysis: str   # Why the conflict happened and how it was resolved
    resolved_code: str       # The merged, production-ready code block
    architectural_notes: str # Design decisions, warnings, recommendations
```

**System prompt sent to the model:**

```
You are an expert software architect and git conflict resolution agent called the Git-Conflict Arbitrator.
Analyze the following conflicting feature intents and code implementations for a project module having this context:
Project Context/Language: {module_context}

Developer A: {dev_a_name}
Feature Intent: {dev_a_intent}
Conflicting Code Block:
{dev_a_code}

Developer B: {dev_b_name}
Feature Intent: {dev_b_intent}
Conflicting Code Block:
{dev_b_code}

Please resolve the conflict by providing:
1. conflict_analysis: A detailed breakdown of why the conflict happened, what each developer intended,
   and how the conflict is resolved by combining both intents.
2. resolved_code: A production-ready, clean, single, and complete unified code block that successfully
   integrates the features of Developer A and Developer B without duplication, including comments
   explaining the changes.
3. architectural_notes: Important design decisions, potential security warnings, performance
   considerations, or follow-up recommendations.

Instructions:
- Do not output any markdown code blocks inside the json fields.
- If the inputs are invalid or not software code, return appropriate analytical errors in the json format.
- Ensure the resolved code is complete, correct, and compiles/runs.
```

---

## Tools, Services, and Models Used

| Category | Tool / Service |
|---|---|
| Language | Python 3.10+ |
| Web Framework | Streamlit |
| AI Provider | Mistral AI |
| AI Model | mistral-large-latest |
| Response Schema | Pydantic v2 |
| Environment Config | python-dotenv |
| Deployment | Streamlit Community Cloud |

---

## Screenshots

*(Add 3 or more screenshots of your running app here after deployment)*

Example:
```
![Input layout showing Developer A and Developer B columns](screenshots/input_view.png)
![Demo mode output showing resolved code block](screenshots/output_code.png)
![Conflict analysis and architectural notes panels](screenshots/output_details.png)
```

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/git-conflict-arbitrator.git
cd git-conflict-arbitrator
```

### 2. Set Up a Virtual Environment and Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Your API Key

Create a `.env` file in the project root:

```bash
touch .env
```

Add your Mistral API key (get one at [console.mistral.ai](https://console.mistral.ai)):

```env
MISTRAL_API_KEY="your_actual_mistral_api_key"
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

### Running Without an API Key (Demo Mode)

If you do not have a Mistral API key, enable the **Demo Mode (Mock Simulation)** toggle in the left sidebar. The app will simulate a complete arbitration response using predefined mock data, allowing full demonstration of the interface without any API calls.

---

## Deployment on Streamlit Community Cloud

1. Push this repository to a public GitHub repository.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io).
3. Click **New app**, connect your GitHub repository, and set the main file to `app.py`.
4. Go to **App Settings > Secrets** and add:

```toml
MISTRAL_API_KEY = "your_actual_mistral_api_key"
```

5. Click **Deploy**. The app will be available at a public `.streamlit.app` URL.

---

## Important Notes

- Never commit your `.env` file or API keys to the repository. The `.env` file is listed in `.gitignore`.
- The repository must be set to **Public** on GitHub before submitting. Verify this by opening the repo link in a private/incognito browser window.
