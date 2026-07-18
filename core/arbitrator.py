"""
core/arbitrator.py

Main orchestration layer for the Git Conflict Arbitrator.

Flow

Input
    ↓
Validation
    ↓
Security Scan
    ↓
Syntax Validation
    ↓
Prompt Builder
    ↓
LLM Client
    ↓
Post Processing
    ↓
Return ArbitrationResponse
"""

from models.response_models import ArbitrationResponse

from utils.logger import get_logger
from utils.helpers import is_empty

from security.security_checker import security_summary
from security.syntax_validator import validate

from core.prompt_builder import prompt_builder
from core.llm_client import get_llm_client


logger = get_logger(__name__)


class GitConflictArbitrator:

    def __init__(self):
        pass

    ####################################################################
    # Validation
    ####################################################################

    def _validate_inputs(
        self,
        module_context,
        dev_a_name,
        dev_a_intent,
        dev_a_code,
        dev_b_name,
        dev_b_intent,
        dev_b_code,
    ):

        if is_empty(module_context):
            raise ValueError(
                "Project Context cannot be empty."
            )

        if is_empty(dev_a_name):
            raise ValueError(
                "Developer A name is missing."
            )

        if is_empty(dev_b_name):
            raise ValueError(
                "Developer B name is missing."
            )

        if is_empty(dev_a_code):
            raise ValueError(
                "Developer A code is empty."
            )

        if is_empty(dev_b_code):
            raise ValueError(
                "Developer B code is empty."
            )

    ####################################################################
    # Security Scan
    ####################################################################

    def _security_scan(
        self,
        dev_a_code,
        dev_b_code,
    ):

        ok_a, report_a = security_summary(dev_a_code)

        ok_b, report_b = security_summary(dev_b_code)

        logger.info("Security scan completed.")

        return {
            "developer_a": {
                "safe": ok_a,
                "report": report_a,
            },
            "developer_b": {
                "safe": ok_b,
                "report": report_b,
            },
        }

    ####################################################################
    # Syntax Validation
    ####################################################################

    def _syntax_validation(
        self,
        language,
        dev_a_code,
        dev_b_code,
    ):

        syntax_a = validate(
            language,
            dev_a_code,
        )

        syntax_b = validate(
            language,
            dev_b_code,
        )

        logger.info("Syntax validation completed.")

        return {
            "developer_a": syntax_a,
            "developer_b": syntax_b,
        }

    ####################################################################
    # Main Entry
    ####################################################################

    def arbitrate(
        self,
        module_context,
        dev_a_name,
        dev_a_intent,
        dev_a_code,
        dev_b_name,
        dev_b_intent,
        dev_b_code,
    ) -> ArbitrationResponse:

        logger.info(
            "Starting Git Conflict Arbitration..."
        )

        ###############################################################
        # Validation
        ###############################################################

        self._validate_inputs(
            module_context,
            dev_a_name,
            dev_a_intent,
            dev_a_code,
            dev_b_name,
            dev_b_intent,
            dev_b_code,
        )

        ###############################################################
        # Security Scan
        ###############################################################

        security_report = self._security_scan(
            dev_a_code,
            dev_b_code,
        )

        ###############################################################
        # Syntax Validation
        ###############################################################

        syntax_report = self._syntax_validation(
            module_context,
            dev_a_code,
            dev_b_code,
        )

        logger.info(
            "Prompt construction..."
        )

        ###############################################################
        # Build Prompt
        ###############################################################

        prompt = prompt_builder.build_prompt(
            module_context=module_context,
            dev_a_name=dev_a_name,
            dev_a_intent=dev_a_intent,
            dev_a_code=dev_a_code,
            dev_b_name=dev_b_name,
            dev_b_intent=dev_b_intent,
            dev_b_code=dev_b_code,
        )

        ###############################################################
        # LLM Call
        ###############################################################

        logger.info(
            "Sending request to language model..."
        )

        response = get_llm_client().generate(prompt)

        ###############################################################
        # Append Local Security Results
        ###############################################################

        local_report = []

        local_report.append(
            "========== LOCAL SECURITY SCAN =========="
        )

        local_report.append(
            f"Developer A Safe: {security_report['developer_a']['safe']}"
        )

        local_report.append(
            security_report["developer_a"]["report"]
        )

        local_report.append("")

        local_report.append(
            f"Developer B Safe: {security_report['developer_b']['safe']}"
        )

        local_report.append(
            security_report["developer_b"]["report"]
        )

        response.security_analysis = (
            "\n\n".join(local_report)
            + "\n\n"
            + response.security_analysis
        )

        ###############################################################
        # Append Syntax Results
        ###############################################################

        syntax_notes = []

        syntax_notes.append(
            "========== LOCAL SYNTAX VALIDATION =========="
        )

        syntax_notes.append(
            f"Developer A: {syntax_report['developer_a'][1]}"
        )

        syntax_notes.append(
            f"Developer B: {syntax_report['developer_b'][1]}"
        )

        response.architectural_notes += (

            "\n\n"

            + "\n".join(syntax_notes)

        )

        logger.info(
            "Arbitration completed successfully."
        )

        return response


########################################################################
# Singleton
########################################################################

arbitrator = GitConflictArbitrator()