import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Central configuration class.
    """

    APP_NAME = "Git Conflict Arbitrator"

    APP_ICON = "⚡"

    MODEL_NAME = "mistral-large-latest"

    TEMPERATURE = 0.2

    MAX_TOKENS = 4000

    API_KEY = (
        os.getenv("MISTRAL_API_KEY")
        or os.getenv("API_KEY")
    )

    DEMO_MODE = API_KEY is None