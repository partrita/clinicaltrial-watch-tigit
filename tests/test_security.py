import pytest
from src.utils import sanitize_id, escape_html, get_status_badge, get_update_badge, get_changed_count_badge

def test_sanitize_id():
    assert sanitize_id("NCT12345678") == "NCT12345678"
    assert sanitize_id("Target Name") == "Target_Name"
    assert sanitize_id("../../etc/passwd") == "etc_passwd"
    assert sanitize_id("<script>alert(1)</script>") == "script_alert_1___script"
    assert sanitize_id("") == "unknown"
    assert sanitize_id(None) == "unknown"

def test_escape_html():
    assert escape_html("Hello World") == "Hello World"
    assert escape_html("Sponsor & Co.") == "Sponsor &amp; Co."
    assert escape_html("Phase 1 | Phase 2") == "Phase 1 &#124; Phase 2"
    assert escape_html("<script>") == "&lt;script&gt;"
    assert escape_html(None) == ""
    assert escape_html(123) == "123"

def test_get_status_badge():
    badge = get_status_badge("RECRUITING")
    assert 'class="badge bg-success"' in badge
    assert 'aria-label="Status: RECRUITING"' in badge
    assert "RECRUITING</span>" in badge

    badge = get_status_badge("UNKNOWN")
    assert 'class="badge bg-light text-dark"' in badge
    assert 'aria-label="Status: UNKNOWN"' in badge

def test_get_update_badge():
    assert "🔴 Changed" in get_update_badge("Changed")
    assert 'aria-label="Recently Changed"' in get_update_badge("Changed")
    assert "🟢 No Change" in get_update_badge("No Change")
    assert 'aria-label="No Recent Changes"' in get_update_badge("No Change")

def test_get_changed_count_badge():
    assert 'bg-danger' in get_changed_count_badge(5)
    assert '🔴 5' in get_changed_count_badge(5)
    assert 'bg-success' in get_changed_count_badge(0)
    assert '🟢 0' in get_changed_count_badge(0)
    assert 'bg-success' in get_changed_count_badge("abc")
