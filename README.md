# Git-Conflict Arbitrator

> **The Team Collaboration Shield**  
> AI-powered Git merge conflict resolution using **Mistral AI**. Analyze conflicting implementations, understand each developer's intent, and generate a single production-ready solution with detailed conflict analysis and architectural recommendations.

---

## 🌐 Live Demo

🚀 **Try it here:**  
https://shaheers171-git-conflict-arbitrator-app-515lqb.streamlit.app/

---

# 🧪 Quick Test Case

Want to test the application immediately?

Copy the following values into the interface.

---

## Project Context / Module

```text
Python FastAPI user services module
```

---

## Developer A

**Developer Name**

```text
Shaheer
```

**Feature Intent / Goal**

```text
Add caching to improve performance.
```

**Conflicting Code**

```python
@app.get("/users/{user_id}")
async def get_user_data(user_id: str):
    # Check cache first to optimize response time
    cached_data = await redis_client.get(f"user:{user_id}")
    if cached_data:
        return json.loads(cached_data)

    user = await db.fetch_user_by_id(user_id)

    # Store result in cache for 1 hour
    await redis_client.setex(f"user:{user_id}", 3600, json.dumps(user))

    return user
```

---

## Developer B

**Developer Name**

```text
Your Name
```

**Feature Intent / Goal**

```text
Add validation before returning data.
```

**Conflicting Code**

```python
@app.get("/users/{user_id}")
async def get_user_data(user_id: str):
    # Validate user ID length and alphanumeric format
    if not user_id.isalnum() or len(user_id) != 8:
        raise HTTPException(
            status_code=400,
            detail="Invalid User ID format"
        )

    user = await db.fetch_user_by_id(user_id)

    # Validate user existence
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
```

## Motivation

While collaborating on a GitHub project, I encountered my first merge conflict after making improvements to an existing codebase. Although Git clearly showed where the conflict occurred, understanding how to combine two different implementations without breaking functionality was much more difficult than expected.

Resolving the conflict manually took considerable time and required carefully understanding the purpose behind both versions of the code. That experience inspired the idea behind **Git-Conflict Arbitrator** an AI powered assistant that analyzes both developers intentions instead of simply comparing text differences.

Rather than forcing developers to manually decide which code to keep, the application evaluates both implementations, understands the feature goals, and produces a unified, production-ready solution while explaining the reasoning behind every decision.

---

# The Problem It Solves

Merge conflicts are a normal part of collaborative software development, but resolving them correctly often requires understanding **why** each developer changed the code—not just **what** they changed.

Traditional merge tools compare files line by line, leaving developers to manually determine:

- Which implementation should be preserved.
- Which logic should be combined.
- Whether either implementation introduces bugs or security risks.
- How both features can coexist without breaking the application.

This process becomes increasingly difficult when developers are working on the same function with completely different objectives.

**Git-Conflict Arbitrator** addresses this challenge by using a Large Language Model to analyze:

- The project context
- Developer A's feature intent
- Developer B's feature intent
- Both conflicting code implementations

The AI then generates:

- ✅ A production-ready merged implementation
- ✅ A detailed conflict analysis
- ✅ Architectural recommendations
- ✅ Security and design considerations

Instead of replacing Git's merge system, the application acts as an intelligent decision support layer that helps developers resolve conflicts faster and with greater confidence.

---

# Features

-  AI-powered merge conflict arbitration using **Mistral AI**
-  Intent-aware conflict resolution instead of simple text comparison
-  Independent inputs for two developers
-  Project context support for improved AI reasoning
-  Production ready merged code generation
-  Detailed conflict analysis explaining the resolution process
-  Architectural notes with design recommendations
-  Demo Mode for testing without an API key
-  Secure API key management using environment variables and Streamlit Secrets
-  Graceful error handling with user-friendly messages
-  Clean Streamlit interface with syntax-highlighted code output

---

#  Architecture

```text
                 User Input
                      │
      ┌───────────────┴───────────────┐
      │                               │
Developer A                     Developer B
Intent + Code                 Intent + Code
      │                               │
      └───────────────┬───────────────┘
                      │
              Project Context
                      │
                      ▼
             Prompt Construction
                      │
                      ▼
             Mistral Large Model
                      │
                      ▼
        Structured JSON (Pydantic)
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
Resolved Code   Conflict Analysis   Architectural Notes
```

---

#  Screenshots

### Input Layout

<img width="1433" height="774" alt="image" src="https://github.com/user-attachments/assets/876542fc-7bcd-4d7a-a954-f0ce733c72f6" />

---

### Resolved Output

<img width="1385" height="853" alt="image" src="https://github.com/user-attachments/assets/bd2e7542-6851-4355-ab54-b672d9c89727" />

---

### Conflict Analysis

<img width="1371" height="734" alt="image" src="https://github.com/user-attachments/assets/b5362f2b-137b-41e5-959a-3325979d7a0f" />

