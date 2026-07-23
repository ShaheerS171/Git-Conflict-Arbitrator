"""
ui/sidebar.py

Sidebar components for the Git Conflict Arbitrator.
"""

import streamlit as st

from config import Config


class Sidebar:

    def __init__(self):
        self.demo_mode = Config.DEMO_MODE

    ####################################################################
    # Sidebar
    ####################################################################

    def render(self):
        """
        Render the sidebar.
        """

        st.sidebar.title(" Configuration")

        st.sidebar.markdown("---")

        self.demo_mode = st.sidebar.toggle(
            "Demo Mode (Mock Simulation)",
            value=Config.DEMO_MODE,
        )

        st.sidebar.markdown("---")

        st.sidebar.subheader(" Model")

        st.sidebar.info(
            Config.MODEL_NAME
        )

        st.sidebar.markdown("---")

        self._api_status()

        st.sidebar.markdown("---")

        st.sidebar.subheader("About")

        st.sidebar.caption(
            """
Git Conflict Arbitrator

• AI-powered merge conflict resolution

• Security-aware code merging

• Architecture analysis

• Production-ready suggestions
"""
        )

        st.sidebar.markdown("---")

        st.sidebar.caption(
            "Version 1.0.0"
        )

        return self.demo_mode

    ####################################################################
    # API Status
    ####################################################################

    def _api_status(self):

        st.sidebar.subheader(" API Status")

        if Config.API_KEY:

            st.sidebar.success(
                "Mistral API Key Loaded"
            )

        else:

            if self.demo_mode:

                st.sidebar.info(
                    "Running in Demo Mode"
                )

            else:

                st.sidebar.error(
                    "No API Key Found"
                )

                st.sidebar.warning(
                    """
Add your API key to:

.env

Example:

MISTRAL_API_KEY=xxxxxxxxxxxxxxxx
"""
                )

    ####################################################################
    # Helpers
    ####################################################################

    def is_demo_mode(self):

        return self.demo_mode


########################################################################
# Singleton
########################################################################

sidebar = Sidebar()
