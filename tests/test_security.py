from src.utils import sanitize_id, escape_html, get_status_badge, get_update_badge, get_changed_count_badge

def test_sanitize_id():
    assert sanitize_id("NCT12345678") == "NCT12345678"
    assert sanitize_id("Target Name") == "Target_Name"
    assert sanitize_id("../../etc/passwd") == "etc_passwd"
    assert sanitize_id("") == "unknown"
    assert sanitize_id(None) == "unknown"

def test_escape_html():
    assert escape_html("<script>") == "&lt;script&gt;"
    assert escape_html("A | B") == "A &#124; B"
    assert escape_html("O'Reilly") == "O&#x27;Reilly"
    assert escape_html(None) == ""
    assert escape_html(123) == "123"

def test_get_status_badge():
    badge = get_status_badge("RECRUITING")
    assert 'class="badge bg-success"' in badge
    assert 'aria-label="Status: RECRUITING"' in badge
    assert 'RECRUITING</span>' in badge

    badge_unknown = get_status_badge("UNKNOWN_STATUS")
    assert 'class="badge bg-light text-dark"' in badge_unknown
    assert 'aria-label="Status: UNKNOWN_STATUS"' in badge_unknown

def test_get_update_badge():
    # Test 'Changed'
    badge_changed = get_update_badge("Changed")
    assert "🔴 Changed" in badge_changed
    assert 'aria-label="Trial has updates (e.g., changed or new) in the last 30 days"' in badge_changed

    # Test 'New' (the fix)
    badge_new = get_update_badge("New")
    assert "🔴 New" in badge_new
    assert 'aria-label="Trial has updates (e.g., changed or new) in the last 30 days"' in badge_new

    # Test 'No Change'
    badge_no_change = get_update_badge("No Change")
    assert "🟢 No Change" in badge_no_change
    assert 'aria-label="No changes in the last 30 days"' in badge_no_change

def test_get_changed_count_badge():
    badge_some = get_changed_count_badge(5)
    assert "🔴 5" in badge_some
    assert 'aria-label="5 trials changed in the last 30 days"' in badge_some
    assert 'bg-danger' in badge_some

    badge_zero = get_changed_count_badge(0)
    assert "🟢 0" in badge_zero
    assert 'aria-label="No trials changed in the last 30 days"' in badge_zero
    assert 'bg-success' in badge_zero
