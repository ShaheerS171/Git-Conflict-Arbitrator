"""
ui/styles.py

Contains all Streamlit styling and page configuration.
"""

import streamlit as st


def configure_page():
    """
    Configure the Streamlit page.
    """

    st.set_page_config(
        page_title="⚡ Git Conflict Arbitrator",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def load_css():
    """
    Load the application's CSS.
    """

    st.markdown(
        """
<style>

@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

html,
body,
[data-testid="stAppViewContainer"]{
    font-family:'Outfit',sans-serif;
}

/* --------------------------------------------------- */
/* Title */
/* --------------------------------------------------- */

.title-container{
    text-align:center;
    padding:1.5rem 0;
}

.title-container h1{

    font-size:3rem;

    font-weight:800;

    margin-bottom:0.2rem;

    background:linear-gradient(
        135deg,
        #FF4B4B,
        #FF8F8F
    );

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;

}

.subtitle{

    color:#8A8A8A;

    font-size:1.2rem;

    margin-top:-0.5rem;

}

/* --------------------------------------------------- */
/* Inputs */
/* --------------------------------------------------- */

textarea{

    font-family:
        "JetBrains Mono",
        monospace !important;

    font-size:14px !important;

}

code{

    font-family:
        "JetBrains Mono",
        monospace;

}

/* --------------------------------------------------- */
/* Buttons */
/* --------------------------------------------------- */

.stButton>button{

    width:100%;

    border-radius:12px;

    font-size:18px;

    font-weight:600;

    padding:12px;

}

/* --------------------------------------------------- */
/* Sidebar */
/* --------------------------------------------------- */

[data-testid="stSidebar"]{

    border-right:1px solid rgba(255,255,255,.08);

}

/* --------------------------------------------------- */
/* Analysis Box */
/* --------------------------------------------------- */

.analysis-box{

    background:rgba(255,75,75,.05);

    border-left:5px solid #FF4B4B;

    padding:18px;

    border-radius:10px;

    margin-top:15px;

}

/* --------------------------------------------------- */
/* Notes Box */
/* --------------------------------------------------- */

.notes-box{

    background:rgba(33,150,243,.05);

    border-left:5px solid #2196F3;

    padding:18px;

    border-radius:10px;

    margin-top:15px;

}

/* --------------------------------------------------- */
/* Security Box */
/* --------------------------------------------------- */

.security-box{

    background:rgba(76,175,80,.05);

    border-left:5px solid #4CAF50;

    padding:18px;

    border-radius:10px;

    margin-top:15px;

}

/* --------------------------------------------------- */
/* Risk Box */
/* --------------------------------------------------- */

.risk-box{

    background:rgba(255,193,7,.08);

    border-left:5px solid #FFC107;

    padding:18px;

    border-radius:10px;

    margin-top:15px;

}

/* --------------------------------------------------- */
/* Confidence */
/* --------------------------------------------------- */

.confidence-high{

    color:#4CAF50;

    font-weight:bold;

}

.confidence-medium{

    color:#FFC107;

    font-weight:bold;

}

.confidence-low{

    color:#F44336;

    font-weight:bold;

}

/* --------------------------------------------------- */
/* Code */
/* --------------------------------------------------- */

pre{

    border-radius:10px;

}

</style>
""",
        unsafe_allow_html=True,
    )


def show_title():
    """
    Display the application title.
    """

    st.markdown(
        """
<div class="title-container">

<h1>⚡ Git Conflict Arbitrator</h1>

<div class="subtitle">

The Team Collaboration Shield

</div>

</div>
""",
        unsafe_allow_html=True,
    )