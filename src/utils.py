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
    Escape HTML special characters and also pipe characters to avoid breaking
    Markdown tables.
    """
    if text is None:
        return ""
    # Standard HTML escape
    escaped = html.escape(str(text))
    # Additionally escape | for Markdown tables
    return escaped.replace("|", "&#124;")


def get_status_badge(status: str) -> str:
    """
    Returns an accessible Bootstrap badge for a trial status.
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
    # Use aria-label for better accessibility
    return f'<span class="badge bg-{badge_class}" aria-label="Status: {status}">{escape_html(status)}</span>'


def get_update_badge(monitor_status: str) -> str:
    """
    Returns a status indicator badge for monitoring status.
    """
    if monitor_status == "No Change":
        return f'<span aria-label="No recent changes">🟢 No Change</span>'
    else:
        return f'<span aria-label="Recent changes detected">🔴 {escape_html(monitor_status)}</span>'


def get_changed_count_badge(count: int) -> str:
    """
    Returns a badge indicating the number of changed trials in a target.
    """
    if count > 0:
        return f'<span class="badge bg-danger" aria-label="{count} trials changed">🔴 {count}</span>'
    else:
        return f'<span class="badge bg-success" aria-label="No trials changed">🟢 0</span>'
