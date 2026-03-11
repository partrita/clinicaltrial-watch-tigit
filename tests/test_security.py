import pytest
from src.utils import sanitize_id, escape_html


def test_sanitize_id():
    # Test normal cases
    assert sanitize_id("NCT12345678") == "NCT12345678"
    assert sanitize_id("CCR8-Target") == "CCR8-Target"
    assert sanitize_id("TIGIT_Trial") == "TIGIT_Trial"

    # Test path traversal attempts
    assert sanitize_id("../../../etc/passwd") == "etc_passwd"
    assert sanitize_id("..\\..\\windows\\system32") == "windows_system32"

    # Test special characters
    assert sanitize_id("Target!@#$%^&*()") == "Target"
    assert sanitize_id("  Spaces Around  ") == "Spaces_Around"

    # Test empty or None
    assert sanitize_id("") == "unknown"
    assert sanitize_id(None) == "unknown"


def test_escape_html():
    # Test normal strings
    assert escape_html("Normal text") == "Normal text"
    assert escape_html("NCT12345") == "NCT12345"

    # Test HTML characters (XSS vectors)
    assert escape_html("<script>alert(1)</script>") == "&lt;script&gt;alert(1)&lt;/script&gt;"
    assert escape_html('Sponsor "Big Pharma"') == "Sponsor &quot;Big Pharma&quot;"
    assert escape_html("Conditions & Treatments") == "Conditions &amp; Treatments"
    assert escape_html("O'Reilly") == "O&#x27;Reilly"

    # Test Markdown table breaker
    assert escape_html("Treatment | Observation") == "Treatment &#124; Observation"

    # Test combined
    assert escape_html('<div class="test">Data | More Data</div>') == "&lt;div class=&quot;test&quot;&gt;Data &#124; More Data&lt;/div&gt;"

    # Test empty or None
    assert escape_html("") == ""
    assert escape_html(None) == ""
