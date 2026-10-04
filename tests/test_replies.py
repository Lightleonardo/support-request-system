import pytest
from support_system.manager import SupportSystem
from support_system.models import Request
from support_system.replies import display_replies, display_replies_indented
from datetime import date


def test_display_replies_empty():
    result = display_replies([])
    assert result == []


def test_display_replies_single():
    replies = ["First reply"]
    result = display_replies(replies)
    assert len(result) == 1
    assert result[0] == "Reply 1: First reply"


def test_display_replies_multiple():
    replies = ["First reply", "Second reply", "Third reply"]
    result = display_replies(replies)
    assert len(result) == 3
    assert result[0] == "Reply 1: First reply"
    assert result[1] == "Reply 2: Second reply"
    assert result[2] == "Reply 3: Third reply"


def test_display_replies_with_request():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    r1.replies = ["Thanks for reporting", "We're looking into it", "Fixed in v2.1"]
    system.add_request(r1)

    result = display_replies(r1.replies)
    assert len(result) == 3
    assert result[0] == "Reply 1: Thanks for reporting"
    assert result[1] == "Reply 2: We're looking into it"
    assert result[2] == "Reply 3: Fixed in v2.1"


def test_display_replies_indented():
    replies = ["First reply", "Second reply", "Third reply"]
    result = display_replies_indented(replies)
    assert len(result) == 3
    assert result[0] == "Reply 1: First reply"
    assert result[1] == "  Reply 2: Second reply"
    assert result[2] == "    Reply 3: Third reply"


def test_display_replies_recursion_order():
    """Verify replies are displayed in correct order (index 0 first)."""
    replies = ["A", "B", "C", "D", "E"]
    result = display_replies(replies)
    expected = ["Reply 1: A", "Reply 2: B", "Reply 3: C", "Reply 4: D", "Reply 5: E"]
    assert result == expected
