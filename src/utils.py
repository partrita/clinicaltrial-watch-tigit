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
    Escape HTML special characters in a string.
    Also escapes the pipe character '|' to avoid breaking Markdown tables.
    """
    if text is None:
        return ""
    s = html.escape(str(text))
    return s.replace("|", "&#124;")


def get_status_badge(status: str) -> str:
    """
    Return a Bootstrap badge for a trial status with an ARIA label.
    """
    status = str(status) if status else "N/A"
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
    return f'<span class="badge bg-{badge_class}" aria-label="Status: {escaped_status}">{escaped_status}</span>'


def get_update_badge(monitor_status: str) -> str:
    """
    Return a badge/indicator for the update status.
    """
    status = str(monitor_status) if monitor_status else "No Change"
    if status == "Changed":
        return f'<span aria-label="Recently Changed">🔴 Changed</span>'
    return f'<span aria-label="No Recent Changes">🟢 No Change</span>'


def get_changed_count_badge(count: int) -> str:
    """
    Return a badge for the number of changed trials in a target.
    """
    try:
        val = int(count)
    except (ValueError, TypeError):
        val = 0

    if val > 0:
        return f'<span class="badge bg-danger" aria-label="{val} trials changed">🔴 {val}</span>'
    return f'<span class="badge bg-success" aria-label="No trials changed">🟢 0</span>'
