"""
Simple syntax validation.

Currently supports Python.

Additional languages can easily be added later.
"""

import ast


def validate_python(code: str):

    try:

        ast.parse(code)

        return True, None

    except SyntaxError as e:

        return (
            False,
            f"SyntaxError: {e}"
        )


def validate(language: str, code: str):

    language = language.lower()

    if "python" in language:

        return validate_python(code)

    return (
        True,
        "Validation not implemented for this language."
    )