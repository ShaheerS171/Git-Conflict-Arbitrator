import os
import streamlit as st
from pydantic import BaseModel
from dotenv import load_dotenv

# Load local .env variables
load_dotenv()

# Define structural schema
class ArbitrationResponse(BaseModel):
    conflict_analysis: str
    resolved_code: str
    architectural_notes: str

# Page Configuration
st.set_page_config(
    page_title="⚡ Git-Conflict Arbitrator",
    page_icon="⚡",
    layout="wide"
)

# Custom Sleek CSS Styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Outfit', sans-serif;
}
.title-container {
    text-align: center;
    padding: 1.5rem 0rem;
}
h1 {
    font-weight: 800 !important;
    background: linear-gradient(135deg, #FF4B4B, #FF8F8F) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-size: 3rem !important;
}
.subtitle {
    font-size: 1.25rem;
    color: #888888;
    margin-top: -1rem;
    margin-bottom: 2rem;
    font-weight: 400;
}
.callout-title {
    font-size: 1.15rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.callout-box-analysis {
    background-color: rgba(255, 75, 75, 0.05);
    border-left: 5px solid #FF4B4B;
    padding: 1.2rem;
    border-radius: 8px;
    margin-top: 1rem;
}
.callout-box-notes {
    background-color: rgba(33, 150, 243, 0.05);
    border-left: 5px solid #2196F3;
    padding: 1.2rem;
    border-radius: 8px;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# App Titles
st.markdown('<div class="title-container"><h1>⚡ Git-Conflict Arbitrator</h1><div class="subtitle">The Team Collaboration Shield</div></div>', unsafe_allow_html=True)

# API Configuration and State Management
api_key = os.environ.get("MISTRAL_API_KEY")
if not api_key and "MISTRAL_API_KEY" in st.secrets:
    api_key = st.secrets["MISTRAL_API_KEY"]

# Sidebar Integration
st.sidebar.title("🛠️ Configuration")
is_demo_mode = st.sidebar.toggle("Demo Mode (Mock Simulation)", value=(not bool(api_key)))

if not api_key:
    if not is_demo_mode:
        st.warning("⚠️ MISTRAL_API_KEY is not defined in the environment config or secrets. Please add it to your configuration, or enable 'Demo Mode (Mock Simulation)' in the sidebar to run the application.")
    else:
        st.sidebar.info("💡 Running in Demo Mode (Mock Simulation) because active api key is missing.")

# Top full-width single-line text input
module_context = st.text_input(
    "Project Module Context / Language", 
    value="Python FastAPI User Services Module",
    placeholder="e.g., Python FastAPI tracking module, React auth context..."
)

# Opposing inputs layout (columns)
col1, col2 = st.columns(2)

with col1:
    st.subheader("Developer A")
    dev_a_name = st.text_input("Name", value="Shaheer", key="dev_a_name")
    dev_a_intent = st.text_input("Feature Intent / Goal", value="Add LRU caching to the fetch_user_data function to improve lookup speed.", key="dev_a_intent")
    dev_a_code = st.text_area(
        "Conflicting Code Block",
        value="""def fetch_user_data(user_id):
    # Fetch from database
    data = db.query("SELECT * FROM users WHERE id = ?", user_id)
    return data""",
        height=200,
        key="dev_a_code"
    )

with col2:
    st.subheader("Developer B")
    dev_b_name = st.text_input("Name", value="Teammate", key="dev_b_name")
    dev_b_intent = st.text_input("Feature Intent / Goal", value="Add validation checks to verify user state is active before returning data.", key="dev_b_intent")
    dev_b_code = st.text_area(
        "Conflicting Code Block",
        value="""def fetch_user_data(user_id):
    data = db.query("SELECT * FROM users WHERE id = ?", user_id)
    if not data:
        raise ValueError("User not found")
    if data.get("status") != "active":
        raise PermissionError("User is inactive")
    return data""",
        height=200,
        key="dev_b_code"
    )

# Action button
st.markdown("<br>", unsafe_allow_html=True)
arbitrate_button = st.button("Analyze & Arbitrate Conflicts", use_container_width=True)

# Process click
if arbitrate_button:
    # Validation checks
    if not dev_a_name or not dev_b_name:
        st.error("Please provide names for both Developer A and Developer B.")
    elif not dev_a_code or not dev_b_code:
        st.error("Please add code blocks in both developer panels.")
    else:
        # Predefined Mock response for Demo Mode
        if is_demo_mode:
            with st.spinner("Arbitrating conflicts in Demo Mode... Evaluating intents & checking syntax..."):
                import time
                time.sleep(2) # Simulate processing delay
                
                # Mock result payload
                mock_resolved_code = f"""# Resolved Code
from functools import lru_cache

@lru_cache(maxsize=128)
def _fetch_from_db(user_id):
    # Cached database lookup to speed up performance (Intent: {dev_a_name})
    return db.query("SELECT * FROM users WHERE id = ?", user_id)

def fetch_user_data(user_id):
    # Perform cached query
    data = _fetch_from_db(user_id)
    
    # Validate user is active (Intent: {dev_b_name})
    if not data:
        raise ValueError("User not found")
    if data.get("status") != "active":
        raise PermissionError("User is inactive")
        
    return data"""
                
                mock_analysis = f"Developer A ({dev_a_name}) wanted to add performance-enhancing caching. Developer B ({dev_b_name}) wanted user status validation checks. The arbitrator resolved this by decoupling the database operation (which is now cached) from the logic check (which must run on every request to ensure real-time status check)."
                mock_notes = "1. Using `lru_cache` internally avoids caching validation logic so inactive users cannot exploit previously cached active state. 2. Verify that `db.query` supports hashable arguments."
                
                # Display output
                st.success("Arbitration complete!")
                st.subheader("Resolved Unified Code Block")
                st.code(mock_resolved_code, language="python")
                
                details_col1, details_col2 = st.columns(2)
                with details_col1:
                    st.markdown(f'<div class="callout-box-analysis"><div class="callout-title">🔴 Conflict Analysis</div>{mock_analysis}</div>', unsafe_allow_html=True)
                with details_col2:
                    st.markdown(f'<div class="callout-box-notes"><div class="callout-title">🟢 Architectural Notes</div>{mock_notes}</div>', unsafe_allow_html=True)
        else:
            if not api_key:
                st.error("Cannot proceed. MISTRAL_API_KEY is missing and Demo Mode is disabled. Enable Demo Mode in the sidebar or provide an API key.")
            else:
                with st.spinner("Connecting to Mistral (mistral-large-latest) to analyze & resolve git conflicts..."):
                    try:
                        from mistralai.client import Mistral
                        
                        # Initialize Mistral Client
                        client = Mistral(api_key=api_key)
                        
                        prompt = f"""
                        You are an expert software architect and git conflict resolution agent called the Git-Conflict Arbitrator.
                        Analyze the following conflicting feature intents and code implementations for a project module having this context:
                        Project Context/Language: {module_context}

                        Developer A: {dev_a_name}
                        Feature Intent: {dev_a_intent}
                        Conflicting Code Block:
                        ```
                        {dev_a_code}
                        ```

                        Developer B: {dev_b_name}
                        Feature Intent: {dev_b_intent}
                        Conflicting Code Block:
                        ```
                        {dev_b_code}
                        ```

                        Please resolve the conflict by providing:
                        1. conflict_analysis: A detailed breakdown of why the conflict happened, what each developer intended, and how the conflict is resolved by combining both intents.
                        2. resolved_code: A production-ready, clean, single, and complete unified code block that successfully integrates the features of Developer A and Developer B without duplication, including comments explaining the changes.
                        3. architectural_notes: Important design decisions, potential security warnings, performance considerations, or follow-up recommendations.

                        Instructions:
                        - Do not output any markdown code blocks inside the json fields (e.g. do not wrap resolved_code with markdown backticks).
                        - If the inputs are invalid or not software code, return appropriate analytical errors in the json format.
                        - Ensure the resolved code is complete, correct, and compiles/runs.
                        """
                        
                        resolved_code = ""
                        conflict_analysis = ""
                        architectural_notes = ""
                        
                        # 1. Try structured parse
                        try:
                            response = client.chat.parse(
                                model="mistral-large-latest",
                                messages=[{"role": "user", "content": prompt}],
                                response_format=ArbitrationResponse,
                                temperature=0.2
                            )
                            result = response.choices[0].message.parsed # type:ignore
                            if result:
                                resolved_code = result.resolved_code
                                conflict_analysis = result.conflict_analysis
                                architectural_notes = result.architectural_notes
                        except Exception as e_parse:
                            # 2. Fallback to normal complete client with json_object configuration
                            try:
                                response = client.chat.complete(
                                    model="mistral-large-latest",
                                    messages=[{"role": "user", "content": prompt + "\nRespond strictly in JSON matching the schema containing conflict_analysis, resolved_code, and architectural_notes fields."}],
                                    response_format={"type": "json_object"},
                                    temperature=0.2
                                )
                                import json
                                result_dict = json.loads(response.choices[0].message.content) #type:ignore
                                resolved_code = result_dict.get("resolved_code", "")
                                conflict_analysis = result_dict.get("conflict_analysis", "")
                                architectural_notes = result_dict.get("architectural_notes", "")
                            except Exception as e_complete:
                                raise RuntimeError(f"Mistral API calls failed.\nParse error: {e_parse}\nComplete error: {e_complete}")
                        
                        if not resolved_code:
                            raise ValueError("Empty response returned from Mistral.")
                            
                        st.success("Arbitration complete!")
                        st.subheader("Resolved Unified Code Block")
                        st.code(resolved_code, language="python" if "python" in module_context.lower() else "")
                        
                        details_col1, details_col2 = st.columns(2)
                        with details_col1:
                            st.markdown(f'<div class="callout-box-analysis"><div class="callout-title">🔴 Conflict Analysis</div>{conflict_analysis}</div>', unsafe_allow_html=True)
                        with details_col2:
                            st.markdown(f'<div class="callout-box-notes"><div class="callout-title">🟢 Architectural Notes</div>{architectural_notes}</div>', unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.error("An error occurred during conflict arbitration. The API key might be invalid or the model request failed. Details: " + str(e))
