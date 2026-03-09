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
    """Escape HTML special characters in a string to prevent XSS."""
    if text is None:
        return ""
    return html.escape(str(text))


def get_status_badge(status: str) -> str:
    """
    Generate an accessible Bootstrap badge for a study status.
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
    escaped_status = escape_html(status)
    # Using aria-label for accessibility
    return f'<span class="badge bg-{badge_class}" aria-label="Study Status: {escaped_status}">{escaped_status}</span>'


def get_update_badge(monitor_status: str) -> str:
    """
    Generate an accessible indicator for trial updates.
    """
    escaped_status = escape_html(monitor_status)
    if monitor_status == "No Change":
        return f'<span class="badge border text-dark" aria-label="No changes detected since last update">🟢 {escaped_status}</span>'
    else:
        # We use a red badge for changes
        return f'<span class="badge border text-danger" aria-label="Changes detected: {escaped_status}">🔴 {escaped_status}</span>'
