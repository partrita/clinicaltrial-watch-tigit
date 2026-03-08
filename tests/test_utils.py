from src.utils import escape_html, sanitize_id

def test_escape_html():
    assert escape_html("Hello <script>alert(1)</script>") == "Hello &lt;script&gt;alert(1)&lt;/script&gt;"
    assert escape_html("Special characters: & \" '") == "Special characters: &amp; &quot; &#x27;"
    assert escape_html(123) == "123"
    assert escape_html(None) == ""

def test_sanitize_id():
    assert sanitize_id("NCT12345678") == "NCT12345678"
    assert sanitize_id("Target Name") == "Target_Name"
    assert sanitize_id("../etc/passwd") == "etc_passwd"
    assert sanitize_id("") == "unknown"
    assert sanitize_id(None) == "unknown"
