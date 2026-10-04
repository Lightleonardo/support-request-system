import pytest
from support_system.manager import SupportSystem
from support_system.models import Request
from support_system.sorting import sort_requests, insertion_sort_requests
from datetime import date, timedelta


def test_sort_by_date():
    system = SupportSystem()
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    r1 = Request("REQ003", "User C", "c@example.com", "Third", tomorrow)
    r2 = Request("REQ001", "User A", "a@example.com", "First", yesterday)
    r3 = Request("REQ002", "User B", "b@example.com", "Second", today)
    system.add_request(r1)
    system.add_request(r2)
    system.add_request(r3)

    sorted_requests = sort_requests(system, by="date")
    assert sorted_requests[0].request_id == "REQ001"  # yesterday
    assert sorted_requests[1].request_id == "REQ002"  # today
    assert sorted_requests[2].request_id == "REQ003"  # tomorrow


def test_sort_by_priority():
    system = SupportSystem()
    today = date.today()

    r1 = Request("REQ001", "User A", "a@example.com", "Normal priority", today)
    r2 = Request("REQ002", "User B", "b@example.com", "High priority", today)
    r3 = Request("REQ003", "User C", "c@example.com", "Low priority", today)
    r1.priority = "normal"
    r2.priority = "high"
    r3.priority = "low"
    system.add_request(r1)
    system.add_request(r2)
    system.add_request(r3)

    sorted_requests = sort_requests(system, by="priority")
    assert sorted_requests[0].priority == "high"
    assert sorted_requests[1].priority == "normal"
    assert sorted_requests[2].priority == "low"


def test_sort_by_status():
    system = SupportSystem()
    today = date.today()

    r1 = Request("REQ001", "User A", "a@example.com", "Processing", today)
    r2 = Request("REQ002", "User B", "b@example.com", "Closed", today)
    r3 = Request("REQ003", "User C", "c@example.com", "Open", today)
    r1.status = "processing"
    r2.status = "closed"
    r3.status = "open"
    system.add_request(r1)
    system.add_request(r2)
    system.add_request(r3)

    sorted_requests = sort_requests(system, by="status")
    assert sorted_requests[0].status == "open"
    assert sorted_requests[1].status == "processing"
    assert sorted_requests[2].status == "closed"


def test_sort_invalid_key():
    system = SupportSystem()
    r1 = Request("REQ001", "User A", "a@example.com", "Test", date.today())
    system.add_request(r1)

    with pytest.raises(ValueError):
        sort_requests(system, by="invalid")


def test_both_sorts_agree():
    """Test that both sorting approaches produce the same result."""
    system = SupportSystem()
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    r1 = Request("REQ003", "User C", "c@example.com", "Third", tomorrow)
    r2 = Request("REQ001", "User A", "a@example.com", "First", yesterday)
    r3 = Request("REQ002", "User B", "b@example.com", "Second", today)
    system.add_request(r1)
    system.add_request(r2)
    system.add_request(r3)

    builtin_result = sort_requests(system, by="date")
    manual_result = insertion_sort_requests(system, by="date")

    assert len(builtin_result) == len(manual_result)
    for b, m in zip(builtin_result, manual_result):
        assert b.request_id == m.request_id


def test_both_sorts_agree_priority():
    """Test that both sorting approaches agree on priority sort."""
    system = SupportSystem()
    today = date.today()

    r1 = Request("REQ001", "User A", "a@example.com", "Normal", today)
    r2 = Request("REQ002", "User B", "b@example.com", "High", today)
    r3 = Request("REQ003", "User C", "c@example.com", "Low", today)
    r1.priority = "normal"
    r2.priority = "high"
    r3.priority = "low"
    system.add_request(r1)
    system.add_request(r2)
    system.add_request(r3)

    builtin_result = sort_requests(system, by="priority")
    manual_result = insertion_sort_requests(system, by="priority")

    assert len(builtin_result) == len(manual_result)
    for b, m in zip(builtin_result, manual_result):
        assert b.request_id == m.request_id


def test_both_sorts_agree_status():
    """Test that both sorting approaches agree on status sort."""
    system = SupportSystem()
    today = date.today()

    r1 = Request("REQ001", "User A", "a@example.com", "Processing", today)
    r2 = Request("REQ002", "User B", "b@example.com", "Closed", today)
    r3 = Request("REQ003", "User C", "c@example.com", "Open", today)
    r1.status = "processing"
    r2.status = "closed"
    r3.status = "open"
    system.add_request(r1)
    system.add_request(r2)
    system.add_request(r3)

    builtin_result = sort_requests(system, by="status")
    manual_result = insertion_sort_requests(system, by="status")

    assert len(builtin_result) == len(manual_result)
    for b, m in zip(builtin_result, manual_result):
        assert b.request_id == m.request_id
