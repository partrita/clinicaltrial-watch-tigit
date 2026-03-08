import re


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


def get_status_badge(status: str) -> str:
    """Return a Bootstrap badge for the given trial status."""
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
    return f'<span class="badge bg-{badge_class}" aria-label="Status: {status}">{status}</span>'


def get_update_badge(monitor_status: str) -> str:
    """Return a Bootstrap badge for the monitor status."""
    if monitor_status == "No Change":
        return '<span class="badge bg-success" aria-label="No change detected">No Change</span>'
    return f'<span class="badge bg-danger" aria-label="Change detected: {monitor_status}">{monitor_status}</span>'
