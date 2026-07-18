"""
core/response_parser.py

Responsible for parsing and validating LLM responses.

Supported inputs:
- ArbitrationResponse
- dict
- JSON string
- Markdown wrapped JSON
"""

import json
import re
from typing import Any

from models.response_models import ArbitrationResponse
from utils.logger import get_logger

logger = get_logger(__name__)


class ResponseParser:

    ####################################################################
    # Remove Markdown Code Blocks
    ####################################################################

    @staticmethod
    def strip_markdown(text: str) -> str:
        """
        Removes ```json ... ``` wrappers.
        """

        if not text:
            return ""

        text = re.sub(
            r"^```(?:json)?",
            "",
            text.strip(),
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"```$",
            "",
            text.strip(),
        )

        return text.strip()

    ####################################################################
    # Safe JSON Loading
    ####################################################################

    @staticmethod
    def safe_json_load(text: str):

        text = ResponseParser.strip_markdown(text)

        try:

            return json.loads(text)

        except Exception as e:

            logger.exception(e)

            raise ValueError(
                "Model returned invalid JSON."
            )

    ####################################################################
    # Fill Missing Fields
    ####################################################################

    @staticmethod
    def normalize(data: dict):

        defaults = {

            "conflict_analysis":
                "No analysis generated.",

            "security_analysis":
                "No security analysis generated.",

            "merged_strategy":
                "No merge strategy generated.",

            "resolved_code":
                "",

            "architectural_notes":
                "No architectural notes.",

            "risks":
                "None",

            "confidence":
                "Unknown",
        }

        for key, value in defaults.items():

            if key not in data:

                data[key] = value

        return data

    ####################################################################
    # Parse
    ####################################################################

    def parse(self, response: Any) -> ArbitrationResponse:

        ###############################################################
        # Already Parsed
        ###############################################################

        if isinstance(
            response,
            ArbitrationResponse,
        ):

            logger.info(
                "Received structured response."
            )

            return response

        ###############################################################
        # Dictionary
        ###############################################################

        if isinstance(response, dict):

            logger.info(
                "Received dictionary response."
            )

            response = self.normalize(response)

            return ArbitrationResponse(**response)

        ###############################################################
        # JSON String
        ###############################################################

        if isinstance(response, str):

            logger.info(
                "Received JSON string."
            )

            data = self.safe_json_load(response)

            data = self.normalize(data)

            return ArbitrationResponse(**data)

        ###############################################################
        # Unknown
        ###############################################################

        raise TypeError(

            f"Unsupported response type: {type(response)}"

        )

    ####################################################################
    # Convert Back to Dict
    ####################################################################

    @staticmethod
    def to_dict(response: ArbitrationResponse):

        return response.model_dump()

    ####################################################################
    # Pretty JSON
    ####################################################################

    @staticmethod
    def pretty_json(response: ArbitrationResponse):

        return json.dumps(

            response.model_dump(),

            indent=4,

            ensure_ascii=False,

        )


########################################################################
# Singleton
########################################################################

response_parser = ResponseParser()