import re
import html


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


def escape_html(text: str) -> str:
    """
    Escape HTML special characters to prevent XSS.
    """
    if not text or not isinstance(text, str):
        return text
    return html.escape(text)


def get_status_badge(status: str) -> str:
    """
    Returns an accessible Bootstrap badge for clinical trial status.
    """
    status = str(status).upper() if status else "N/A"
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
    # Accessibility: added aria-label and meaningful text
    return f'<span class="badge bg-{badge_class}" aria-label="Trial Status: {status}">{status}</span>'


def get_update_badge(monitor_status: str) -> str:
    """
    Returns an accessible indicator for monitoring status changes.
    """
    if monitor_status == "Changed":
        return '<span aria-label="Status: Changed" title="Changed in last 30 days">🔴 Changed</span>'
    return '<span aria-label="Status: No Change" title="No change in last 30 days">🟢 No Change</span>'