---

### Security Analysis

<img width="1422" height="716" alt="image" src="https://github.com/user-attachments/assets/31aedd62-65af-40cb-93a0-547e00e5526e" />

---

### Risk Analysis

<img width="1441" height="702" alt="image" src="https://github.com/user-attachments/assets/80ab1dc8-7c6f-492b-a8c7-da4576975551" />

---

### Architectural Notes

<img width="1401" height="645" alt="image" src="https://github.com/user-attachments/assets/2e25c299-edcc-4b7c-a0bc-94129e183eb9" />

---

---

**Expected Result**

The application should generate:

- ✅ A merged production-ready implementation
- ✅ Conflict analysis
- ✅ Architectural recommendations
- ✅ Security and performance considerations

---

#  AI Implementation

## Overview

The core intelligence of **Git-Conflict Arbitrator** is powered by **Mistral AI's `mistral-large-latest` model**. Instead of relying on traditional line by line merge algorithms, the application performs **intent-aware conflict resolution** by understanding what each developer is trying to accomplish before generating a unified implementation.

The workflow is designed to preserve the objectives of both developers whenever possible while producing clean, maintainable, and production-ready code.

---

## How It Works

The arbitration pipeline follows these steps:

1. The user provides the project or module context.
2. Developer A enters:
   - Name
   - Feature intent
   - Conflicting code
3. Developer B enters:
   - Name
   - Feature intent
   - Conflicting code
4. The application constructs a structured prompt containing all developer information.
5. The prompt is sent to **Mistral AI**.
6. The model analyzes both implementations and their intended goals.
7. The response is validated using a **Pydantic schema**.
8. The application displays:
   - Production-ready merged code
   - Conflict analysis
   - Architectural recommendations

---

## AI Model

| Property | Value |
|----------|-------|
| Provider | Mistral AI |
| Model | `mistral-large-latest` |
| Framework | Streamlit |
| Response Format | Structured JSON |
| Validation | Pydantic v2 |

---

#  Structured Response Schema

To ensure reliable and predictable responses, the model returns a structured JSON object validated using **Pydantic**.

```python
class ArbitrationResponse(BaseModel):
    conflict_analysis: str
    resolved_code: str
    architectural_notes: str
```

### Response Fields

| Field | Description |
|--------|-------------|
| **conflict_analysis** | Explains why the conflict occurred, summarizes each developer's intent, and describes how the conflict was resolved. |
| **resolved_code** | A complete, production-ready implementation that combines both developers' features. |
| **architectural_notes** | Design considerations, recommendations, performance observations, and potential security concerns. |

---

#  Prompt Engineering

The application dynamically constructs a prompt that contains:

- Project context
- Programming language or module
- Developer A's information
- Developer B's information
- Both conflicting implementations
- Detailed instructions for producing structured output

This allows the model to reason about **developer intent** rather than simply comparing text differences.

---

#  System Prompt

```text
You are an expert software architect and Git conflict resolution agent called the Git-Conflict Arbitrator.

Analyze the following conflicting feature intents and code implementations for a project module having this context:

Project Context/Language:
{module_context}

Developer A:
{dev_a_name}

Feature Intent:
{dev_a_intent}

Conflicting Code Block:
{dev_a_code}

Developer B:
{dev_b_name}

Feature Intent:
{dev_b_intent}

Conflicting Code Block:
{dev_b_code}

Please resolve the conflict by providing:

1. conflict_analysis
A detailed breakdown explaining:
- Why the conflict happened
- What each developer intended
- How both implementations were combined

2. resolved_code
Generate a clean, production-ready implementation that:
- Integrates both feature sets
- Avoids duplicated logic
- Includes helpful comments where appropriate
- Produces a complete solution

3. architectural_notes
Include:
- Design decisions
- Performance observations
- Security considerations
- Potential risks
- Future recommendations

Instructions:

- Return valid JSON only.
- Do not wrap code inside markdown blocks.
- If the supplied input is invalid or not software code,
  return analytical errors using the same JSON schema.
- Ensure the merged implementation is complete and executable.
```

---

#  Technologies Used

| Category | Technology |
|-----------|------------|
| Programming Language | Python 3.10+ |
| Frontend Framework | Streamlit |
| AI Provider | Mistral AI |
| AI Model | `mistral-large-latest` |
| Data Validation | Pydantic v2 |
| Environment Management | python-dotenv |
| Deployment | Streamlit Community Cloud |

---

#  Why Intent Based Conflict Resolution?

Traditional Git merge tools compare **code differences**.

Git-Conflict Arbitrator compares **developer intentions**.

Instead of asking:

> "Which lines changed?"

the AI asks:

> "What was each developer trying to accomplish?"

This enables the application to intelligently combine complementary features such as:

- Performance optimizations
- Input validation
- Security enhancements
- Error handling
- Logging
- Refactoring

