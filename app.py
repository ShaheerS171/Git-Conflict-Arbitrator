"""
app.py

Entry point for the Git-Conflict Arbitrator Streamlit application.

Flow
  1. Configure page & load CSS            (ui/styles.py)
  2. Render sidebar                        (ui/sidebar.py)
  3. Render title                          (ui/styles.py)
  4. Render inputs                         (ui/components.py)
  5. On button click
     a. Demo mode  → mock response
     b. Live mode  → core/arbitrator.py pipeline
  6. Display results tabs                  (ui/components.py)
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

# Sidebar – returns the current demo-mode toggle value
sidebar = Sidebar()
is_demo_mode = sidebar.render()

# Warn if no API key and not in demo mode
if not Config.API_KEY and not is_demo_mode:
    st.warning(
        "⚠️ MISTRAL_API_KEY is not set.  "
        "Add it to your `.env` file or enable **Demo Mode** in the sidebar."
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

    # ── Demo Mode ─────────────────────────────────────────────────────
    elif is_demo_mode:

        with st.spinner("Arbitrating conflicts in Demo Mode…"):
            time.sleep(2)

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

    # ── Live Mode via Mistral ──────────────────────────────────────────
    else:

        if not Config.API_KEY:
            st.error(
                "Cannot proceed — MISTRAL_API_KEY is missing.  "
                "Enable Demo Mode or add the key to `.env`."
            )
        else:
            with st.spinner(
                f"Connecting to Mistral ({Config.MODEL_NAME}) to resolve conflicts…"
            ):
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

                    st.success("✅ Arbitration complete!")
                    ui.render_output(result)

                except ValueError as e:
                    st.error(f"⚠️ Validation error: {e}")

                except Exception as e:
                    st.error(
                        "An error occurred during arbitration. "
                        "Check that your API key is valid and try again.\n\n"
                        f"Details: {e}"
                    )
