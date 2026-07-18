"""
core/llm_client.py

Handles all communication with the Mistral LLM.
"""

"""
Try multiple import locations for the Mistral client to avoid import errors
across different packaging variations.
"""

try:
    from mistralai.client import Mistral
    print("Imported from mistralai successfully.")
except Exception as e:
    print("Error importing mistralai:", repr(e))
    raise

from config import Config
from models.response_models import ArbitrationResponse
from core.response_parser import response_parser
from utils.logger import get_logger

logger = get_logger(__name__)


class LLMClient:
    """
    Wrapper around the Mistral API.
    """

    def __init__(self):

        if Mistral is None:
            raise ImportError(
                "Mistral client package is not installed."
            )

        if not Config.API_KEY:
            raise ValueError(
                "MISTRAL_API_KEY not found."
            )

        self.client = Mistral(
            api_key=Config.API_KEY
        )

        self.model = Config.MODEL_NAME

    ####################################################################
    # Structured Response
    ####################################################################

    def _structured_request(
        self,
        prompt: str,
    ) -> ArbitrationResponse:

        logger.info("Sending structured request...")

        response = self.client.chat.parse(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            response_format=ArbitrationResponse,
            temperature=Config.TEMPERATURE,
        )

        parsed = response.choices[0].message.parsed

        if parsed is None:
            raise RuntimeError(
                "Structured response is empty."
            )

        return parsed

    ####################################################################
    # JSON Fallback
    ####################################################################

    def _fallback_request(
        self,
        prompt: str,
    ) -> ArbitrationResponse:

        logger.warning(
            "Using JSON fallback..."
        )

        response = self.client.chat.complete(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": (
                        prompt
                        + "\n\nReturn ONLY valid JSON."
                    ),
                }
            ],
            response_format={
                "type": "json_object"
            },
            temperature=Config.TEMPERATURE,
        )

        content = response.choices[0].message.content

        return response_parser.parse(content)

    ####################################################################
    # Public API
    ####################################################################

    def generate(
        self,
        prompt: str,
    ) -> ArbitrationResponse:

        try:

            result = self._structured_request(
                prompt
            )

            logger.info(
                "Structured parsing successful."
            )

            return response_parser.parse(result)

        except Exception as e:

            logger.warning(
                f"Structured request failed: {e}"
            )

        try:

            return self._fallback_request(
                prompt
            )

        except Exception as e:

            logger.exception(e)

            raise RuntimeError(
                "Failed to obtain a valid response from the LLM."
            ) from e


########################################################################
# Factory (lazy – avoids crashing on import when no API key is set)
########################################################################

def get_llm_client() -> "LLMClient":
    """Return a fresh LLMClient.  Raises ImportError/ValueError if the
    Mistral package or API key is not available, so callers can catch."""
    return LLMClient()