import re
import html
from typing import Any
from functools import lru_cache


@lru_cache(maxsize=1024)
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
    Also explicitly escapes the pipe character '|' to prevent breaking Markdown tables.
    """
    if text is None:
        return ""
    escaped = html.escape(str(text))
    return escaped.replace("|", "&#124;")


def get_status_badge(status: str) -> str:
    """Return a Bootstrap badge for a trial status with emoji and ARIA label."""
    # Maps raw status to (display_label, emoji, bootstrap_class)
    status_configs = {
        "RECRUITING": ("Recruiting", "🟢", "success"),
        "ACTIVE_NOT_RECRUITING": ("Active (Not Recruiting)", "🔵", "info"),
        "COMPLETED": ("Completed", "⚪", "secondary"),
        "NOT_YET_RECRUITING": ("Not Yet Recruiting", "🟡", "warning"),
        "SUSPENDED": ("Suspended", "🟠", "danger"),
        "TERMINATED": ("Terminated", "🔴", "danger"),
        "WITHDRAWN": ("Withdrawn", "🔴", "danger"),
    }

    label, emoji, bg_class = status_configs.get(
        status, (status.replace("_", " ").title(), "⚪", "light text-dark")
    )

    safe_label = escape_html(label)
    safe_status = escape_html(status)
    display_text = f"{emoji} {safe_label}" if emoji else safe_label

    return (
        f'<span class="badge bg-{bg_class}" '
        f'title="Original status: {safe_status}" '
        f'aria-label="Status: {safe_label}">{display_text}</span>'
    )


def get_update_badge(monitor_status: str, last_change_date: str = None) -> str:
    """Return a badge/emoji for monitoring status with ARIA label and title."""
    safe_status = escape_html(monitor_status)
    if monitor_status == "Changed":
        title = "Changes detected since last crawl"
        if last_change_date:
            title += f" (Last change: {escape_html(last_change_date)})"
        return f'<span aria-label="Changes detected" title="{title}">🔴 {safe_status}</span>'

    title = "No changes detected since last crawl"
    if last_change_date:
        title += f" (Last change: {escape_html(last_change_date)})"
    return f'<span aria-label="No recent changes" title="{title}">🟢 {safe_status}</span>'


def format_enrollment(count: Any) -> str:
    """Format enrollment count with commas."""
    if count is None or count == "N/A":
        return "N/A"
    try:
        return f"{int(count):,}"
    except (ValueError, TypeError):
        return str(count)


def get_changed_count_badge(count: int) -> str:
    """Return a badge for changed trial count with title."""
    if count > 0:
        return f'<span aria-label="{count} trials changed" title="{count} trials have updates">🔴 {count}</span>'
    return '<span aria-label="No trials changed" title="No trials have updates">🟢 0</span>'
