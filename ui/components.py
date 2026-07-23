"""
ui/components.py

Reusable UI components for the Git Conflict Arbitrator.
"""

import json
from typing import Dict
import streamlit as st


class UIComponents:

    ####################################################################
    # Project Context
    ####################################################################

    def render_project_context(self) -> str:

        return st.text_input(
            "Project Module Context / Language",
            value="Python FastAPI User Services Module",
            placeholder="e.g. Python FastAPI Auth Module",
        )

    ####################################################################
    # Developer Panels
    ####################################################################

    def render_developer_inputs(self) -> Dict[str, str]:

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Developer A")

            dev_a_name = st.text_input(
                "Name",
                value="Shaheer",
                key="dev_a_name",
            )

            dev_a_intent = st.text_input(
                "Feature Intent / Goal",
                value="Add caching to improve performance.",
                key="dev_a_intent",
            )

            dev_a_code = st.text_area(
                "Conflicting Code Block",
                height=250,
                key="dev_a_code",
            )

        with col2:

            st.subheader("Developer B")

            dev_b_name = st.text_input(
                "Name",
                value="Teammate",
                key="dev_b_name",
            )

            dev_b_intent = st.text_input(
                "Feature Intent / Goal",
                value="Add validation before returning data.",
                key="dev_b_intent",
            )

            dev_b_code = st.text_area(
                "Conflicting Code Block",
                height=250,
                key="dev_b_code",
            )

        return {

            "dev_a_name": dev_a_name,
            "dev_a_intent": dev_a_intent,
            "dev_a_code": dev_a_code,

            "dev_b_name": dev_b_name,
            "dev_b_intent": dev_b_intent,
            "dev_b_code": dev_b_code,

        }

    ####################################################################
    # Action Button
    ####################################################################

    def render_action_button(self) -> bool:

        st.markdown("<br>", unsafe_allow_html=True)

        return st.button(

            "Analyze & Arbitrate Conflicts",

            use_container_width=True,

        )

    ####################################################################
    # Input Section
    ####################################################################

    def render_inputs(self):

        module_context = self.render_project_context()

        developer_data = self.render_developer_inputs()

        analyze = self.render_action_button()

        return (
            module_context,
            developer_data,
            analyze,
        )

    ####################################################################
    # Success / Error / Loading
    ####################################################################

    def show_success(self, message: str):

        st.success(message)

    def show_error(self, message: str):

        st.error(message)

    def show_loading(self, message: str = "Analyzing..."):

        return st.spinner(message)

    ####################################################################
    # Resolved Code
    ####################################################################

    def show_resolved_code(self, result):

        st.subheader("Resolved Code")

        st.code(
            result.resolved_code,
            language="python",
        )

    ####################################################################
    # Conflict Analysis
    ####################################################################

    def show_conflict_analysis(self, result):

        st.subheader("Conflict Analysis")

        st.markdown(
            f"""
<div class="analysis-box">

{result.conflict_analysis}

</div>
""",
            unsafe_allow_html=True,
        )

    ####################################################################
    # Security Analysis
    ####################################################################

    def show_security_analysis(self, result):

        st.subheader("Security Analysis")

        st.markdown(
            f"""
<div class="security-box">

{result.security_analysis}

</div>
""",
            unsafe_allow_html=True,
        )

    ####################################################################
    # Merge Strategy
    ####################################################################

    def show_merge_strategy(self, result):

        st.subheader("Merge Strategy")

        st.info(result.merged_strategy)

    ####################################################################
    # Architecture Notes
    ####################################################################

    def show_architecture_notes(self, result):

        st.subheader("Architectural Notes")

        st.markdown(
            f"""
<div class="notes-box">

{result.architectural_notes}

</div>
""",
            unsafe_allow_html=True,
        )

    ####################################################################
    # Risks
    ####################################################################

    def show_risks(self, result):

        st.subheader("Risks")

        st.markdown(
            f"""
<div class="risk-box">

{result.risks}

</div>
""",
            unsafe_allow_html=True,
        )

    ####################################################################
    # Confidence
    ####################################################################

    def show_confidence(self, result):

        confidence = result.confidence.lower()

        css_class = "confidence-medium"

        if confidence == "high":
            css_class = "confidence-high"

        elif confidence == "low":
            css_class = "confidence-low"

        st.subheader("Confidence")

        st.markdown(
            f"""
<h3 class="{css_class}">
{result.confidence}
</h3>
""",
            unsafe_allow_html=True,
        )

    ####################################################################
    # Display Everything
    ####################################################################

    def display_results(self, result):

        self.show_resolved_code(result)

        st.divider()

        self.show_conflict_analysis(result)

        self.show_security_analysis(result)

        self.show_merge_strategy(result)

        self.show_architecture_notes(result)

        self.show_risks(result)

        self.show_confidence(result)

    ####################################################################
    # Download Merged Code
    ####################################################################

    def download_code(self, result):

        st.download_button(
            label="Download Resolved Code",
            data=result.resolved_code,
            file_name="resolved_code.py",
            mime="text/plain",
            use_container_width=True,
        )

    ####################################################################
    # Export Complete Report
    ####################################################################

    def export_report(self, result):

        report = {

            "conflict_analysis":
                result.conflict_analysis,

            "security_analysis":
                result.security_analysis,

            "merged_strategy":
                result.merged_strategy,

            "resolved_code":
                result.resolved_code,

            "architectural_notes":
                result.architectural_notes,

            "risks":
                result.risks,

            "confidence":
                result.confidence,

        }

        st.download_button(

            "Export JSON Report",

            data=json.dumps(
                report,
                indent=4,
            ),

            file_name="arbitration_report.json",

            mime="application/json",

            use_container_width=True,

        )

    ####################################################################
    # Copy Helper
    ####################################################################

    def copy_hint(self):

        st.info(
            "Select the resolved code above and copy it into your editor."
        )

    ####################################################################
    # Result Tabs
    ####################################################################

    def display_results_tabs(self, result):

        tabs = st.tabs(
            [
                " Resolved Code",
                " Conflict",
                " Security",
                " Architecture",
                " Risks",
            ]
        )

        with tabs[0]:
            self.show_resolved_code(result)
            self.download_code(result)

        with tabs[1]:
            self.show_conflict_analysis(result)
            self.show_merge_strategy(result)

        with tabs[2]:
            self.show_security_analysis(result)

        with tabs[3]:
            self.show_architecture_notes(result)

        with tabs[4]:
            self.show_risks(result)
            self.show_confidence(result)
            self.export_report(result)

    ####################################################################
    # Footer
    ####################################################################

    def footer(self):

        st.divider()

        st.caption(
            " Git Conflict Arbitrator • AI-Powered Merge Resolution"
        )

    ####################################################################
    # Full Workflow
    ####################################################################

    def render_output(self, result):

        self.display_results_tabs(result)

        self.copy_hint()

        self.footer()


########################################################################
# Singleton
########################################################################

components = UIComponents()
