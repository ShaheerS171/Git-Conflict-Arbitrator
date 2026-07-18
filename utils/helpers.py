import json


def is_empty(value):

    if value is None:
        return True

    if isinstance(value, str):

        return value.strip() == ""

    return False


def safe_json_load(text):

    try:

        return json.loads(text)

    except Exception:

        return None


def clean_code(text: str):

    if not text:

        return ""

    text = text.replace("```python", "")

    text = text.replace("```", "")

    return text.strip()


def truncate(text: str, limit: int = 250):

    if len(text) <= limit:

        return text

    return text[:limit] + "..."