without forcing developers to manually reconstruct the final implementation.

---

#  Demo Mode

The application includes a built-in **Demo Mode (Mock Simulation)**.

When enabled:

- No API key is required.
- No requests are sent to Mistral AI.
- The application returns predefined sample results.
- The complete interface can be demonstrated offline.

This feature is particularly useful for:

- Project demonstrations
- Portfolio presentations
- Academic evaluations
- Testing the user interface
- Exploring the application's workflow without consuming API credits

---

#  Security Considerations

To protect sensitive credentials, the application follows recommended security practices:

- API keys are never hardcoded into the source code.
- Credentials are loaded using environment variables.
- Streamlit Secrets are supported for deployment.
- `.env` files are excluded using `.gitignore`.
- Errors are handled gracefully without exposing sensitive information.

These practices help ensure that API credentials remain secure during both development and deployment.

#  Getting Started

Follow these steps to run the project locally.

---

## 1. Clone the Repository

```bash
git clone https://github.com/ShaheerS171/git-conflict-arbitrator.git
cd git-conflict-arbitrator
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

Upgrade pip (recommended):

```bash
pip install --upgrade pip
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## 4. Configure Your API Key

Create a `.env` file in the project root.

### Linux / macOS

```bash
touch .env
```

### Windows

```cmd
type nul > .env
```

Add your Mistral API key:

```env
MISTRAL_API_KEY="your_actual_mistral_api_key"
```

You can obtain an API key from:

https://console.mistral.ai

---

## 5. Run the Application

```bash
streamlit run app.py
```

The application will start locally and open in your browser at:

```
http://localhost:8501
```

---

#  Running Without an API Key

The project includes a **Demo Mode (Mock Simulation)** for users who do not have a Mistral API key.

Simply enable the **Demo Mode** toggle from the left sidebar.

Demo Mode allows you to:

- Explore the complete interface
- Generate sample conflict resolutions
- View architectural recommendations
- Test the application's workflow
- Demonstrate the project without making API requests

This is especially useful for:

- Academic evaluations
- Portfolio demonstrations
- Recruiter presentations
- Offline testing

---

#  Deployment

The application is deployed using **Streamlit Community Cloud**.

### Deployment Steps

1. Push the repository to GitHub.

2. Sign in to:

https://share.streamlit.io

3. Create a new application.

4. Connect your GitHub repository.

5. Select:

```
app.py
```

as the main application file.

6. Open **App Settings → Secrets**

Add:

```toml
MISTRAL_API_KEY = "your_actual_mistral_api_key"
```

7. Click **Deploy**.

Your application will become publicly available through a `.streamlit.app` URL.

---

#  Live Demo

Try the deployed application here:

https://shaheers171-git-conflict-arbitrator-app-515lqb.streamlit.app/

---

#  Important Notes

Before running or deploying the application, keep the following recommendations in mind:

- Never commit your `.env` file.
- Never expose your API key publicly.
- Ensure `.env` is included in `.gitignore`.
- Use Streamlit Secrets for cloud deployments.
- Keep dependencies updated.
- Verify that your GitHub repository is set to **Public** before sharing it.
- Test using Demo Mode if you do not have an API key.

---

# Future Improvements

This project establishes a foundation for AI-assisted merge conflict resolution. Several enhancements can further improve its capabilities:

### Git Integration

- Automatic Git merge conflict detection
- Support for multi-file conflicts
- Git patch generation
- Automatic commit suggestions

### AI Improvements

- Support for multiple LLM providers
- Local LLM inference
- Model selection inside the UI
- Better architectural reasoning
- Repository-aware conflict analysis

### Developer Experience

- VS Code extension
- GitHub Pull Request integration
- GitHub Actions workflow
- REST API version
- Docker deployment
- User authentication

### UI Improvements

- Dark/Light theme switching
- Conflict visualization
- Side-by-side diff viewer
- Download merged code
- Export reports as PDF

---

#  Contributing

Contributions are welcome!

If you have ideas for new features, performance improvements, or bug fixes, feel free to:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push your branch
5. Open a Pull Request

Constructive feedback and suggestions are always appreciated.

---

# Technologies

- Python
- Streamlit
- Mistral AI
- Pydantic
- python-dotenv

---

# Acknowledgements

Special thanks to:

- **Mistral AI** for providing the language model powering the arbitration engine.
- **Streamlit** for enabling rapid development of interactive AI applications.
- The open-source community for continuously inspiring better software engineering practices.

---

# License

This project is licensed under the **MIT License**.

You are free to use, modify, and distribute this project in accordance with the terms of the license.

---

# Author

**Shaheer**

GitHub:
https://github.com/ShaheerS171

---

##  Support the Project

If you found this project useful or interesting:

 Report bugs

 Suggest new features

 Contribute to the project

Your support helps improve the project and encourages future development.

---

## Thank You!

Thank you for checking out **Git-Conflict Arbitrator**.

