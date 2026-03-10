import sys
import os

# Add src/ to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import escape_html, get_status_badge, get_update_badge


def test_escape_html():
    assert escape_html("safe") == "safe"
    assert escape_html("<script>") == "&lt;script&gt;"
    assert escape_html("John & Doe") == "John &amp; Doe"
    assert escape_html(' "double" and \'single\' ') == " &quot;double&quot; and &#x27;single&#x27; "
    assert escape_html(None) == ""
    assert escape_html(123) == "123"


def test_get_status_badge():
    badge = get_status_badge("RECRUITING")
    assert 'class="badge bg-success"' in badge
    assert 'aria-label="Status: RECRUITING"' in badge
    assert "RECRUITING</span>" in badge

    badge_xss = get_status_badge("<script>alert(1)</script>")
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in badge_xss
    assert "light text-dark" in badge_xss


def test_get_update_badge():
    badge_changed = get_update_badge("Changed")
    assert "🔴 Changed" in badge_changed
    assert 'aria-label="Status changed recently"' in badge_changed

    badge_no_change = get_update_badge("No Change")
    assert "🟢 No Change" in badge_no_change
    assert 'aria-label="No recent changes"' in badge_no_change
