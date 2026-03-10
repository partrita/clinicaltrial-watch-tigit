import re
import html
from typing import Any


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


def escape_html(text: Any) -> str:
    """
    Escape HTML special characters and Markdown table pipes in text to prevent XSS
    and table breakage.
    """
    if text is None:
        return ""
    # Convert to string and escape HTML
    escaped = html.escape(str(text), quote=True)
    # Also escape | to avoid breaking Markdown tables
    return escaped.replace("|", "&#124;")


def get_status_badge(status: str) -> str:
    """
    Generate an accessible Bootstrap badge for trial status.
    """
    status_map = {
        "RECRUITING": "success",
        "ACTIVE_NOT_RECRUITING": "info",
        "COMPLETED": "secondary",
        "NOT_YET_RECRUITING": "warning",
        "SUSPENDED": "danger",
        "TERMINATED": "danger",
        "WITHDRAWN": "danger",
    }
    badge_class = status_map.get(status, "light text-dark")
    safe_status = escape_html(status)
    return f'<span class="badge bg-{badge_class}" aria-label="Status: {safe_status}">{safe_status}</span>'


def get_update_badge(monitor_status: str) -> str:
    """
    Generate an accessible indicator for monitoring status.
    """
    if monitor_status == "Changed":
        return f'<span aria-label="Status changed recently">🔴 Changed</span>'
    return f'<span aria-label="No recent changes">🟢 No Change</span>'
