import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from utils import escape_html, sanitize_id

def test_escape_html():
    # Standard HTML characters
    assert escape_html("<script>alert('XSS')</script>") == "&lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"
    assert escape_html("Data & More") == "Data &amp; More"
    assert escape_html('"Double Quotes"') == "&quot;Double Quotes&quot;"
    assert escape_html("'Single Quotes'") == "&#x27;Single Quotes&#x27;"

    # Pipe character for Markdown tables
    assert escape_html("Pipe | Character") == "Pipe &#124; Character"
    assert escape_html("|Multiple|Pipes|") == "&#124;Multiple&#124;Pipes&#124;"

    # Non-string input
    assert escape_html(None) == ""
    assert escape_html(123) == "123"
    assert escape_html(True) == "True"

def test_sanitize_id():
    # Normal IDs
    assert sanitize_id("NCT12345678") == "NCT12345678"
    assert sanitize_id("target-name") == "target-name"
    assert sanitize_id("target_name") == "target_name"

    # Malicious input
    assert sanitize_id("../../etc/passwd") == "etc_passwd"
    assert sanitize_id("<script>alert(1)</script>") == "script_alert_1___script"
    assert sanitize_id("id with spaces") == "id_with_spaces"
    assert sanitize_id("!!special@@chars##") == "special__chars"

    # Edge cases
    assert sanitize_id(None) == "unknown"
    assert sanitize_id("") == "unknown"
    assert sanitize_id("___") == "unknown"
    assert sanitize_id(123) == "123"
