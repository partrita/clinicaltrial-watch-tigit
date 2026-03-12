import pytest
from src.utils import sanitize_id, escape_html


def test_sanitize_id_basic():
    assert sanitize_id("NCT12345678") == "NCT12345678"
    assert sanitize_id("My-Target_Name") == "My-Target_Name"


def test_sanitize_id_path_traversal():
    assert sanitize_id("../../etc/passwd") == "etc_passwd"
    assert sanitize_id("trials/data.json") == "trials_data_json"


def test_sanitize_id_special_chars():
    assert sanitize_id("target@name#123") == "target_name_123"
    assert sanitize_id("   space   ") == "space"
    assert sanitize_id("!!!") == "unknown"


def test_sanitize_id_none_and_empty():
    assert sanitize_id(None) == "unknown"
    assert sanitize_id("") == "unknown"


def test_escape_html_basic():
    assert escape_html("safe text") == "safe text"
    assert escape_html("<script>alert(1)</script>") == "&lt;script&gt;alert(1)&lt;/script&gt;"


def test_escape_html_quotes():
    assert escape_html('Hello "World"') == "Hello &quot;World&quot;"
    assert escape_html("It's me") == "It&#x27;s me"


def test_escape_html_markdown_table():
    # Pipe should be escaped to prevent breaking markdown tables
    assert escape_html("Field | Value") == "Field &#124; Value"


def test_escape_html_types():
    assert escape_html(None) == ""
    assert escape_html(123) == "123"
    assert escape_html(45.67) == "45.67"


def test_escape_html_combined():
    assert escape_html("<b id='test'>Hello | World</b>") == "&lt;b id=&#x27;test&#x27;&gt;Hello &#124; World&lt;/b&gt;"
