import re
import html
from typing import Any, Optional


def sanitize_id(identifier: Optional[Any]) -> str:
    """
    Sanitize an identifier (trial ID or target name) to prevent
    path traversal and code injection.
    Allows only alphanumeric characters, dashes, and underscores.
    """
    if identifier is None or identifier == "":
        return "unknown"
    # Replace any non-alphanumeric, non-dash, non-underscore characters with an underscore
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "_", str(identifier))
    # Remove leading/trailing underscores and prevent empty string
    sanitized = sanitized.strip("_")
    return sanitized if sanitized else "unknown"


def escape_html(text: Optional[Any]) -> str:
    """
    Escape HTML special characters in a string to prevent XSS.
    Also escapes the pipe character '|' to prevent breaking Markdown tables.
    """
    if text is None:
        return ""
    # Use standard html.escape for &, <, >, ", '
    escaped = html.escape(str(text))
    # Additionally escape | for Markdown table safety
    return escaped.replace("|", "&#124;")
