import re
import html
from typing import Any


def escape_html(text: Any) -> str:
    """
    Escape HTML special characters in a string to prevent XSS.
    Also escapes the pipe character '|' to prevent breaking Markdown tables.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)

    # Standard HTML escaping
    escaped = html.escape(text)
    # Escape pipe character for Markdown tables
    return escaped.replace("|", "&#124;")


def sanitize_id(identifier: str) -> str:
    """
    Sanitize an identifier (trial ID or target name) to prevent
    path traversal and code injection.
    Allows only alphanumeric characters, dashes, and underscores.
    """
    if not identifier:
        return "unknown"
    # Replace any non-alphanumeric, non-dash, non-underscore characters with an underscore
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "_", str(identifier))
    # Remove leading/trailing underscores and prevent empty string
    sanitized = sanitized.strip("_")
    return sanitized if sanitized else "unknown"
