"""
app.py

Entry point for the Git-Conflict Arbitrator Streamlit application.
"""

import time
import streamlit as st

# ── Page must be configured before any other st call ──────────────────
from ui.styles import configure_page, load_css, show_title
configure_page()

# ── Remaining imports (after page config) ─────────────────────────────
from config import Config
from ui.sidebar import Sidebar
from ui.components import UIComponents
from models.response_models import ArbitrationResponse
from core.arbitrator import arbitrator

# ─────────────────────────────────────────────────────────────────────
# Bootstrap
# ─────────────────────────────────────────────────────────────────────

load_css()
show_title()

# Check Streamlit Secrets directly if config falls back
api_key = Config.API_KEY or st.secrets.get("GROQ_API_KEY")

# Sidebar – Passes key status to handle fallback logic gracefully
sidebar = Sidebar()
is_demo_mode = sidebar.render()

# Force override: If a key exists and demo mode isn't explicitly wanted, turn demo off
if api_key and is_demo_mode:
    # Optional: If you want live mode to always take dominance when a key is present,
    # you can uncheck the default state inside ui/sidebar.py using this key condition.
    pass

# Warn if no API key and not in demo mode
if not api_key and not is_demo_mode:
    st.warning(
        "⚠️ GROQ_API_KEY is not set. "
        "Add it to your Streamlit Secrets or enable **Demo Mode** in the sidebar."
    )

# ─────────────────────────────────────────────────────────────────────
# UI Components
# ─────────────────────────────────────────────────────────────────────

ui = UIComponents()
module_context, developer_data, analyze = ui.render_inputs()

# ─────────────────────────────────────────────────────────────────────
# Arbitration Logic
# ─────────────────────────────────────────────────────────────────────

if analyze:

    dev_a_name   = developer_data["dev_a_name"]
    dev_a_intent = developer_data["dev_a_intent"]
    dev_a_code   = developer_data["dev_a_code"]

    dev_b_name   = developer_data["dev_b_name"]
    dev_b_intent = developer_data["dev_b_intent"]
    dev_b_code   = developer_data["dev_b_code"]

    # ── Validation ────────────────────────────────────────────────────
    if not dev_a_name or not dev_b_name:
        st.error("Please provide names for both Developer A and Developer B.")

    elif not dev_a_code or not dev_b_code:
        st.error("Please add code blocks in both developer panels.")

    # ── Demo Mode Fallback ────────────────────────────────────────────
    elif is_demo_mode:

        with st.spinner("Arbitrating conflicts in Demo Mode…"):
            time.sleep(1.5)

            mock_resolved_code = f"""# Resolved Code (Demo)
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

            mock_result = ArbitrationResponse(
                conflict_analysis=(
                    f"Developer A ({dev_a_name}) added LRU caching to improve performance. "
                    f"Developer B ({dev_b_name}) added validation to verify user state. "
                    "The conflict is resolved by separating the cached DB lookup from the "
                    "validation logic, so the cache only stores raw records while "
                    "validation runs on every request."
                ),
                security_analysis=(
                    "No sensitive data is stored in the cache. Validation logic runs "
                    "after the cache lookup, so inactive users cannot exploit stale "
                    "cached state from before their account was deactivated."
                ),
                merged_strategy=(
                    "Extracted the raw database query into a private cached helper "
                    "(`_fetch_from_db`). The public `fetch_user_data` function calls "
                    "the helper and then applies the validation checks on the result."
                ),
                resolved_code=mock_resolved_code,
                architectural_notes=(
                    "1. Verify that `db.query` accepts hashable arguments for `lru_cache`.\n"
                    "2. Consider using a TTL-aware cache (e.g. `cachetools.TTLCache`) "
                    "to automatically expire stale records."
                ),
                risks=(
                    "Stale cache entries could be returned if a user's status changes "
                    "between cache misses. A short TTL or manual cache invalidation on "
                    "status change is recommended."
                ),
                confidence="High",
            )

        st.success("✅ Arbitration complete! (Demo Mode)")
        ui.render_output(mock_result)

    # ── Live Mode via Groq Engine ────────────────────────────────────
    else:

        if not api_key:
            st.error(
                "Cannot proceed — GROQ_API_KEY is missing. "
                "Enable Demo Mode or add the key to your secrets environment."
            )
        else:
            with st.spinner("Connecting to Groq Engine to arbitrate architectural conflict…"):
                try:
                    result = arbitrator.arbitrate(
                        module_context=module_context,
                        dev_a_name=dev_a_name,
                        dev_a_intent=dev_a_intent,
                        dev_a_code=dev_a_code,
                        dev_b_name=dev_b_name,
                        dev_b_intent=dev_b_intent,
                        dev_b_code=dev_b_code,
                    )

                    st.success("✅ Live Arbitration Complete!")
                    ui.render_output(result)

                except ValueError as e:
                    st.error(f"⚠️ Validation error: {e}")

                except Exception as e:
                    st.error(
                        "An error occurred during live generation. "
                        "Check that your API key is valid and try again.\n\n"
                        f"Details: {e}"
                    )
