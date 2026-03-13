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
    Also escapes the pipe character '|' to prevent breaking Markdown tables.
    """
    if text is None:
        return ""
    if not isinstance(text, str):
        text = str(text)
    # Use standard html.escape but also escape | for markdown tables
    escaped = html.escape(text, quote=True)
    return escaped.replace("|", "&#124;")


def get_status_badge(status: str) -> str:
    """
    Return a Bootstrap badge for the trial status with ARIA label.
    """
    status_val = escape_html(status or "N/A")
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
    return f'<span class="badge bg-{badge_class}" aria-label="Status: {status_val}">{status_val}</span>'


def get_update_badge(monitor_status: str) -> str:
    """
    Return a status indicator (emoji + text) for updates with ARIA label.
    """
    status_val = escape_html(monitor_status or "No Change")
    if status_val == "No Change":
        return f'<span aria-label="No changes in the last 30 days">🟢 {status_val}</span>'
    return f'<span aria-label="Trial has updates (e.g., changed or new) in the last 30 days">🔴 {status_val}</span>'


def get_changed_count_badge(count: int) -> str:
    """
    Return a badge for the number of changed trials with ARIA label.
    """
    try:
        count_val = int(count)
    except (ValueError, TypeError):
        count_val = 0

    if count_val > 0:
        return f'<span class="badge bg-danger" aria-label="{count_val} trials changed in the last 30 days">🔴 {count_val}</span>'
    return f'<span class="badge bg-success" aria-label="No trials changed in the last 30 days">🟢 0</span>'
