import pytest
from support_system.manager import SupportSystem
from support_system.models import Request
from support_system.search import search_by_id, search_by_name
from datetime import date


def test_search_by_id_found():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)

    result = search_by_id(system, "REQ001")
    assert result is not None
    assert result.request_id == "REQ001"
    assert result.customer_name == "Ada Obi"


def test_search_by_id_not_found():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)

    result = search_by_id(system, "NONEXISTENT")
    assert result is None


def test_search_by_name_found():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    r2 = Request("REQ002", "Ada Obi", "ada2@example.com", "Billing issue", date.today())
    r3 = Request(
        "REQ003", "Bob Smith", "bob@example.com", "Feature request", date.today()
    )
    system.add_request(r1)
    system.add_request(r2)
    system.add_request(r3)

    results = search_by_name(system, "Ada Obi")
    assert len(results) == 2
    assert all(r.customer_name == "Ada Obi" for r in results)


def test_search_by_name_case_insensitive():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)

    results = search_by_name(system, "ada obi")
    assert len(results) == 1
    assert results[0].customer_name == "Ada Obi"


def test_search_by_name_not_found():
    system = SupportSystem()
    r1 = Request("REQ001", "Ada Obi", "ada@example.com", "Can't log in", date.today())
    system.add_request(r1)

    results = search_by_name(system, "Nonexistent User")
    assert results == []
